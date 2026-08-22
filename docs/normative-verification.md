# Normative source verification record

Facts this pack depends on that live in public registries rather than in any
document here. The core's own record covers what it verified: the VKN algorithm,
the IBAN bank code, Turkey's permanent UTC+3 status, and the banking denylist.
This file records what the insurance pack added.

## Real Turkish insurers, and a collision that had already happened

**Verified:** 2026-08-22. **Drift risk:** real. Insurers merge, rename, and are
licensed. **Wired into the cadence loop.**

**Why this needed doing, and what it caught.** The core denylist is built from the
payment systems participant register, which lists banks. It cannot catch a
collision with an insurer.

One was already in this pack's fictional lexicon when the check was written:
**Bereket Sigorta**, a real company incorporated in 1995 and acquired by the
Turkish Wealth Fund in 2023. It reached the invented list because "bereket" reads
as an ordinary Turkish word for abundance.

That is the same property the denylist's generic-word rule was written for, in the
opposite direction. The rule stops an ordinary word from firing on ordinary prose.
Nothing stopped an ordinary word from being chosen as an invented brand that
happens to be taken.

The root turned out to be in three lexicons across two packs, and in the core's own
organization descriptors. All were corrected and the family was re-scanned.

**Source.** A public compilation of Turkish insurance, reinsurance, and pension
companies, retrieved 2026-08-22, cross-checked against individual company records
for the entries that mattered. 40 companies.

**Outcome.** `lexicons/denylist_extension.txt` carries 110 entries: the core's
banks plus these insurers. Every fictional name in this pack passes it, and a
test asserts that in required CI.

**A limitation, stated rather than papered over.** The Turkish insurance
association publishes the authoritative member list, and its page renders client
side; it could not be read programmatically. A public compilation of 40 companies
is not the same as the authoritative register. It was enough to catch a real
collision. It is not enough to prove there are none.

**What follows from that.** A manual read of the association's own member page
belongs in the release checklist, before any reference dataset is published. Until
that happens, this pack's claim is "scanned against a 40-company public
compilation", not "scanned against the authoritative register", and the README
says the former.

## Province plate codes

**Verified:** 2026-08-22. **Drift risk:** very low.

The two-digit province code in `lexicons/plates_tr.yaml` is factual reference
data: the standard 01 to 81 assignment, stable since the creation of Duzce in
1999. The letters and digits after it are invented and follow no real
registration series.

Plates are emitted unlabeled, because the pinned taxonomy has no PLATE label. That
is settled in the brief and asserted by two tests: one on the declaration, one on
the minted data.

## Inherited from the core

The VKN check-digit algorithm, the unassigned status of IBAN bank code 99999,
Turkey's permanent UTC+3 status, the reserved documentation domain names, and the
banking institution denylist. All verified in the core repository, with sources
and retrieval dates in its own `docs/normative-verification.md`.

This pack does not re-verify them. It pins a core version range, and the core is
where those facts are checked and re-checked.
