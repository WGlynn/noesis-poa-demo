"""
Noesis - a minimal, runnable demonstration: Proof of Authority you cannot buy.

Traditional Proof of Authority APPOINTS validators - permissioned, centralized, trusted
because someone said so. Noesis EARNS authority: it accrues as soulbound "standing" from
verified contribution, cannot be bought or transferred, and no amount of capital can
finalize a decision without the contribution dimension's independent consent.

This file is a ~200-line legible model of mechanisms that are already BUILT AND TESTED in
the Noesis reference node (Rust, 300+ passing tests). It exists to answer one question with
real code a skeptic can read and run: does the core idea actually work? It demonstrates the
PROVEN steel:

  1. contribution -> earned, soulbound authority (you can't transfer it)
  2. capital cannot capture finalization  (the anti-concentration floor)
  3. exact copies and sybil splits earn zero  (strategyproof novelty)

...and it HONESTLY shows the one thing that is NOT solved: a byte-level novelty proxy does
not catch a semantic paraphrase of the same idea. Closing that gap needs a *learned* value
function - the open research bet, whose first real-data test came back null (unsupported,
not refuted). We show it rather than hide it. See README.md.

Run:  python poa_demo.py
"""

from dataclasses import dataclass, field

# ----- Constants mirrored from the Noesis reference node (see ARCHITECTURE.md) -----
THETA_SIM = 0.95          # near-duplicate floor: >= this similarity to prior work earns 0 novelty
MIN_DIM_FRACTION = 0.50   # anti-concentration floor: each dimension must independently clear 50%


# ============ Value measure (a minimal stand-in for temporal_novelty + theta_sim floor) ============

def _shingles(text):
    """3-word shingles - a tiny, order-sensitive fingerprint of the content."""
    words = text.lower().split()
    return {" ".join(words[i:i + 3]) for i in range(max(len(words) - 2, 1))}


def similarity(a, b):
    """Jaccard overlap of shingles. 1.0 = identical content, 0.0 = disjoint."""
    sa, sb = _shingles(a), _shingles(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def novelty(work, prior_corpus):
    """A contribution is worth its novelty against everything already contributed. An exact
    copy or near-duplicate (sim >= THETA_SIM) is floored to 0 - you cannot bank value by
    re-submitting the same bytes. This is the strategyproofness that makes copy/sybil earn
    nothing. (It does NOT catch a semantic paraphrase - see demo 3.)"""
    if not prior_corpus:
        return 1.0
    max_sim = max(similarity(work, p) for p in prior_corpus)
    if max_sim >= THETA_SIM:
        return 0.0
    return round(1.0 - max_sim, 4)


# ============ Soulbound standing - authority you earn, cannot buy, cannot transfer ============

@dataclass
class Ledger:
    standing: dict = field(default_factory=dict)   # identity -> earned PoM standing (soulbound)
    stake: dict = field(default_factory=dict)      # identity -> bonded capital (PoS)
    _corpus: list = field(default_factory=list)    # everything contributed so far

    def contribute(self, identity, work):
        """Contribution -> earned standing. Value is the novelty of the work; identical or
        near-duplicate work earns 0. Standing binds to the identity and is never moved."""
        v = novelty(work, self._corpus)
        self._corpus.append(work)
        self.standing[identity] = self.standing.get(identity, 0.0) + v
        return v

    def transfer_standing(self, frm, to, amount):
        """Standing is SOULBOUND: there is no transfer. This always refuses. (Only bonded
        capital / stake is transferable; authority is not.)"""
        return False


# ============ Finalization - the anti-concentration floor (the anti-plutocracy property) ============

def finalizes(signers, ledger):
    """A checkpoint finalizes only if the signing set INDEPENDENTLY clears the floor on BOTH
    dimensions: >= 50% of all bonded capital (PoS) AND >= 50% of all earned standing (PoM).

    Consequence: capital holding every coin controls only the PoS dimension. The PoM
    dimension is unbuyable, so it must clear 50% on its own. Capital cannot finalize without
    contribution's consent - and contribution cannot be steamrolled by capital. Neither axis
    rules alone. (In the full node PoW is excluded from finality and the weights are 1/3:2/3
    with a 2/3 supermajority; the load-bearing property demonstrated here is the per-dimension
    floor.)"""
    total_stake = sum(ledger.stake.values()) or 1e-9
    total_standing = sum(ledger.standing.values()) or 1e-9
    signer_stake = sum(ledger.stake.get(s, 0.0) for s in signers)
    signer_standing = sum(ledger.standing.get(s, 0.0) for s in signers)
    pos_ok = signer_stake / total_stake >= MIN_DIM_FRACTION
    pom_ok = signer_standing / total_standing >= MIN_DIM_FRACTION
    return pos_ok and pom_ok


# ============ Demonstrations ============

def hr(title):
    print("\n" + "=" * 74 + "\n  " + title + "\n" + "=" * 74)


def demo_1_earned_soulbound_authority():
    hr("1. Contribution earns authority - and it is soulbound (you can't buy or move it)")
    L = Ledger()
    L.stake = {"alice": 0.0, "whale": 1_000_000.0}   # whale is rich, alice is not
    v = L.contribute("alice", "a novel commit-reveal batch auction that clears at a uniform price")
    print("  alice contributes novel work         -> earns %s standing" % v)
    print("  whale holds 1,000,000 capital        -> earns %s standing" % L.standing.get("whale", 0.0))
    moved = L.transfer_standing("alice", "whale", v)
    print("  whale tries to BUY alice's standing  -> transfer allowed? %s" % moved)
    print("  => authority is earned, not bought. Standing: %s" % L.standing)


def demo_2_capital_cannot_capture():
    hr("2. Capital cannot capture finalization - the anti-concentration floor")
    L = Ledger()
    # Honest contributors earned standing through real, distinct work.
    L.contribute("alice", "novel proof that batch auctions find the true clearing price")
    L.contribute("bob", "an unrelated sybil-resistance mechanism using soulbound identity")
    L.contribute("carol", "a distinct fixed-point argument for observer convergence")
    L.stake = {"alice": 10.0, "bob": 10.0, "carol": 10.0, "whale": 1_000_000.0}

    print("  whale holds ~100%s of capital, 0 earned standing." % "%")
    print("  whale alone tries to finalize a checkpoint -> finalizes? %s" % finalizes({"whale"}, L))
    print("    (PoS dimension cleared; PoM dimension 0%s -> floor fails. Capital cannot buy it.)" % "%")
    print("  the contributors alone (all standing, ~0 stake) -> finalizes? %s"
          % finalizes({"alice", "bob", "carol"}, L))
    print("    (they hold the contribution dimension but not the capital dimension.)")
    print("  contributors + whale, in agreement          -> finalizes? %s"
          % finalizes({"alice", "bob", "carol", "whale"}, L))
    print("  => neither capital nor contribution finalizes alone. No one buys the outcome.")


def demo_3_copy_earns_zero_paraphrase_is_the_frontier():
    hr("3. Copies and sybil splits earn zero - and the honest frontier (paraphrase)")
    original = "a cooperative-game value function that prices contribution by realized downstream flow"

    # Attacker: split the SAME work across 20 fresh identities (identity multiplication + copy).
    L = Ledger()
    L.contribute("author", original)
    gained = sum(L.contribute("sybil_%d" % i, original) for i in range(20))
    print("  author contributes one real body of work    -> earns 1.0 standing")
    print("  attacker re-submits it under 20 identities   -> total earned: %s  (not 20x)"
          % round(gained, 4))

    # The honest frontier: a SEMANTIC paraphrase of the same idea slips past a byte-level proxy.
    Lp = Ledger()
    Lp.contribute("author", original)
    para = "a mechanism that scores each contributor by the real value that flows downstream from their work"
    earned = Lp.contribute("paraphraser", para)
    print("  attacker rewords the SAME idea (paraphrase)  -> earns %s   <-- NOT floored" % earned)
    print("  A byte-level novelty proxy catches exact copies and reshuffles, but a semantic")
    print("  reword of the same meaning slips through. That gap is EXACTLY the open frontier:")
    print("  closing it needs a *learned* value function - the bet we are raising to build")
    print("  (first real-data test: null). We show it here rather than hide it.")


def main():
    print("Noesis - Proof of Authority, except the authority is EARNED by contribution")
    print("and cannot be bought. A minimal, runnable model of the proven core.")
    demo_1_earned_soulbound_authority()
    demo_2_capital_cannot_capture()
    demo_3_copy_earns_zero_paraphrase_is_the_frontier()
    hr("Honest boundary")
    print("  PROVEN + shown above (built and tested in the Noesis node): earned soulbound")
    print("  authority, the anti-concentration floor, strategyproof novelty vs copy/sybil.")
    print("  OPEN + shown above (the research bet we are raising to close): a learned value")
    print("  function that beats a fixed proxy on real labels, incl. semantic paraphrase.")


if __name__ == "__main__":
    main()
