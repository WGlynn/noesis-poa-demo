# Noesis — Proof of Authority you can't buy

**Proof of Authority, except the authority is earned by contribution and cannot be bought.**

Traditional Proof of Authority *appoints* validators — permissioned, centralized, trusted
because someone said so. Noesis *earns* authority: it accrues as soulbound standing from
verified contribution, cannot be bought or transferred, and no amount of capital can finalize
a decision without the contribution dimension's independent consent.

This is a minimal, runnable model of mechanisms already built and tested in the Noesis
reference node (Rust, 300+ passing tests). It exists to answer one question with real code a
skeptic can read and run: **does the core idea actually work?**

## What it demonstrates (the proven steel)

1. **Contribution earns soulbound authority** — you can't buy it or transfer it.
2. **Capital cannot capture finalization** — the anti-concentration floor: a checkpoint
   finalizes only if it independently clears 50% of *both* the capital dimension (stake) and
   the contribution dimension (earned standing). Capital holding every coin still cannot
   finalize without contribution's consent.
3. **Copies and sybil splits earn zero** — re-submitting the same work under 20 identities
   earns nothing, not 20x (strategyproof novelty).

## What it does NOT claim (the honest frontier)

A byte-level novelty proxy catches exact copies and reshuffles, but a **semantic paraphrase**
of the same idea slips through — demo 3 shows this openly. Closing that gap needs a *learned*
value function. That is the open research bet, and its first real-data test came back **null**
(unsupported, not refuted). We show the boundary rather than hide it.

## Run it

```bash
python poa_demo.py        # the reference model, prints all three checks
```

Or open `index.html` in a browser — the same logic ported 1:1 to JavaScript, running live
(view-source is the audit; a Node parity check confirms identical numbers).

## Host it (Vercel)

It's a single static `index.html`, zero build step, zero dependencies:

```bash
vercel deploy             # from this directory; or drag the folder into vercel.com
```

## Provenance

`index.html` (JS) mirrors `poa_demo.py`, which mirrors the mechanisms in the Noesis reference
node. Constants (`THETA_SIM = 0.95` near-duplicate floor; `MIN_DIM = 0.50` anti-concentration
floor) are taken from the node's `ARCHITECTURE.md`. The full hardened implementation, with the
adversarial test suite, is the Rust node — this is its proven core made legible.
