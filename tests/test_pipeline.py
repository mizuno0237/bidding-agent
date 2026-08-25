from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from bidding_agent.pipeline import (
    build_outline,
    coverage_markdown,
    coverage_report,
    outline_as_json,
    parse_rfp,
    run_job,
    run_pipeline,
    traceability_rows,
)

RFP = ROOT / "samples" / "rfp" / "harborlight-dc-rfp.md"


def test_outline_covers_required_response_sections() -> None:
    outline = build_outline(parse_rfp(RFP.read_text(encoding="utf-8")))
    ids = [item.id for item in outline]
    assert ids == [
        "scope",
        "functional",
        "non_functional",
        "implementation",
        "training",
        "assumptions",
    ]
    functional = next(item for item in outline if item.id == "functional")
    assert any("ASN" in bullet for bullet in functional.bullets)


def test_export_traces_rfp_and_stays_synthetic() -> None:
    markdown = run_pipeline(RFP)
    assert "Harborlight Regional DC — technical proposal" in markdown
    assert "Functional response" in markdown
    assert "synthetic" in markdown.lower()
    assert "live inventory" in markdown.lower()


def test_outline_json_keeps_section_ids_and_asn_trace() -> None:
    _, outline = run_job(RFP)
    payload = outline_as_json(outline)
    assert [row["id"] for row in payload] == [
        "scope",
        "functional",
        "non_functional",
        "implementation",
        "training",
        "assumptions",
    ]
    functional = next(row for row in payload if row["id"] == "functional")
    first = functional["bullets"][0]
    assert first["id"] == "REQ-F1"
    assert "ASN" in first["text"]


def test_proposal_stamps_requirement_ids() -> None:
    markdown = run_pipeline(RFP)
    assert "**REQ-F1:**" in markdown
    assert "**REQ-N1:**" in markdown


def test_coverage_is_complete_for_the_sample_rfp() -> None:
    _, outline = run_job(RFP)
    report = coverage_report(outline)
    assert report["complete"] is True
    assert report["missing"] == []
    assert "REQ-F1" in report["stamped"]
    assert report["count"] == len(report["stamped"])
    assert report["byChapter"]["functional"] == 5
    sheet = coverage_markdown(report)
    assert "Status: **complete**" in sheet
    assert "| functional | 5 |" in sheet


def test_coverage_flags_missing_training_heading() -> None:
    truncated = "\n".join(RFP.read_text(encoding="utf-8").split("## 5.")[0])
    outline = build_outline(parse_rfp(truncated))
    report = coverage_report(outline)
    assert report["complete"] is False
    assert "training" in report["missing"]


def test_traceability_maps_asn_to_functional_chapter() -> None:
    _, outline = run_job(RFP)
    rows = {row["id"]: row for row in traceability_rows(outline)}
    assert rows["REQ-F1"]["chapterId"] == "functional"
    assert rows["REQ-F1"]["chapter"] == "Functional response"
    assert "ASN" in rows["REQ-F1"]["text"]
    assert rows["REQ-T1"]["chapterId"] == "training"


def test_strict_cli_fails_when_training_is_missing(tmp_path: Path) -> None:
    truncated = tmp_path / "rfp.md"
    truncated.write_text("\n".join(RFP.read_text(encoding="utf-8").split("## 5.")[0]), encoding="utf-8")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "bidding_agent",
            str(truncated),
            "--strict",
            "--out",
            str(tmp_path / "proposal.md"),
            "--outline",
            str(tmp_path / "outline.json"),
            "--report",
            str(tmp_path / "coverage.json"),
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "training" in result.stderr + result.stdout
