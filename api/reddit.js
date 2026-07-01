// Reddit read proxy with app-only OAuth.
// Reddit 403s unauthenticated .json from datacenter IPs, so we mint an app-only
// (client_credentials) bearer token and read via oauth.reddit.com.
//
// PORTABLE: this is a self-contained capability (token mint + cache + read).
// Lift api/reddit.js + the two env vars to reuse it elsewhere (e.g. Boris).
//
// Setup (one-time, Will):
//   1. https://www.reddit.com/prefs/apps -> "create app" -> type "web app"
//      (redirect uri can be http://localhost, unused for app-only).
//   2. Set two env vars on the deployment:
//        vercel env add REDDIT_CLIENT_ID
//        vercel env add REDDIT_CLIENT_SECRET
//   3. Redeploy.  No user login needed — app-only reads public posts/comments.
//
// GET /api/reddit?url=<reddit permalink>  ->  { text, author, label }

const UA = "web:noesis-poa-demo:1.0 (by /u/noesis; contribution-pricing prototype)";

// token cache — survives across warm invocations of the same function instance
let _tok = { value: null, exp: 0 };

async function appToken() {
  const id = process.env.REDDIT_CLIENT_ID, secret = process.env.REDDIT_CLIENT_SECRET;
  if (!id || !secret) throw new Error("Reddit not configured — set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET");

  const now = Date.now();
  if (_tok.value && now < _tok.exp - 60000) return _tok.value;

  const auth = Buffer.from(`${id}:${secret}`).toString("base64");
  const r = await fetch("https://www.reddit.com/api/v1/access_token", {
    method: "POST",
    headers: {
      Authorization: "Basic " + auth,
      "Content-Type": "application/x-www-form-urlencoded",
      "User-Agent": UA,
    },
    body: "grant_type=client_credentials",
  });
  if (!r.ok) throw new Error("reddit auth " + r.status);
  const j = await r.json();
  if (!j.access_token) throw new Error("no reddit token");
  _tok = { value: j.access_token, exp: now + (j.expires_in || 3600) * 1000 };
  return _tok.value;
}

export default async function handler(req, res) {
  const raw = req.query.url;
  if (!raw) { res.status(400).json({ error: "url required" }); return; }

  let u;
  try { u = new URL(raw); } catch (_) { res.status(400).json({ error: "bad url" }); return; }
  const host = u.hostname.replace(/^www\./, "");
  if (!(host === "reddit.com" || host === "old.reddit.com" || host.endsWith(".reddit.com"))) {
    res.status(400).json({ error: "not a reddit url" }); return;
  }

  try {
    const token = await appToken();
    const path = u.pathname.replace(/\/$/, "") + ".json";
    const r = await fetch("https://oauth.reddit.com" + path, {
      headers: { Authorization: "bearer " + token, "User-Agent": UA },
    });
    if (!r.ok) { res.status(502).json({ error: "reddit " + r.status }); return; }
    const data = await r.json();

    // Post permalink -> data[0].data.children[0] is the post.
    // Comment permalink -> data[1] holds comments; fall back to the post title + top comment.
    const post = data && data[0] && data[0].data && data[0].data.children && data[0].data.children[0] && data[0].data.children[0].data;
    if (!post) { res.status(404).json({ error: "no post found" }); return; }

    let text = ((post.title || "") + (post.selftext ? "\n\n" + post.selftext : "")).trim();
    let author = post.author || "";

    // If it's a comment permalink, prefer the specific comment's body.
    const comment = data && data[1] && data[1].data && data[1].data.children && data[1].data.children[0] && data[1].data.children[0].data;
    if (comment && comment.body) { text = comment.body.trim(); author = comment.author || author; }

    const label = "r/" + (post.subreddit || "?") + " · " + (post.title || "").slice(0, 48);

    res.setHeader("Cache-Control", "s-maxage=300, stale-while-revalidate=600");
    res.status(200).json({ text, author, label });
  } catch (e) {
    res.status(500).json({ error: String((e && e.message) || e) });
  }
}
