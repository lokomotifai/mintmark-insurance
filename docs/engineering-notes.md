# Engineering notes

Operational know-how for this repository. Committed, unlike the plan.

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
brands. A test asserts no field is named for one.

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
