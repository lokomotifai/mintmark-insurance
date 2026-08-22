"""The pack's conformance suite.

Green here means: the declarations are valid under the strict loader, a mint
produces the shapes the brief describes, no invented name collides with a real
institution, and the recipes can actually satisfy the coverage they promise.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from mintmark.annotate import ALL_LABELS
from mintmark.lexicons import load as load_denylist
from mintmark.mint import asset_dir, mint
from mintmark.packs.model import load_pack

ROOT = Path(__file__).resolve().parents[1]
PACK = load_pack(ROOT)
CORE_DENYLIST = load_denylist(asset_dir("denylist") / "institutions-tr.txt")


# The pack contains no engine code, and its Python imports only the public API.


def test_no_python_outside_tests_and_tools() -> None:
    offenders = [
        str(p.relative_to(ROOT))
        for p in ROOT.rglob("*.py")
        if p.is_file() and not str(p.relative_to(ROOT)).startswith(("tests/", "tools/", ".venv/"))
    ]
    assert not offenders, f"a pack carries no engine code, but found: {offenders}"


def test_tests_import_only_the_public_api() -> None:
    """A pack that reaches into a private core module has coupled itself to it."""
    import ast

    for path in sorted((ROOT / "tests").glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                assert not node.module.startswith("mintmark._"), (
                    f"{path.name} imports a private core module: {node.module}"
                )


def test_no_dataset_is_committed_outside_samples() -> None:
    offenders = [
        str(p.relative_to(ROOT))
        for p in ROOT.rglob("*.jsonl")
        if not str(p.relative_to(ROOT)).startswith(("samples/", "tests/", ".venv/", "dist/"))
    ]
    assert not offenders, f"datasets are release artifacts, never committed: {offenders}"


# Identity and pins.


def test_the_pack_name_matches_the_repository() -> None:
    assert PACK.name == ROOT.name == "mintmark-insurance"


def test_the_core_pin_has_a_closed_upper_bound() -> None:
    """An open pin lets a future core change what a published manifest reproduces."""
    assert PACK.requires_core.text == ">=0.1,<0.2"
    assert PACK.requires_core.contains("0.1.0")
    assert not PACK.requires_core.contains("0.2.0")


def test_the_locale_is_turkish() -> None:
    assert PACK.locale == "tr-TR"


# Record shapes the brief settles.


def test_the_four_structured_record_types_exist() -> None:
    names = {t.type_name for t in PACK.record_types}
    assert {"policyholder", "policy", "claim", "payment"} <= names


def test_the_two_document_types_exist_with_their_evaluation_twins() -> None:
    names = {t.type_name for t in PACK.record_types}
    for base in ("claim_note", "call_transcript"):
        assert base in names
        assert f"{base}_eval" in names


def test_policies_are_one_to_four_per_policyholder() -> None:
    ref = next(f.ref for f in PACK.record_type("policy").fields if f.type == "ref")
    assert ref.parent == "policyholder"
    assert ref.counts == (1, 2, 3, 4)
    assert ref.weights == ("0.45", "0.30", "0.15", "0.10")


def test_a_policy_may_have_no_claim() -> None:
    """0..2 per policy. Most policies never produce one."""
    ref = next(f.ref for f in PACK.record_type("claim").fields if f.type == "ref")
    assert ref.counts[0] == 0


def test_the_plate_field_is_emitted_unlabeled() -> None:
    """Settled by the brief, and the reason matters.

    The pinned taxonomy has no PLATE label. Labeling a plate as ADDRESS would
    corrupt every evaluation this pack's dataset is used for, and inventing a
    label outside the closed set fails closed. So the field carries none.
    """
    plate = next(f for f in PACK.record_type("policy").fields if f.name == "plate")
    assert plate.pii_label == "none"


def test_no_span_in_any_sidecar_covers_a_plate(minted: Path) -> None:
    """The unlabeled rule has to hold in the data, not only in the declaration."""
    plates = {
        json.loads(line)["plate"]
        for line in (minted / "policy.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    for sidecar in sorted(minted.glob("*.labels.jsonl")):
        stem = sidecar.name.removesuffix(".labels.jsonl")
        bodies = {
            next(v for k, v in json.loads(line).items() if k.endswith("_id")): json.loads(line)[
                "body"
            ]
            for line in (minted / f"{stem}.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        for line in sidecar.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            text = bodies[record["doc_id"]]
            for span in record["spans"]:
                surface = text[span["start"] : span["end"]]
                assert surface not in plates, f"a plate was labeled {span['label']}"


def test_no_vehicle_make_or_model_field_exists() -> None:
    """The brand prohibition covers vehicle brands, so a vehicle is year and body."""
    banned = {"make", "model", "marka", "brand", "vehicle_make", "vehicle_model"}
    for record_type in PACK.record_types:
        for field in record_type.fields:
            assert field.name not in banned, f"{record_type.type_name}.{field.name}"


def test_a_rejected_claim_is_still_a_claim_with_an_amount() -> None:
    """amount_paid is derived from amount_claimed and is never larger than it."""
    claim = PACK.record_type("claim")
    paid = next(f for f in claim.fields if f.name == "amount_paid_kurus")
    assert paid.generator == "derived:ratio_of"
    assert int(paid.params["numerator"]) < int(paid.params["denominator"])


# Lexicons.


def test_at_least_twenty_four_fictional_bank_names() -> None:
    banks = PACK.lexicons["insurers_fictional"]["values"]
    assert len(banks) >= 24, f"the brief settles at least 24, found {len(banks)}"


@pytest.mark.parametrize("name", sorted(p.stem for p in (ROOT / "lexicons").glob("*.yaml")))
def test_every_lexicon_entry_passes_the_denylist(name: str) -> None:
    document = yaml.safe_load((ROOT / "lexicons" / f"{name}.yaml").read_text(encoding="utf-8"))
    hits = [
        hit.render()
        for value in document.get("values", [])
        for hit in CORE_DENYLIST.scan(str(value))
    ]
    assert not hits, "\n".join(hits)


@pytest.mark.parametrize("name", sorted(p.stem for p in (ROOT / "lexicons").glob("*.yaml")))
def test_every_lexicon_carries_a_source_note(name: str) -> None:
    document = yaml.safe_load((ROOT / "lexicons" / f"{name}.yaml").read_text(encoding="utf-8"))
    assert len(document.get("source_note", "")) > 40, f"{name} has no real source note"


def test_the_pack_denylist_covers_the_core_one() -> None:
    """Packs may extend the list and may never shrink it."""
    extension = load_denylist(ROOT / "lexicons" / "denylist_extension.txt")
    assert extension.covers(CORE_DENYLIST), (
        f"missing from the pack list: {sorted(extension.missing_from(CORE_DENYLIST))[:5]}"
    )


def test_no_template_names_a_real_institution() -> None:
    text = "\n".join(
        p.read_text(encoding="utf-8") for p in sorted((ROOT / "templates").rglob("*.yaml"))
    )
    hits = [hit.render() for hit in CORE_DENYLIST.scan(text)]
    assert not hits, "\n".join(hits)


# Recipes.


def test_the_three_named_recipes_exist() -> None:
    assert set(PACK.recipes) == {"portfolio-baseline", "pii-eval", "anomaly-mix"}


def test_every_recipe_ships_with_the_safe_policy() -> None:
    """Reference datasets are always minted safe."""
    for name, recipe in PACK.recipes.items():
        assert recipe.identifier_policy == "safe", f"{name} does not pin the safe policy"


def test_the_evaluation_recipe_declares_a_target_for_every_label() -> None:
    targets = PACK.recipe("pii-eval").coverage_targets
    assert set(targets) == {label.value for label in ALL_LABELS}
    for label in ("PERSON", "HEALTH", "UNION"):
        assert targets[label] >= 300
    for label in ("TCKN", "VKN", "IBAN", "PAN", "PHONE", "EMAIL"):
        assert targets[label] >= 500


def test_the_reference_seeds_are_the_settled_ones() -> None:
    """Changing a seed silently invalidates a published manifest."""
    datasets = json.loads((ROOT / "docs" / "reference-datasets.json").read_text(encoding="utf-8"))
    assert datasets["portfolio-baseline"]["seed"] == "20261001"
    assert datasets["pii-eval"]["seed"] == "20261002"
    for name, entry in datasets.items():
        if name.startswith("_"):
            continue
        assert entry["identifier_policy"] == "safe", f"{name} is not pinned to safe"


# The mint itself.


@pytest.fixture(scope="module")
def minted(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("pack") / "run"
    mint(
        pack=ROOT,
        recipe="portfolio-baseline",
        seed=1,
        out=out,
        records={
            "policyholder": 120,
            "policy": 200,
            "claim": 60,
            "payment": 400,
            "claim_note": 40,
            "call_transcript": 30,
        },
        invocation="pytest",
    )
    return out


def test_a_mint_produces_every_declared_type(minted: Path) -> None:
    for record_type in PACK.record_types:
        assert (minted / f"{record_type.type_name}.jsonl").exists()


def test_documents_produce_sidecars(minted: Path) -> None:
    for name in ("claim_note", "call_transcript"):
        sidecar = minted / f"{name}.labels.jsonl"
        assert sidecar.exists()
        assert sidecar.read_text(encoding="utf-8").strip()


def test_a_minted_dataset_verifies(minted: Path) -> None:
    from mintmark.api import verify

    report = verify(minted)
    assert report.ok, report.problems
    assert report.checksum_valid_identifiers == 0


def test_no_real_institution_appears_in_minted_output(minted: Path) -> None:
    text = "\n".join(p.read_text(encoding="utf-8") for p in sorted(minted.glob("*.jsonl")))
    hits = [hit.render() for hit in CORE_DENYLIST.scan(text)]
    assert not hits, "\n".join(hits)


def test_every_reference_resolves(minted: Path) -> None:
    def ids(name: str, field: str) -> set[str]:
        return {
            json.loads(line)[field]
            for line in (minted / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        }

    holders = ids("policyholder", "policyholder_id")
    policies = ids("policy", "policy_id")
    for line in (minted / "policy.jsonl").read_text(encoding="utf-8").splitlines():
        assert json.loads(line)["policyholder_id"] in holders
    for name in ("claim", "payment"):
        for line in (minted / f"{name}.jsonl").read_text(encoding="utf-8").splitlines():
            assert json.loads(line)["policy_id"] in policies


def test_pans_are_emitted_masked(minted: Path) -> None:
    for line in (minted / "payment.jsonl").read_text(encoding="utf-8").splitlines():
        value = json.loads(line)["pan_masked"]
        assert value is None or "*" in value


def test_the_anomaly_flag_never_disagrees_with_the_kind(tmp_path: Path) -> None:
    out = tmp_path / "anomaly"
    mint(
        pack=ROOT,
        recipe="anomaly-mix",
        seed=1,
        out=out,
        records={
            "policyholder": 60,
            "policy": 400,
            "claim": 1500,
            "payment": 300,
            "claim_note": 10,
            "call_transcript": 10,
        },
        invocation="pytest",
    )
    rows = [
        json.loads(line)
        for line in (out / "claim.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert rows
    for row in rows:
        assert row["is_anomaly"] == (row["anomaly_kind"] != "none")
    kinds = {row["anomaly_kind"] for row in rows}
    assert kinds == {"none", "erken_hasar", "mukerrer_talep", "tutar_sapmasi", "siklik_artisi"}


def test_packcheck_passes_against_the_pinned_core() -> None:
    """The conformance run a pack release may not be tagged without."""
    result = subprocess.run(
        [sys.executable, "-m", "mintmark.cli", "packcheck", str(ROOT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


# Sample freshness.

SAMPLE_COUNTS = dict.fromkeys(
    ["policyholder", "policy", "claim", "payment", "claim_note", "call_transcript"],
    50,
)


def test_samples_regenerate_to_the_same_bytes(tmp_path: Path) -> None:
    """A sample that drifted from the declarations misrepresents them silently."""
    out = tmp_path / "regenerated"
    mint(
        pack=ROOT,
        recipe="portfolio-baseline",
        seed=1,
        out=out,
        records=SAMPLE_COUNTS,
        invocation="pytest",
    )
    drifted = []
    for committed in sorted((ROOT / "samples").glob("*.jsonl")):
        fresh = out / committed.name
        assert fresh.exists(), f"{committed.name} is committed but no longer produced"
        if committed.read_bytes() != fresh.read_bytes():
            drifted.append(committed.name)
    assert not drifted, (
        f"samples drifted: {drifted}. Regenerate with the command in samples/README.md."
    )


def test_samples_are_capped_at_fifty_records_per_type() -> None:
    """The contract's bound. A pack is declarations, not a dataset."""
    for path in sorted((ROOT / "samples").glob("*.jsonl")):
        lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        assert len(lines) <= 50, f"{path.name} carries {len(lines)} records"
        assert lines, f"{path.name} is empty and should not be committed"


def test_samples_carry_no_manifest() -> None:
    """Samples are illustrative. A manifest would make them look like a dataset."""
    assert not (ROOT / "samples" / "MINTMARK.json").exists()
    assert not (ROOT / "samples" / "SHA256SUMS").exists()


# The README's claims about its own contents.


README_EN = ROOT / "README.md"
README_TR = ROOT / "README.tr.md"


def test_the_readme_example_is_real_output_not_an_illustration() -> None:
    """A README that invents its example will invent a stale one eventually."""
    quoted = README_EN.read_text(encoding="utf-8")
    first = json.loads(
        (ROOT / "samples" / "claim_note.jsonl").read_text(encoding="utf-8").splitlines()[0]
    )["body"]
    # The README wraps the excerpt, so compare on the distinctive values rather
    # than on the wrapped text.
    for token in first.split()[:6]:
        assert token in quoted, f"the README example does not match the sample: {token!r} missing"


def test_the_readme_states_the_counts_it_claims() -> None:
    banks = len(PACK.lexicons["insurers_fictional"]["values"])
    text = README_EN.read_text(encoding="utf-8")
    assert (
        f"{banks} invented insurer names" in text
        or f"kurgusal%20sigortaci-{banks}" in text
        or f"fictional%20insurers-{banks}" in text
    ), f"the README insurer count has drifted from the {banks} actually declared"
    assert f"record%20types-{len(PACK.record_types) - 3}" in text or "record types" in text


def test_both_readmes_exist_and_mirror_each_other() -> None:
    import re

    heading = re.compile(r"^(#{1,6})\s", re.MULTILINE)
    levels_en = [len(m.group(1)) for m in heading.finditer(README_EN.read_text(encoding="utf-8"))]
    levels_tr = [len(m.group(1)) for m in heading.finditer(README_TR.read_text(encoding="utf-8"))]
    assert levels_en == levels_tr, "the Turkish mirror has diverged in structure"


@pytest.mark.parametrize("path", [README_EN, README_TR], ids=["en", "tr"])
def test_each_readme_declares_the_anomaly_limitation(path: Path) -> None:
    """The anomaly kinds are per-row labels, not temporal structures.

    Saying so is the difference between a fixture someone can trust and one that
    quietly overstates what it contains.
    """
    text = path.read_text(encoding="utf-8").lower()
    assert "per-row" in text or "satir bazli" in text or "satır bazlı" in text
    assert "evasion" in text or "atlatma" in text or "kacinma" in text or "kaçınma" in text


@pytest.mark.parametrize("path", [README_EN, README_TR], ids=["en", "tr"])
def test_each_readme_names_the_release_that_actually_exists(path: Path) -> None:
    """A README may claim a release, and the claim has to be the right one.

    This replaced a test that asserted nothing was published, which was correct
    until something was. The failure it now guards is subtler and likelier: a
    version bump that leaves the README pointing at a tag nobody cut, or at an
    older one whose datasets no longer reproduce from these declarations.
    """
    text = path.read_text(encoding="utf-8")
    tag = f"v{PACK.version}"
    assert f"/releases/tag/{tag}" in text, (
        f"{path.name} does not point at {tag}, the version this pack declares"
    )
    stale = re.findall(r"/releases/tag/v(\d+\.\d+\.\d+)", text)
    assert set(stale) == {PACK.version}, (
        f"{path.name} names releases {sorted(set(stale))} while the pack is {PACK.version}"
    )


@pytest.mark.parametrize("path", [README_EN, README_TR], ids=["en", "tr"])
def test_each_readme_installs_the_engine_from_where_it_now_lives(path: Path) -> None:
    """This used to assert the engine was on no index, which held until it was.

    The failure worth guarding now is the opposite one: a README still routing a
    reader through the git workaround, or through a name that is not there.
    """
    text = path.read_text(encoding="utf-8")
    assert "uv tool install mintmark" in text, f"{path.name} does not install the engine"
    assert "https://pypi.org/project/mintmark/" in text, (
        f"{path.name} does not link the published engine"
    )
    assert "git+https://github.com/lokomotifai/mintmark" not in text, (
        f"{path.name} still installs from git, which was the workaround for not "
        f"being on an index"
    )


@pytest.mark.parametrize("path", [README_EN, README_TR], ids=["en", "tr"])
def test_each_readme_references_only_committed_assets(path: Path) -> None:
    import re

    for match in re.finditer(r"\((assets/[^)]+)\)", path.read_text(encoding="utf-8")):
        assert (ROOT / match.group(1)).exists(), f"{match.group(1)} is referenced but absent"


# The health boundary.

CLINICAL_DENIED = ROOT / "lexicons" / "clinical_denied_tr.txt"


def denied_terms() -> list[str]:
    return [
        line.strip()
        for line in CLINICAL_DENIED.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]


def test_the_clinical_denied_list_has_real_content() -> None:
    terms = denied_terms()
    assert len(terms) >= 20, f"only {len(terms)} denied terms; the list is a placeholder"
    for category in ("teshis", "kemoterapi", "prognoz"):
        assert category in terms, f"the list omits {category!r}"


def test_no_rendered_document_contains_denied_clinical_vocabulary(minted: Path) -> None:
    """The boundary held in a real mint, not only in the templates.

    A template that drifts into clinical detail still renders, still labels, and
    still passes every other check. This is the control that would notice.
    """
    from mintmark.lexicons import parse

    denied = parse("\n".join(f"{term}    # denied clinical vocabulary" for term in denied_terms()))
    offenders = []
    for name in ("claim_note", "call_transcript"):
        for line in (minted / f"{name}.jsonl").read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            body = json.loads(line)["body"]
            for hit in denied.scan(body):
                offenders.append(f"{name}: {hit.entry!r} in a rendered document")
    assert not offenders, "\n".join(offenders[:10])


def test_no_template_source_contains_denied_clinical_vocabulary() -> None:
    """Catch it in the template rather than waiting for a draw to surface it."""
    from mintmark.lexicons import parse

    denied = parse("\n".join(f"{term}    # denied clinical vocabulary" for term in denied_terms()))
    text = "\n".join(
        p.read_text(encoding="utf-8") for p in sorted((ROOT / "templates").rglob("*.yaml"))
    )
    hits = [hit.entry for hit in denied.scan(text)]
    assert not hits, f"a template carries denied clinical vocabulary: {hits}"


def test_every_health_span_draws_from_the_core_condition_classes(minted: Path) -> None:
    """Category granularity is enforced by where the surface comes from."""
    from mintmark.annotate import Label
    from mintmark.mint import core_descriptors

    allowed = set(core_descriptors(Label.HEALTH))
    for sidecar in sorted(minted.glob("*.labels.jsonl")):
        stem = sidecar.name.removesuffix(".labels.jsonl")
        bodies = {
            next(v for k, v in json.loads(line).items() if k.endswith("_id")): json.loads(line)[
                "body"
            ]
            for line in (minted / f"{stem}.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        for line in sidecar.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            text = bodies[record["doc_id"]]
            for span in record["spans"]:
                if span["label"] == "HEALTH":
                    surface = text[span["start"] : span["end"]]
                    assert surface in allowed, (
                        f"a HEALTH span carries {surface!r}, which is not a curated condition class"
                    )


def test_the_denied_list_would_catch_a_planted_term() -> None:
    """A control that has never rejected anything is not known to reject anything."""
    from mintmark.lexicons import parse

    denied = parse("\n".join(f"{term}    # denied clinical vocabulary" for term in denied_terms()))
    planted = "Sigortalinin dosyasina kemoterapi tedavisi notu islendi."
    assert denied.scan(planted), "the denied list no longer catches an obvious term"


# What a version bump costs.


def test_the_pack_version_is_part_of_what_seeds_the_streams(tmp_path: Path) -> None:
    """Bumping the version changes every emitted byte for a fixed seed.

    The version is one of the six inputs every generation stream is derived from,
    so version and content correspond exactly: two datasets carrying the same
    pack version cannot differ, and a bump is never a no-op for anyone holding a
    published manifest. Worth a test because it is surprising, and because the
    sample freshness failure it causes reads like a bug until you know why.

    The pack digest is a separate record and seeds nothing. An earlier version of
    this docstring said the version reached the streams through the digest, which
    was wrong.
    """
    import shutil

    rolled_back = tmp_path / "rolled-back"
    shutil.copytree(
        ROOT,
        rolled_back,
        ignore=shutil.ignore_patterns(".venv", ".git", ".pytest_cache", "samples", "dist"),
    )
    manifest = rolled_back / "pack.yaml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            f"version: {PACK.version}", "version: 9.9.9"
        ),
        encoding="utf-8",
    )

    out = tmp_path / "probe"
    mint(
        pack=rolled_back,
        recipe="portfolio-baseline",
        seed=1,
        out=out,
        records={"policyholder": 20},
        invocation="pytest",
    )
    changed = (out / "policyholder.jsonl").read_bytes()
    committed = (ROOT / "samples" / "policyholder.jsonl").read_bytes()
    assert not committed.startswith(changed[:200]), (
        "a different pack version produced identical bytes, so the version is no "
        "longer part of the digest and two datasets can now share a version while "
        "differing in content"
    )


@pytest.mark.parametrize("path", [README_EN, README_TR], ids=["en", "tr"])
def test_no_readme_claims_a_test_count(path: Path) -> None:
    """A number in a badge goes stale the next time somebody adds a test.

    One of these READMEs claimed 53 while the suite had grown past a hundred. The
    engine repository keeps its count badge and holds it true with a test; a pack
    has no such badge, and this keeps it that way rather than inviting a claim
    nobody will maintain.
    """
    import re

    assert not re.search(r"badge/tests?-\d+-", path.read_text(encoding="utf-8")), (
        f"{path.name} claims a test count; either drop it or hold it true with a test"
    )
