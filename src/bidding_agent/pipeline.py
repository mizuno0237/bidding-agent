from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

SECTION_MAP = [
    ("scope", "Understanding of scope", ("scope of work", "1. scope")),
    ("functional", "Functional response", ("functional requirements", "2. functional")),
    ("non_functional", "Non-functional response", ("non-functional", "3. non-functional")),
    ("implementation", "Implementation plan", ("implementation", "4. implementation")),
    ("training", "Training and support", ("training", "5. training")),
]


@dataclass
class Section:
    heading: str
    body: str


@dataclass
class OutlineItem:
    id: str
    title: str
    source_heading: str
    bullets: list[str] = field(default_factory=list)


def parse_rfp(text: str) -> list[Section]:
    chunks = re.split(r"(?m)^##\s+", text)
    sections: list[Section] = []
    for chunk in chunks[1:]:
        lines = chunk.strip().splitlines()
        if not lines:
            continue
        sections.append(Section(heading=lines[0].strip(), body="\n".join(lines[1:]).strip()))
    return sections


def _match_section(sections: list[Section], needles: tuple[str, ...]) -> Section | None:
    for section in sections:
        hay = section.heading.lower()
        if any(needle in hay for needle in needles):
            return section
    return None


def bullets_from(body: str) -> list[str]:
    items: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if re.match(r"^[-*]|\d+\.", stripped):
            items.append(re.sub(r"^([-*]|\d+\.)\s*", "", stripped))
    if items:
        return items
    paras = [part.strip() for part in re.split(r"\n\s*\n", body) if part.strip()]
    return paras[:4]


def build_outline(sections: list[Section]) -> list[OutlineItem]:
    outline: list[OutlineItem] = []
    for item_id, title, needles in SECTION_MAP:
        found = _match_section(sections, needles)
        outline.append(
            OutlineItem(
                id=item_id,
                title=title,
                source_heading=found.heading if found else "(no matching RFP heading)",
                bullets=bullets_from(found.body) if found else [],
            )
        )
    outline.append(
        OutlineItem(
            id="assumptions",
            title="Assumptions and exclusions",
            source_heading="Proposal format",
            bullets=[
                "Sample is synthetic. No live inventory, no customer brand.",
                "Commercial envelope (price, bonds) is out of scope for this public slice.",
            ],
        )
    )
    return outline


REQ_PREFIX = {
    "scope": "S",
    "functional": "F",
    "non_functional": "N",
    "implementation": "I",
    "training": "T",
    "assumptions": "A",
}


def stamp_requirements(item: OutlineItem) -> list[dict[str, str]]:
    """Stable ids so a reviewer can point at one RFP bullet."""
    prefix = REQ_PREFIX[item.id]
    return [{"id": f"REQ-{prefix}{index}", "text": text} for index, text in enumerate(item.bullets, start=1)]


def outline_as_json(outline: list[OutlineItem]) -> list[dict[str, object]]:
    """Stable outline the drafter (or a later model) must follow. Missing bullets stay empty."""
    return [
        {
            "id": item.id,
            "title": item.title,
            "sourceHeading": item.source_heading,
            "bullets": stamp_requirements(item),
        }
        for item in outline
    ]


def draft_chapters(outline: list[OutlineItem]) -> str:
    parts = [
        "# Harborlight Regional DC — technical proposal (synthetic)",
        "",
        "> Generated offline from `samples/rfp/harborlight-dc-rfp.md`. Replace this stub with a model call later; the outline is the contract.",
        "",
    ]
    for item in outline:
        parts.append(f"## {item.title}")
        parts.append("")
        parts.append(f"*RFP source:* {item.source_heading}")
        parts.append("")
        if not item.bullets:
            parts.append("No RFP bullets were found for this heading. The agent must not invent requirements.")
        else:
            parts.append("Response traces the RFP as follows:")
            parts.append("")
            for bullet in stamp_requirements(item):
                parts.append(f"- **{bullet['id']}:** {bullet['text']}")
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def coverage_report(outline: list[OutlineItem]) -> dict[str, object]:
    """Required response sections with no RFP bullets. The agent must not invent them."""
    required = [item for item in outline if item.id != "assumptions"]
    missing = [item.id for item in required if not item.bullets]
    stamped = [row["id"] for item in outline for row in stamp_requirements(item)]
    return {
        "complete": len(missing) == 0,
        "required": [item.id for item in required],
        "missing": missing,
        "stamped": stamped,
        "count": len(stamped),
    }


def traceability_rows(outline: list[OutlineItem]) -> list[dict[str, str]]:
    """One row per stamped requirement so a reviewer can jump chapter → RFP line."""
    rows: list[dict[str, str]] = []
    for item in outline:
        for bullet in stamp_requirements(item):
            rows.append(
                {
                    "id": bullet["id"],
                    "chapterId": item.id,
                    "chapter": item.title,
                    "sourceHeading": item.source_heading,
                    "text": bullet["text"],
                }
            )
    return rows


def traceability_markdown(rows: list[dict[str, str]]) -> str:
    lines = [
        "# Harborlight Regional DC — requirement traceability (synthetic)",
        "",
        "Each `REQ-*` maps to one proposal chapter. The agent does not invent ids.",
        "",
        "| Id | Chapter | RFP source | Requirement |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        text = row["text"].replace("|", "\\|")
        lines.append(f"| {row['id']} | {row['chapter']} | {row['sourceHeading']} | {text} |")
    lines.append("")
    return "\n".join(lines)


def run_job(rfp_path: Path) -> tuple[str, list[OutlineItem]]:
    sections = parse_rfp(rfp_path.read_text(encoding="utf-8"))
    outline = build_outline(sections)
    return draft_chapters(outline), outline


def run_pipeline(rfp_path: Path) -> str:
    markdown, _ = run_job(rfp_path)
    return markdown


def main() -> None:
    parser = argparse.ArgumentParser(description="RFP → outline → chapter export (offline sample).")
    parser.add_argument("rfp", type=Path, help="Path to a markdown RFP")
    parser.add_argument("--out", type=Path, default=Path("samples/output/proposal.md"))
    parser.add_argument("--outline", type=Path, default=Path("samples/output/outline.json"))
    parser.add_argument("--report", type=Path, default=Path("samples/output/coverage.json"))
    parser.add_argument("--matrix", type=Path, default=Path("samples/output/traceability.md"))
    parser.add_argument("--strict", action="store_true", help="exit 2 if a required section has no RFP bullets")
    args = parser.parse_args()
    markdown, outline = run_job(args.rfp)
    report = coverage_report(outline)
    matrix = traceability_markdown(traceability_rows(outline))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(markdown, encoding="utf-8")
    args.outline.write_text(
        json.dumps(outline_as_json(outline), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    args.matrix.write_text(matrix, encoding="utf-8")
    print(f"wrote {args.out}")
    print(f"wrote {args.outline}")
    print(f"wrote {args.report}")
    print(f"wrote {args.matrix}")
    if args.strict and not report["complete"]:
        missing = ", ".join(str(item) for item in report["missing"])
        raise SystemExit(f"coverage incomplete: {missing}")


if __name__ == "__main__":
    main()
