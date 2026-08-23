# Engineering notes

Operational know-how for this repository. Committed, unlike the plan.

## The core wheel is bound to an immutable source revision

`pack.yaml` requires Mintmark `>=0.3,<0.4`, while required CI installs the
vendored `mintmark-0.3.0-py3-none-any.whl` whose SHA-256 is recorded in
`vendor/CHECKSUMS`. The separated network workflow checks out core commit
`499216efdc8d30ccb21d4a4a03a38b014b0ca870`, builds it with its locked backend,
and byte-compares that independently sourced wheel with the vendored artifact.
Repository-local checksums establish integrity; the immutable core checkout and
reproducible comparison establish provenance.
## The health boundary is two controls, not one

The `saglik` branch is this pack's sensitive surface. Health mentions stay at
category granularity: a condition class and nothing more.

The first control is where the surface comes from. Every HEALTH span draws from
the core's curated condition-class descriptors, which are written at that
granularity and reviewed by hand. A test asserts that every HEALTH span in a
minted dataset is one of them.

The second is `lexicons/clinical_denied_tr.txt`, scanned against rendered
documents and against the template sources. It exists because review gets tired
and a list does not, and because the failure mode is silent: a template that
drifts into clinical detail still renders, still labels, and still passes every
other check.

When a template feels thin because the detail that would make it read naturally
is forbidden, the template is thin. Do not fix it by adding detail.

## Two constraints the taxonomy imposed

**Plates are unlabeled.** The pinned taxonomy has no PLATE label. A reviewer will
reasonably think a plate is personal data and reach for ADDRESS. That would
corrupt every evaluation this pack's dataset is used for. Two tests hold it: one
on the field declaration, one on the minted sidecars.

**No vehicle make or model field exists.** The brand prohibition covers vehicle
brands. A dedicated Unicode-aware denylist is scanned across field, template,
and lexicon declarations and across baseline and evaluation output; a separate
shape assertion still prevents a make/model field from being introduced under
the obvious names.

If a later taxonomy version adds a plate label, this pack takes it in a major
bump, because it changes the label set of every dataset minted afterwards.

## The corporate share is the VKN surface

Fifteen percent of policyholders are `kurumsal` and carry a tax number in a
field. That is the structural difference from the banking pack, where every
record type is retail and VKN has to reach the data through document templates.

If the corporate share changes, the evaluation recipe's VKN coverage changes with
it. Check the manifest's coverage block after any such change.

## Evaluation twins

`claim_note_eval` and `call_transcript_eval` exist because a recipe selects a
template set through the record type that names it, and the two recipes need
different special-category densities. Each recipe sets the other family's counts
to zero.

This pack has two document types where banking has three, so its evaluation
templates carry the same two special slots each across a smaller surface. The
coverage margins are correspondingly thinner; check them after any template
change rather than assuming.

## The insurer denylist is a compilation, not the register

The authoritative member list is published by the Turkish insurance association,
whose page renders client side and could not be read programmatically. What this
pack scans against is a 40-company public compilation.

It was enough to catch Bereket Sigorta, a real company that had reached the
fictional lexicon. It is not enough to prove there are no others. A manual read
of the association's own page belongs in the release checklist.

## Regenerating the samples

    mintmark mint --pack . --recipe portfolio-baseline --seed 1 \
      --records policyholder=50 --records policy=50 --records claim=50 \
      --records payment=50 --records claim_note=50 --records call_transcript=50 \
      --out ./regenerated

Then copy the JSONL files into `samples/`. The freshness test compares by bytes.

## Why birth dates carry an age window

`birth_date` used to be a plain `datetime_window` draw, which meant every person
in a dataset describing 2026 was also born in 2026. Nothing in the suite caught
it: the field is a valid date, the label is right, the span aligns, the manifest
verifies. It is only wrong to a reader, which is the one check that had not run.

The field now declares `params: {age_years: [18, 90]}`, and the core draws from
the span that would give a person that age at the start of the recipe window. The
parameter is optional and a field that omits it behaves exactly as before, so no
other declaration in the family had to move.

Adopting it moved emitted bytes for a fixed seed, so the samples were regenerated
and the pack version went to 0.1.1. That is the rule this pack already had for
lexicon growth, applied to a declaration change.

## A version bump changes every emitted byte

The pack version is one of the six inputs the engine derives every generation
stream from, alongside the seed, the engine's major version, the pack name, the
recipe name, and the site path. So raising `version` in `pack.yaml` changes every
value in every record for a fixed seed, and the sample freshness test fails until
the samples are regenerated.

That reads like a bug the first time it happens. It is the opposite: version and
content correspond exactly, so two datasets carrying the same pack version cannot
differ, and nobody can quietly change what a version emits. The cost is that a
bump is never free for anyone holding a published manifest, which is the reason
the family treats one as a decision rather than a formality.

The pack digest is a separate thing and does not seed anything. It records which
declarations produced a dataset, so a consumer can tell whether the pack they
hold is the pack it came from. An earlier note here said the version reached the
streams by way of the digest. That was wrong, and worth correcting rather than
quietly deleting: it is the kind of plausible mechanism somebody would go on to
reason from.
