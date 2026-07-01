# HANDOFF — Noesis "Proof of Authority you can't buy" demo (2026-07-01)

> ✅ **SESSION 2026-07-01 PM — design/messaging overhaul + attack-defense doc + v3 spec.** LIVE on
> https://noesis-poa-demo.vercel.app, all pushed to `WGlynn/noesis-poa-demo` (git WGlynn/noreply, no
> Claude trailer). This session's changes on the demo:
> - **Finder's-reward economics (panel 04) + flywheel (panel 06):** Maarten G's third-party-surfacer idea
>   built in — unified native "share" action (Web Share API), 24h value-pool **lottery** (E[lottery]=π·v =
>   same expectation as a fixed cut), soulbound-author vs transferable-finder split, **Shapley-priced =
>   flywheel not dilution**, self-tapering subsidy with an animated flywheel (spinning wheel + orbiting
>   value particles, speed tied to saturation) + a live taper curve. Credited to Maarten G on-page.
> - **Provenance (panel 05):** real ECDSA (P-256) account-link widget (generate identity / sign handle↔key
>   binding / verify — Web Crypto, no key held server-side). Honest-edge rewritten to **structural closure
>   to the Nakamoto bound** (false timestamp can't finalize without a majority of un-buyable soulbound
>   contribution); open frontier correctly relocated to learned `v(S)`, not the timestamp.
> - **Panel 01 presets:** added "whale + 1 contributor" (REJECTED) and "whale + 2 contributors" (FINALIZES)
>   — shows the floor is anti-**capture**, not anti-capital.
> - **Visual layer:** live threshold bars (panel 01), novelty meter (02), catch-p/loss gauges + rising
>   strength-ladder (05), expected-reward bar (04). Shared `meterBar` helper + `.ctl` slider rows (fixed a
>   slider-crush bug under the new font).
> - **Structure/polish (Will-driven, rapid):** **landing gate** — the app is now behind an "enter the
>   interactive demo" page; landing is LIGHT (hero + white/bold thesis paragraph + enter only, fixed
>   non-scrolling viewport via `body.landing`). Panels lead with the interactive; deep prose fans down
>   behind `details.more` **learn-more expanders** (progressive disclosure). Typography: **Space Grotesk**
>   (reading) + **JetBrains Mono** (data/chrome). Removed: soulbound panel (concept lives in 01/04/05),
>   footer prose, live pill, "real core loaded" indicator, finalize-mini, name teaser, "real core ·
>   webassembly" tag, the public **"Tom"** partner name (don't name partners on a public page).
> - Panels renumbered 1–6 (01 floor · 02 novelty · 03 nash · 04 finder's reward · 05 provenance · 06 flywheel).
>
> ✅ **PROTOTYPE v3 SHIPPED — browser testnet (panel 07).** Real ECDSA identity (localStorage-persisted),
> SHA-256 hash-chained blocks, commit-reveal (`commit=hash(content|secret|author)`), novelty-gated
> minting, soulbound standing vs transferable finder tokens (real ECDSA-signed + verified transfers),
> "try to sell standing" → REFUSED, live explorer + reset. Single-node honest boundary stated. Spec:
> `PROTOTYPE-SPEC-V3.md`. ⚠ NEEDS a human **browser click-test** — crypto/localStorage paths built +
> syntax-verified but not exercised in a real browser from here (mine a block, do a transfer).
>
> ▶▶ **NEXT (fresh session recommended): ZK into NOESIS CORE (private repo, not the demo).** Will
> 2026-07-01: "all 4 ZK ideas are good, build them into core." Grounded design doc written:
> `~/noesis/docs/ZK-INTEGRATION.md`. Headline holds under grounding: `noesis-core` is `no_std` + builds
> `riscv64imac` (`onchain/noesis-core/src/lib.rs:1-14`), so a RISC-V zkVM (RISC Zero / SP1) proves the
> exact functions already run (`finalizes_pos_pom_fixed`:481, `coverage`:88, `semantic_floor_q16`:67) —
> no circuit rewrite. Build order: (1) RISC Zero PoC proving `finalizes_pos_pom_fixed` ← START HERE,
> (2) private-input scoring proof (zkML), (3) Noir Merkle non-membership novelty, (4) account-link
> selective disclosure. All 🟡 designed / 🔬 unbuilt. Recommended as its own focused session (real
> Rust zkVM + Noir work; deferred out of this ~573k-context session).
>
> ▶ **Attack/defense (partner material):** `~/noesis/docs/ATTACK-DEFENSE.md` (PRIVATE repo) — Will
> stress-tested the design 4 ways this session (key-sale, reuse-inflation, incumbency, "are we sure about
> soulbound") and it strengthened under scrutiny; each attack bottoms out at the Nakamoto bound. Grounded
> to `lib.rs`/`TOKENOMICS.md` file:lines (retention/`effective_weight`:3507/3516, `Op::Decay`:462-473/488,
> symmetric franchise-decay:3469-3525, soulbound rationale TOKENOMICS:25-27/113-119). Franfran reply draft:
> `~/Desktop/franfran-contribution-sybil-2026-07-01.md`. NOT yet committed to the private repo (Will's call).
> Two open follow-ups: commit ATTACK-DEFENSE.md to private repo · condense the attack/defense pairs into
> public demo expanders (no private file:lines).
>
> Memory captured this session: `primitive_provenance-gap-is-airgap-instance`, `primitive_finder-reward-shapley-flywheel`.

> ✅ **PROTOTYPE 2 SHIPPED (2026-07-01): feed REAL contributions in + tabbed nav.** LIVE on
> https://noesis-poa-demo.vercel.app. Panel 02 now has an "import a real one" box:
> - **GitHub — live now, zero infra.** Paste a commit / PR / issue / repo URL → fetched from the public
>   CORS API (`api.github.com`), text extracted, scored through the real novelty path. Verified
>   end-to-end (ethereum/EIPs#3 → @wanderer). Client fns `importURL`/`fetchGitHub`/`ghApi` in index.html.
> - **Reddit — OAuth proxy built (`api/reddit.js`), waits on creds.** Reddit 403s unauthenticated `.json`
>   from datacenter IPs, so I built an app-only (`client_credentials`) token-mint + cache proxy. **Will-gated
>   one-time step:** create a Reddit app (reddit.com/prefs/apps → "web app") then
>   `vercel env add REDDIT_CLIENT_ID` + `REDDIT_CLIENT_SECRET` + redeploy. Until then it returns a clean
>   "Reddit not configured" (no crash). Portable by design — **lift `api/reddit.js` + the 2 env vars to Boris.**
> - **X / Telegram / anything else — paste.** The text box scores words regardless of platform.
> - **Soulbound attribution (answers Maarten's "share anything even if not yours"):** importing someone
>   else's PR binds standing to the ORIGINAL author (`@login` from the API), labels you the third-party
>   surfacer. Sharing another's work prices THEIR contribution, not yours — reinforces panel 03.
> - **Navigation:** single long scroll → sticky tab nav (01 floor / 02 novelty / 03 soulbound / 04 nash),
>   one panel at a time, `#1`–`#4` hash-routable, mobile-scrollable. Fn `show(n)`.
>
> ▶ **OPEN for Prototype 2:** (a) Will creates the Reddit app + sets the 2 env vars → Reddit goes live.
> (b) Maarten's idea: a **finder's/curation reward** for the third-party surfacer (separate incentive from
> the author's soulbound standing) — design note, not built. (c) real novelty wasm export still pending
> (still the faithful JS port; see Graduation 1 note below).

> ✅ **GRADUATION 1 DONE (2026-07-01): the real Noesis core runs in the browser.** The finalize verdict
> now comes from `noesis-core::finalizes_pos_pom_fixed` compiled to wasm32 (`wasm/` crate → `noesis_poa.wasm`,
> 5KB), wired into `index.html`, Node-parity-verified (whale-alone REJECTED, everyone FINALIZES). Full neon
> restyle (sleek retro-futurist). LIVE + verified: page 200, wasm served `application/wasm` 200. Repo public
> `WGlynn/noesis-poa-demo` (wasm/target gitignored). Novelty still a faithful JS port (labeled); learned v(S)
> still the openly-shown frontier.
>
> ✅ **PANEL 04 — Nash equilibrium (2026-07-01, HL's question, visual):** payoff table (honest EARN /
> impersonate 0 / lie LOSE / pad 0 / sybil <=0 => honest = unique best response = Nash eq) + interactive
> honest-report IC calc (expected payoff of lying = (1-p)*g - p*b, live sliders). Honest scope: demonstrated
> unilateral + cyclic (nash_honesty); symmetric-lie ring + adaptive/learned-v(S) named as frontier. Grounds
> in `~/noesis/internal/thesis/DESIGN-wills-equilibrium.md` (HCE M1). LIVE + verified.
> NOTE: HL | CKBased.bit = the "friend" who asked the impersonation Q; CKB-tuned text answer given in-chat
> (soulbound = type_script.args, ownership = lock.args); Gmail draft r2062801939364981661 has the generic version.
>
> ▶▶ **TOP PRIORITY NEXT SESSION (Will 2026-07-01): PROTOTYPE 2** — let people feed REAL contribution
> examples from Telegram / Reddit / GitHub into the demo and see what standing they earn. Full spec:
> `PROTOTYPE-SPEC.md` § "PROTOTYPE 2" (GitHub-import first = CORS-friendly public API; Reddit via a tiny
> Vercel serverless proxy; Telegram = paste for v1). This is the demo→prototype jump on the DATA axis.
>
> ▶ **also open (lower):** (a) install @testdriverai on the repo → verify in-browser render+clicks. (b) real
> novelty wasm export (`coverage`/`semantic_floor_q16`, needs string marshaling) — pairs with Prototype 2.
> (c) Graduation 2 (funded research bet): learned v(S) beats a fixed proxy on real labels (first test null).
> (d) share the prototype with Pragma.
>
> BUILD NOTES: wasm crate is `no_std` cdylib, bump allocator + panic handler, flat C-ABI (`floor_finalizes`,
> f64 args + u32 mask/threshold, no wasm-bindgen). Toolchain: rustup + `wasm32-unknown-unknown` target
> installed this session; `cargo build --target wasm32-unknown-unknown --release`.

## Why this exists (the strategic context)
Live Pragma/OPH conversation (TG), 2026-07-01. Bernhard called Noesis "too complex" — an
invitation to improve, not a rejection. Then it escalated into an opportunity:
- **Bernhard**: "Proof-of-mind sounds crazy enough to be a Pragma project... fits with anti-gravity,
  fusion, optical compute. I love the idea." (portfolio-absorption offer forming)
- **Tom Lindeman**: must **show it works with real code, not paper, before anyone funds it**; everyone
  on a shoestring; Pragma OS on ice over AI costs. Asked for "a super basic prototype with real code."
- **Will**: "I can try that today." This demo is that prototype.

## The strategic resolution (decided with Will, partner discussion)
Three-bucket sort of Noesis's complexity:
1. **Invention** (fundable, one sentence): endogenous, un-gameable contribution measurement with no
   oracle — `v(S)`: temporal_novelty -> pom_scores -> value_v5..v8. + HCE.
2. **Essential enforcement** (the steel that looks like straw): the **anti-concentration floor**
   (`MIN_DIM_BPS`/`dim_ok`) + PoM-coupled finality = "capital can't finalize without contribution's
   consent." This is a **decision-rule** property -> portable to a DAO/contract; does NOT need a base L1.
3. **Accidental packaging** (burn): own L1 consensus, PoW, **JUL money layer** (JUL = #1 burn: designed-
   not-built, excluded from finality, pure "new-chain money").

**Spine (Will's crystallization, use everywhere): "PoM = decentralized Proof of Authority — authority
EARNED by contribution, soulbound, un-buyable."** This is the legibility answer to "too complex" AND
slots into Tom's "trusted not trustless economy" framework as the decentralized authority layer.

**Interim vs long-run (Will's call):** sovereignty is load-bearing LONG-RUN, not interim. Ship interim
as a **DAO/module** that carries the **PoM∧PoS floor** (NOT a plain token-vote DAO = the plutocracy we
dissolve). v(S) computes off-chain + posts an attestation -> natural **Pragma-Registry composition**
(Pragma certifies value, DAO enforces floor). Multi-chain reach, no token-sours-retail risk, fundable.

## What was built (this folder, ~/noesis-poa-demo/)
- `poa_demo.py` — reference model, runs clean (`python poa_demo.py`). 3 checks: earned soulbound
  authority · anti-concentration floor (capital can't finalize alone) · copies/sybil earn 0.
- `index.html` — super-minimal Vercel-ready frontend; same logic ported 1:1 to JS, auto-runs in browser.
  **Node parity check confirmed identical numbers to the Python.**
- `README.md` — spine, proven-vs-frontier, run + deploy.
- Constants from `~/noesis/ARCHITECTURE.md`: THETA_SIM=0.95, MIN_DIM=0.50.

## Honest boundary (load-bearing — do NOT overclaim to Pragma)
Demo proves the **built steel** (floor + soulbound authority + strategyproof-vs-copy/sybil). Demo 3
**openly shows** semantic paraphrase earning full novelty (NOT floored) = the open frontier. The learned
`v(S)` moat's first real-data test came back **null (unsupported, not refuted)**. Frame: proven steel =
the demo; learned v(S) = the funded research bet. Under-claim, over-deliver (audience predicted LayerZero 37h early).

## Open / next steps (Will-gated)
1. **Deploy** to Vercel (`cd ~/noesis-poa-demo && vercel deploy`) — NOT done; public URL of Noesis
   material = Will's stealth/exposure call.
2. **Share** the running prototype with Pragma (the "prove it works" artifact Tom asked for). Will delivers.
3. **The fire-doc** (Will committed: "make a doc... throw it through the fire, straw burns, steel remains"):
   formalize the three-bucket sort with keep/burn/defer verdicts per component. NOT yet written.
4. Friend's PoM/impersonation question answered -> Gmail draft `r2062801939364981661` (re-address before send).
5. Demo-link share email -> Gmail draft `r6563721717327864407` ("running prototype not a slide"; re-address before send).
6. Deployed LIVE + public (200, no auth wall): https://noesis-poa-demo.vercel.app (Vercel, tiptaptangsun-8775 acct). Fable 5 NOT available for this account yet (checked 2026-07-01).
7. DEMO IS NOW INTERACTIVE (Will: "static doesn't show what happens when variables change"): edit stake/standing + toggle signers -> live finalize verdict; type-your-own novelty box (paste=0, reword=frontier); soulbound "try to buy"=REFUSED. Logic Node-parity-verified vs poa_demo.py.
8. Design polished testdriver-grade (Will shared testdriver.ai, wanted "both" tool+look): gradient hero, NOESIS wordmark, step-labels, dark kept (stronger for Pragma vs their light-SaaS). NOTE: built from testdriver's TEXT description, not pixels -> Will may want lighter/closer, iterate.
9. Mobile fix: "Signs?" column overflow -> table scroll-wrap + max-width:560px breakpoint (shrunk inputs, trimmed headers).
10. **GitHub repo now PUBLIC: https://github.com/WGlynn/noesis-poa-demo** (git identity WGlynn/noreply, NO Claude trailer). For **TestDriver.ai** (AI UI-testing GitHub App Will wants on the demo): Will installs @testdriverai app + mentions @testdriverai in repo -> writes UI tests. Will-gated (account/install). Then Jarvis helps write test prompts.

## Anti-hallucination note
Noesis numbers were read from `~/noesis/ARCHITECTURE.md` + `docs/WHITEPAPER.md` §9 this session, not
asserted from memory. Consensus mix ≠ finality mix (known trap). Verify file:line before any partner claim.
