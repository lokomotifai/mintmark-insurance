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
  <img alt="Release v0.2.0" src="https://img.shields.io/badge/release-v0.2.0-8A6412?style=flat-square">
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

**Version 0.2.0, prepared and not tagged yet. Its reference datasets are minted
from these declarations and attached to
v0.2.0 when the tag
is cut, each carrying its own manifest and checksums.** What is true today: `packcheck` passes against
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
> What this does and does not mean under Turkish data protection law is set
> out in [docs/kvkk.md](docs/kvkk.md).

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
Hasar dosyasi notu. Olay yeri Guzelyali Mahallesi olarak tespit
edildi. Karsi taraf Zehra Kara, iletisim +90 559 641 52 09.
Sigortali 28340880705 numarali kisi, odeme icin
TR499999900496483948306278 hesabini bildirdi. Arac plakasi eksper
tarafindan kayda gecirildi. Bildirilen hasar turu elektrik
kontagi. Ekspertiz tamamlandi; hasar kismi olarak degerlendirildi.
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
| PERSON, ADDRESS, ORG, DOB | 300 each | 1206 to 2000 |
| The eight special categories | 300 each | 462 to 545 |
| TCKN, VKN, IBAN, PAN, PHONE, EMAIL | 500 each | 811 to 2000 |

Eight special-category labels at 300 spans each is 2400 injections across 2000
documents, and this pack has only two document types to spread them over where
banking has three. The evaluation templates are therefore a separate family at
rate one with two special slots each, spread evenly across the labels.

### What a document does not tell you about its record

An identifier inside a document body is a fresh draw. `{id:TCKN}`, `{id:IBAN}`,
`{id:PHONE}` and the person `{entity:PERSON}` names are drawn independently of the
record the document is attached to, so a document linked to `PLH-00000123` names
somebody else and cites a national identity number no policyholder row carries. The
spans are still right: each one points at the surface it labels, and a detector
scored on them is scored correctly.

What this rules out is anything that needs the two sides to agree. Checking that a
redaction pipeline gives one person the same pseudonym in a table and in prose, or
that a control catches a document citing an identifier its master record does not
hold, cannot be done with this data. It is stated here for the same reason the
other structural losses are: it is invisible until somebody joins on it.

## The two recipes

| Recipe | Shape | For |
| --- | --- | --- |
| **portfolio-baseline** | 8 000 policyholders, about 16 000 policies, 2 700 claims, 40 000 payments, and 2 900 documents | Filling a test environment with something that behaves like a book of business |
| **pii-eval** | 2 000 documents, every label above its target | Measuring a detector on Turkish insurance text |

### A limitation of the anomaly fields, stated plainly

Every claim carries `anomaly_kind` and `is_anomaly`, and the two never disagree.
But the four kinds are **per-row labels drawn at declared rates, not genuine
temporal or cross-record structures**. A real duplicate-claim pattern spans
several claims on one policy; here it is a label.

That is a limit of the pack contract rather than an oversight: each field is drawn
from an independent stream, so a pack cannot declare a pattern that correlates
rows. Use these fields to check that your pipeline carries labels through
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
recipes/            portfolio-baseline, pii-eval
templates/          baseline sets, and the separate evaluation sets
lexicons/           invented insurers and agencies, the denylist, the clinical
                    vocabulary this pack refuses
samples/            fifty records per type, regenerated from a fixed seed
vendor/             the core wheel required CI runs against, recorded by checksum
tests/              the conformance suite, including the health boundary check
docs/               the reference dataset record, the verification record, and
                    what this pack does and does not claim under KVKK
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

Version 0.2.0 is under development. The latest published reference datasets remain attached to
[v0.1.2](https://github.com/lokomotifai/mintmark-insurance/releases/tag/v0.1.2). This version moves emitted bytes for a fixed seed,
which this project family calls a major version event: the core began honouring
template weights, and both the core and this pack widened the surface vocabularies
a document draws from. The reference datasets attached to v0.1.2 stay valid and
stay reproducible, with the core and pack versions their own manifests record. New
ones are minted from these declarations at the seeds in
[docs/reference-datasets.json](docs/reference-datasets.json) when the tag is cut.
The engine is on PyPI as [`mintmark`](https://pypi.org/project/mintmark/). The
weekly pin check rebuilds the vendored wheel from its immutable audited source
revision and requires an exact byte match.

## Community contract

Contributions under the Developer Certificate of Origin 1.1, no contributor
license agreement. See [CONTRIBUTING.md](CONTRIBUTING.md),
[GOVERNANCE.md](GOVERNANCE.md), and [SECURITY.md](SECURITY.md).

`README.md` is canonical and [README.tr.md](README.tr.md) is a full mirror.

## License and trademark

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE). The license grants no
right to the Mintmark name or logo; see [TRADEMARKS.md](TRADEMARKS.md).

Reference datasets are licensed **CC BY 4.0**: use them for anything, including
commercially, and credit the source. Every dataset carries its own credit line in
`MINTMARK.json` and `mintmark verify` prints it, so nothing has to be assembled by
hand. See [LICENSE-DATASETS.md](LICENSE-DATASETS.md). Pending legal confirmation;
nothing here states it as settled.

<p align="center"><sub>Part of the Mintmark family: <a href="https://github.com/lokomotifai/mintmark">the engine</a> · <a href="https://github.com/lokomotifai/mintmark-banking">banking</a> · <a href="https://github.com/lokomotifai/mintmark-hr">human resources</a></sub></p>
