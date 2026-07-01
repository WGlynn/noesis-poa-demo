# PROTOTYPE v3 — the browser testnet

**Decided by Will 2026-07-01:** option (1), a self-contained browser testnet. Real cryptography in the
page, no private-core exposure, ships on the same public Vercel site.

## The one-line goal
The demo stops being six illustrative panels and becomes a tiny **real ledger you can transact on** —
real keypairs, real commit-reveal blocks, real soulbound standing + transferable finder tokens, real
novelty + the real wasm floor — all in-browser, verifiable via view-source, state persisted locally.

## Real vs. illustrative (honest boundary — carries up)
- **REAL:** ECDSA P-256 identities + signatures (already built), SHA-256 content hashing, a hash-chained
  block loop (each block commits the prev hash), commit-reveal, **soulbound** standing (ledger entries
  keyed to pubkey with *no transfer function*), **transferable** finder tokens (transfer requires a
  signature), novelty via the faithful port / wasm export, finalization via the **real `noesis-core` wasm
  floor** over the current signer set.
- **ILLUSTRATIVE:** single browser instance = one node (multi-validator network is *simulated*, not
  networked); the learned `v(S)` stays the open frontier (novelty is still the byte proxy); no PoW / JUL.
  A single-node testnet demonstrates the *protocol*, not a live decentralized network — state that plainly.

## Components
1. **Ledger** (localStorage-persisted JSON): `blocks[]`, `standing{pubkey→amount}` (soulbound),
   `tokens{pubkey→balance}` (transferable), `corpus[]` (committed contributions: contentHash, author,
   blockHeight, revealed text).
2. **Identity** — reuse the panel-06 ECDSA widget: generate/import keypair, "you are noe1…", persisted
   (testnet key, clearly no real value).
3. **Commit-reveal** — `commit = SHA-256(content ‖ secret ‖ pubkey)` posted first; then reveal
   `content + secret` → validate hash → score novelty → mine a block → mint standing to the author
   (soulbound); if surfaced by a different key, mint a finder token to the surfacer.
4. **Block** — `{ height, prevHash, txs[], logicalTime, signerSet, verdict }`, hash-chained. The block
   height + hash **is** the native provenance timestamp (ties panel 05).
5. **Tokens** — standing: soulbound (no `transfer`). finder-cut: `transfer(to, amt, sig)` — verified with
   Web Crypto against the sender's pubkey.
6. **Explorer** — live view: blocks, standing leaderboard, token balances, the corpus with provenance.
   "reset testnet" clears localStorage.

## UI shape
A new **07 · testnet** panel (or a distinct entry): your identity · submit a contribution
(commit → reveal → mined, standing minted) · surface someone's (finder token) · an explorer of
blocks / balances / provenance. Parity note in-UI: the floor + novelty are the *same real functions* the
other panels run.

## Build order
1. Ledger module (state + localStorage + hash-chain helpers).
2. Commit-reveal + block finalize (reuse the wasm floor + novelty port).
3. Token accounting (soulbound vs. transferable, signed transfers via Web Crypto verify).
4. Explorer UI + reset.
5. Wire to the existing identity widget; cross-link from panels 04/05.
6. Parity check: same inputs → testnet finalize == the panel-01 wasm verdict.

## Risks / open
- Key handling: testnet private key in localStorage is fine for a demo (no real value); label it loudly.
- The "single node" honesty line must be visible so a rigorous reader (Pragma) doesn't read it as a
  live network.
- Keep the learned-`v(S)` frontier panel — the testnet makes enforcement real without claiming the moat.

## Paths not taken
Real-node testnet (option 2) — exposes the private core; deferred to Will's post-head-start call.
