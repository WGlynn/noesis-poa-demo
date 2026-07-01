# HANDOFF — Noesis "Proof of Authority you can't buy" demo (2026-07-01)

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

## Anti-hallucination note
Noesis numbers were read from `~/noesis/ARCHITECTURE.md` + `docs/WHITEPAPER.md` §9 this session, not
asserted from memory. Consensus mix ≠ finality mix (known trap). Verify file:line before any partner claim.
