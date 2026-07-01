# PROTOTYPE-SPEC — Graduation 1: the real Noesis core, in the browser (WASM)

**Decided by Will 2026-07-01:** graduate the demo → engineering prototype by compiling the REAL,
built-and-tested Noesis core to `wasm32` and running it in-browser behind the existing UI, replacing
the toy JS. "1 and the real thing." Best started in a FRESH session (this one hit ~606k).

## The one-line goal
The verdicts on https://noesis-poa-demo.vercel.app stop coming from a lookalike JS model and start
coming from the ACTUAL Rust node logic, compiled to WASM. Same beautiful UI, real engine underneath,
on real inputs. Parity-verified against the native Rust so it's provably the same computation.

## Scope (honest boundary — carries up from the demo)
- IN (real, built + tested → make it the engine): the **anti-concentration floor** (`finalizes_pos_pom`
  / `finalizes_pos_pom_fixed`, `MIN_DIM_BPS`, `dim_ok`) and **novelty/strategyproofness**
  (`temporal_novelty`, `pom_scores` / `pom_scores_with_similarity_floor_q16`, `theta_sim`).
- OUT (stays the funded research frontier — do NOT wasm-fake it): the **learned `v(S)`** (value_v8
  Bradley-Terry outcome model). First real-data test null. The prototype proves enforcement is real
  WITHOUT claiming the moat is closed. Keep the "paraphrase slips through" honesty panel.

## Build plan (fresh session)
1. **Audit what compiles.** `~/noesis/onchain/noesis-core` is `no_std` and already targets
   `riscv64imac` (173KB ELF) — the floor mirrors (`finalizes_pos_pom_fixed`, Q32.32) live there and
   should hit `wasm32-unknown-unknown` cleanly. `temporal_novelty` / `pom_scores` live in
   `~/noesis/node/src/lib.rs` (large, likely `std`) — determine whether they extract to a `no_std`
   wasm-friendly slice or need a thin `no_std` shim. Do NOT drag the 6000-line lib into wasm; extract
   the minimal real functions.
2. **wasm build.** `wasm-bindgen` (or `wasm-pack`) exposing two real functions:
   `score(work: &str, corpus: &[String]) -> f64` (real temporal_novelty + theta_sim floor) and
   `finalizes(signers: &[(stake, standing)], totals) -> {pos, pom, ok}` (real floor). Ship the `.wasm`
   + glue into `~/noesis-poa-demo/`.
3. **Wire the UI.** Replace the toy `novelty()` / `finalizes()` in `index.html`'s `<script>` with calls
   to the wasm exports (async init on load). UI/handlers unchanged.
4. **Real inputs.** Swap the toy sentence corpus for a REAL contribution set (e.g., real commit
   messages / paper abstracts / a small OSS slice — pick one, note the source in the UI).
5. **Parity gate (critical — Tom = Runtime Verification).** Same inputs → wasm output == native Rust
   output, bit/tolerance-exact. A test that fails loudly if they diverge. This is the whole credibility.
6. **Deploy** (Vercel, same repo) + let TestDriver (@testdriverai on WGlynn/noesis-poa-demo) drive it.

## Risks / open
- `temporal_novelty`/`pom_scores` may not be cleanly `no_std`-extractable without a small refactor.
  If costly, an acceptable v1 keeps the floor as real-wasm and novelty as a faithful `no_std` port with
  a parity test — still "real core," just note which functions are wasm-native vs ported.
- Q32.32 fixed-point in wasm must match the on-VM fixed-point exactly (that's the point).

## Paths NOT taken
API-over-the-node (needs hosting) — rejected in favor of wasm ("the real thing in the browser", Will).

## Files
- frontend: `~/noesis-poa-demo/index.html` (+ this dir)
- real core: `~/noesis/onchain/noesis-core` (no_std, the floor mirrors)
- real value/novelty source of truth: `~/noesis/node/src/lib.rs` (`temporal_novelty` :89, `pom_scores`
  :162/:182, `finalizes_pos_pom` runtime.rs:608) — read `~/noesis/ARCHITECTURE.md` first, verify file:line.

---

# PROTOTYPE 2 — real contribution examples from Telegram / Reddit / GitHub (Will 2026-07-01)

Goal: stop scoring toy sentences. Let people feed REAL contributions — a GitHub commit/PR/issue, a
Reddit post, a Telegram message — into the demo and see what standing they earn (real novelty + the
real wasm floor). Real inputs are the demo->prototype jump on the DATA axis (pairs with Graduation 1's
real-engine axis). Builds on ~/noesis-poa-demo/ (index.html + noesis_poa.wasm).

## Source feasibility (client-side, since it's a static Vercel site)
- **GitHub — easiest, do first.** `api.github.com` is public + CORS-enabled. Paste a repo/commit/PR/issue
  URL -> fetch via the API -> extract text (commit message, PR title+body, issue body, README) -> score
  through the novelty path. No proxy, no auth for public repos (watch the 60 req/hr unauth rate limit).
- **Reddit — needs a proxy.** `reddit.com/.../<id>.json` exists but is CORS-restricted from the browser.
  Add a tiny Vercel serverless function (`/api/reddit?url=...`) that fetches server-side and returns the
  post/comment text. (Vercel functions are the clean fit; keeps the site static + one endpoint.)
- **Telegram — hardest, defer to paste.** No public read API for arbitrary messages without a bot. v1:
  a paste box ("paste a TG message"), OR later a read-only bot / channel-export importer. Don't block v1 on it.

## v1 shape (pragmatic)
1. An "import a real contribution" box: a URL field (GitHub/Reddit) + a paste field (anything, incl. TG).
2. GitHub URL -> real fetch + extract; Reddit URL -> via the serverless proxy; paste -> direct.
3. Run the extracted text through the novelty scorer (real wasm novelty if the coverage export is done by
   then — see Graduation 1 step (b); else the faithful port), add it to the live record, show earned
   standing + dup/paraphrase behavior ON REAL DATA.
4. Keep the honesty panel: a real paraphrase of real work still slips the byte proxy = the learned-v(S)
   frontier, now demonstrated on real contributions (a stronger, honester story).

## Why it matters (the pitch upgrade)
"Paste your actual GitHub PR / Reddit post and watch the protocol price it" is the moment a skeptic feels
it's real. It also seeds the path to Graduation 2 (learned v(S) on REAL labels) — real contributions are
the corpus that test needs.

## Files / notes
- frontend: `~/noesis-poa-demo/index.html`
- optional proxy: `~/noesis-poa-demo/api/reddit.js` (Vercel serverless) for Reddit CORS
- real novelty export (optional, pairs with this): extend `wasm/` with a `score(work, corpus)` export over
  noesis-core `coverage`/`semantic_floor_q16` (needs string marshaling: alloc + memory export). See G1 step (b).
