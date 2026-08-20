from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from bidding_agent.pipeline import build_outline, outline_as_json, parse_rfp, run_job, run_pipeline

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
    assert any("ASN" in str(bullet) for bullet in functional["bullets"])
