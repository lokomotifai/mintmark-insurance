<p align="center">
  <img src="assets/brand/mintmark-logo.svg" width="112" height="112" alt="Mintmark">
</p>

<h1 align="center">Mintmark insurance</h1>

<p align="center"><strong>Turkish policy and claim data, including a health branch that stays a health branch.</strong></p>

<p align="center">
  Policyholders both individual and corporate, policies across the main branches,<br>
  claims with their payment trail, and the free text where personal data hides.
</p>

<p align="center">
  <a href="https://github.com/lokomotifai/mintmark-insurance/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/lokomotifai/mintmark-insurance/ci.yml?branch=main&amp;style=flat-square&amp;label=CI"></a>
  <img alt="Zero engine code" src="https://img.shields.io/badge/engine%20code-none-3C873A?style=flat-square">
  <img alt="18 of 18 coverage targets met" src="https://img.shields.io/badge/coverage%20targets-18%2F18-3C873A?style=flat-square">
  <img alt="No release published" src="https://img.shields.io/badge/release-not%20published-3B3F46?style=flat-square">
  <a href="LICENSE"><img alt="Apache-2.0 license" src="https://img.shields.io/badge/license-Apache--2.0-3B3F46?style=flat-square"></a>
</p>

<p align="center">
  <a href="https://github.com/lokomotifai/mintmark"><img alt="Requires the Mintmark core" src="https://img.shields.io/badge/core-%3E%3D0.1%2C%3C0.2-17191F?style=flat-square"></a>
  <img alt="Six record types" src="https://img.shields.io/badge/record%20types-6-17191F?style=flat-square">
  <img alt="Seven insurance branches" src="https://img.shields.io/badge/branches-7-17191F?style=flat-square">
  <img alt="26 fictional insurer names" src="https://img.shields.io/badge/fictional%20insurers-26-D11F26?style=flat-square">
  <img alt="Health stays at category granularity" src="https://img.shields.io/badge/health-category%20granularity-C98A2B?style=flat-square">
  <a href="README.tr.md"><img alt="Türkçe" src="https://img.shields.io/badge/belgeler-Türkçe-D11F26?style=flat-square"></a>
</p>

<p align="center">
  <a href="#mint-it-yourself"><strong>Mint it yourself</strong></a>
  ·
  <a href="#the-health-boundary"><strong>The health boundary</strong></a>
  ·
  <a href="#two-things-the-taxonomy-decided-for-us"><strong>What the taxonomy decided</strong></a>
  ·
  <a href="README.tr.md"><strong>Türkçe</strong></a>
</p>

---

> **This repository contains no engine code.** It is declarations and data. The
> engine that reads them lives in
> [mintmark](https://github.com/lokomotifai/mintmark) and is pinned here by a
> version range with a closed upper bound.

Turkish insurers, agencies, and insurtech teams hold policy and claim data that
mixes financial, behavioral, and health-adjacent personal data. None of it can
move into a test environment without KVKK exposure. This pack declares that data,
and the engine mints it: deterministic, span-labeled, and sealed by a manifest.

**Version 0.1, pre-release. No release has been published and no reference
dataset exists yet to download.** What is true today: `packcheck` passes against
the pinned core, the test suite passes, and the evaluation recipe meets every one
of its eighteen coverage targets.

> [!IMPORTANT]
> **What this pack is not.** It is not anonymization of your policy data; it
> ingests none. It is not a compliance guarantee and not a legal safe harbor. It
> is **not clinical data and not a substitute for it**: the health branch stays at
> category granularity by design. The anomaly recipe is detector-side test data
> and this repository documents no evasion guidance. Generated phone numbers can
> coincide with assigned ones, because the Turkish numbering plan reserves no
> fictional range. This data is for testing systems. It is never for contacting
> anyone.

## What is in here, and what is not

![Diagram of the insurance pack's record types: policyholder split between individual and corporate, policy across seven branches with an unlabeled plate and no make or model field, claim with claimed and paid amounts and an anomaly kind, and payment by card or transfer. Two document types below in red, claim note and call transcript, each producing a label sidecar. A band across the bottom states the health boundary](assets/readme/record-map.png)

<p align="center"><sub><a href="assets/readme/record-map.svg">View the accessible SVG source</a></sub></p>

| In here | Not in here |
| --- | --- |
| Six record types, two of which are free text | Any engine code. The only Python is under `tests/` |
| Corporate policyholders, which is where tax numbers live in a field | A vehicle make or model field. The brand prohibition covers vehicle brands |
| A health branch at 10 percent of policies | Clinical detail of any kind. See the boundary below |
| 26 invented insurer names, scanned against a real-institution list | Any real insurer. One got in during development and this is how it was caught |

## The health boundary

This pack includes a `saglik` branch at the policy and claim level, because
insurance data has one and a test environment that pretends otherwise is not
representative.

Health mentions stay at **category granularity**: a condition class and nothing
more. No diagnosis, no clinical finding, no treatment, no medication, no
prognosis. When a template feels thin because the detail that would make it read
naturally is forbidden, the template is thin. That is the correct outcome.

Two controls hold the line, not one:

- Every health span draws from the core's curated condition-class descriptors,
  which are written at that granularity and reviewed by hand.
- `lexicons/clinical_denied_tr.txt` lists the vocabulary this pack refuses, and a
  test scans every rendered document against it. Review gets tired; a list does
  not, and the failure mode here is silent because a template that drifts into
  clinical detail still renders, still labels, and still passes every other check.

The health sector pack itself remains deferred in the family roadmap. Its
special-category density needs a stricter governance review before a brief for it
is even written. This pack is not that pack, and both READMEs say so.

## Two things the taxonomy decided for us

Neither is an oversight, and both are the kind of thing a reader will otherwise
assume is a bug.

**Vehicle plates are emitted unlabeled.** The pinned taxonomy has no PLATE label.
Labeling a plate as ADDRESS would corrupt every evaluation this pack's dataset is
used for, and inventing a label outside the closed set fails closed by design. So
the field carries none, and a test asserts that no span in any sidecar covers a
plate. If a later taxonomy version adds the label, this pack takes it in a major
bump.

**There is no vehicle make or model.** The family's brand prohibition covers
vehicle brands, so a vehicle is described by year and body type only. That is a
real modeling loss for anyone testing a rating engine that keys on make, and it
is stated here rather than discovered after ingest.

## Mint it yourself

```bash
uv tool install mintmark
git clone https://github.com/lokomotifai/mintmark-insurance
cd mintmark-insurance

mintmark packcheck .
mintmark mint --pack . --recipe portfolio-baseline --seed 20261001 --out ./run
mintmark verify ./run
```

One claim note, as emitted:

```
Hasar dosyasi notu. Olay yeri Lale Sokak olarak tespit edildi.
Karsi taraf Emre Arslan, iletisim +90 532 088 32 86. Sigortali
21604968396 numarali kisi, odeme icin TR129999906635627157091446
hesabini bildirdi. Arac plakasi eksper tarafindan kayda gecirildi.
Ekspertiz tamamlandi; hasar onarilabilir olarak degerlendirildi.
Dosya tamamlandi olarak guncellendi.
```

That is the first record in [`samples/claim_note.jsonl`](samples/claim_note.jsonl),
not an illustration written for the README. A test compares the two.

## The evaluation set

`pii-eval` declares a coverage target for every label and meets all eighteen. The
corporate policyholder share is what carries the tax number load, which is the
main structural difference from the banking pack: there, every record type is
retail, so VKN has to reach the data through document templates instead.

| Label group | Target | Achieved |
| --- | --- | --- |
| PERSON, ADDRESS, ORG, DOB | 300 each | 2000 each |
| The eight special categories | 300 each | 474 to 519 |
| TCKN, VKN, IBAN, PAN, PHONE, EMAIL | 500 each | 2000 each |

Eight special-category labels at 300 spans each is 2400 injections across 2000
documents, and this pack has only two document types to spread them over where
banking has three. The evaluation templates are therefore a separate family at
rate one with two special slots each, spread evenly across the labels.

## The three recipes

| Recipe | Shape | For |
| --- | --- | --- |
| **portfolio-baseline** | 8 000 policyholders, about 16 000 policies, 2 700 claims, 40 000 payments, and 2 900 documents | Filling a test environment with something that behaves like a book of business |
| **pii-eval** | 2 000 documents, every label above its target | Measuring a detector on Turkish insurance text |
| **anomaly-mix** | The baseline plus a labeled anomaly field on every claim | Scoring a monitoring system against ground truth |

### A limitation of anomaly-mix, stated plainly

Every claim carries `anomaly_kind` and `is_anomaly`, and the two never disagree.
But the four kinds are **per-row labels drawn at declared rates, not genuine
temporal or cross-record structures**. A real duplicate-claim pattern spans
several claims on one policy; here it is a label.

That is a limit of the pack contract rather than an oversight: each field is drawn
from an independent stream, so a pack cannot declare a pattern that correlates
rows. Use this recipe to check that your pipeline carries labels through
correctly. Do not use it to measure whether a detector finds real patterns.

## A real insurer that reached a fictional list

Worth telling, because it is the argument for the denylist rather than a
hypothetical about it.

The core's denylist is built from the payment systems participant register, which
lists banks. It cannot catch a collision with an insurer, and one was sitting in
this pack's fictional lexicon: **Bereket Sigorta, a real company incorporated in
1995**. It got there because "bereket" reads as an ordinary Turkish word for
abundance.

The root turned out to be in three lexicons across two packs and in the core's own
organization descriptors. All were corrected, this pack now carries a denylist
extension of 110 entries covering banks and insurers, and the whole family was
re-scanned against it.

One limitation of that verification is worth stating: the Turkish insurance
association publishes the authoritative member list, and its page renders client
side, so the list used here is a public compilation of 40 companies. That was
enough to catch a real collision. It is not enough to prove there are none, and a
manual read of the association's own page belongs in the release checklist. The
full record is in
[docs/normative-verification.md](docs/normative-verification.md).

## Repository map

```
pack.yaml           identity, the core pin, the allowed identifier policies
fields/             one file per record type, in generation order
recipes/            portfolio-baseline, pii-eval, anomaly-mix
templates/          baseline sets, and the separate evaluation sets
lexicons/           invented insurers and agencies, the denylist, the clinical
                    vocabulary this pack refuses
samples/            fifty records per type, regenerated from a fixed seed
vendor/             the core wheel required CI runs against, recorded by checksum
tests/              the conformance suite, including the health boundary check
docs/               the reference dataset record and the verification record
```

## Develop the repository

```bash
uv sync
uv run mintmark packcheck .
uv run pytest
uv run python tools/mdlint.py .
```

All of it runs offline against the vendored core wheel.

## Project status

Version 0.1, pre-release. No release, no published dataset. The reference
datasets are declared in
[docs/reference-datasets.json](docs/reference-datasets.json) with their settled
seeds; publishing them is an external authorization checkpoint along with
confirming the dataset license.

## Community contract

Contributions under the Developer Certificate of Origin 1.1, no contributor
license agreement. See [CONTRIBUTING.md](CONTRIBUTING.md),
[GOVERNANCE.md](GOVERNANCE.md), and [SECURITY.md](SECURITY.md).

`README.md` is canonical and [README.tr.md](README.tr.md) is a full mirror.

## License and trademark

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE). The license grants no
right to the Mintmark name or logo; see [TRADEMARKS.md](TRADEMARKS.md).

The dataset license for published reference datasets is proposed as CC0-1.0 and
is pending legal confirmation.

<p align="center"><sub>Part of the Mintmark family: <a href="https://github.com/lokomotifai/mintmark">the engine</a> · <a href="https://github.com/lokomotifai/mintmark-banking">banking</a> · <a href="https://github.com/lokomotifai/mintmark-hr">human resources</a></sub></p>
