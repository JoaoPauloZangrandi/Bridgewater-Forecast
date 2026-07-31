"""Fail-fast checks for the challenge PDF and its forecast inputs."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
FORECASTS = ROOT / "data" / "final_forecasts.csv"
SCENARIOS = ROOT / "data" / "scenario_matrix.csv"
RESOLUTIONS = ROOT / "research" / "resolution_registry.md"
TEX = ROOT / "submission.tex"
DELIVERABLE = ROOT / "deliverable"
BUILD = ROOT / "build"


def command_text(*args: str) -> str:
    completed = subprocess.run(
        args,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.stdout


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def page_text(pdf: Path, page: int) -> str:
    return command_text(
        "pdftotext", "-f", str(page), "-l", str(page), "-layout", str(pdf), "-"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--allow-draft",
        action="store_true",
        help="Allow the visible author-review watermark.",
    )
    args = parser.parse_args()

    pdfs = list(DELIVERABLE.glob("*.pdf"))
    require(len(pdfs) == 1, f"Expected exactly one deliverable PDF, found {len(pdfs)}")
    pdf = pdfs[0]

    with FORECASTS.open(encoding="utf-8", newline="") as handle:
        forecasts = list(csv.DictReader(handle))
    require(len(forecasts) >= 10, "Challenge requires at least ten forecasts")
    require(len({row["id"] for row in forecasts}) == len(forecasts), "Duplicate ID")

    expected_ids = [f"F{number:02d}" for number in range(1, len(forecasts) + 1)]
    require([row["id"] for row in forecasts] == expected_ids, "Forecast IDs are not contiguous")
    for row in forecasts:
        probability = int(row["probability"])
        require(0 < probability < 100, f"{row['id']} probability is not interior")
        require(
            row["forecast_sentence"].startswith(("There is a ", "There is an ")),
            f"{row['id']} wording",
        )
        require(row["forecast_sentence"].endswith("."), f"{row['id']} lacks terminal period")
        require(int(row["horizon"]) <= 2030, f"{row['id']} exceeds five-year event horizon")

    with SCENARIOS.open(encoding="utf-8", newline="") as handle:
        scenario_rows = list(csv.DictReader(handle))
    require(len(scenario_rows) == len(forecasts), "Scenario/forecast row mismatch")
    for forecast, scenario in zip(forecasts, scenario_rows):
        require(forecast["id"] == scenario["id"], "Scenario order mismatch")
        mixture = (
            0.25 * float(scenario["abundant_intelligence"])
            + 0.50 * float(scenario["bottlenecked_boom"])
            + 0.25 * float(scenario["capex_retrenchment"])
        )
        require(
            abs(mixture - int(forecast["probability"])) <= 0.51,
            f"{forecast['id']} probability differs from scenario mixture",
        )

    resolution_text = RESOLUTIONS.read_text(encoding="utf-8")
    for forecast_id in expected_ids:
        require(f"**{forecast_id}." in resolution_text, f"Missing {forecast_id} resolution")

    info = command_text("pdfinfo", str(pdf))
    pages_match = re.search(r"^Pages:\s+(\d+)$", info, flags=re.MULTILINE)
    require(pages_match is not None, "Could not read PDF page count")
    require(int(pages_match.group(1)) == 10, "PDF must be exactly ten pages")
    require("Page size:       612 x 792 pts (letter)" in info, "PDF is not US Letter")

    first_two = page_text(pdf, 1) + page_text(pdf, 2)
    for row in forecasts:
        require(row["id"] in first_two, f"{row['id']} missing from Part 1")
        require(f"{row['probability']}%" in first_two, f"{row['id']} probability missing")

    require("PART 2" in page_text(pdf, 3), "Framework does not start on page 3")
    require("PART 2" in page_text(pdf, 5), "Framework does not occupy page 5")
    require("PART 3" in page_text(pdf, 6), "Appendix does not start on page 6")
    require(
        "RESOLUTION REGISTRY" in page_text(pdf, 10),
        "Resolution registry is not on page 10",
    )

    all_text = command_text("pdftotext", "-layout", str(pdf), "-")
    require("July 30, 2026" in all_text, "Information cutoff missing")
    require("??" not in all_text, "Unresolved placeholder found in PDF text")

    log_path = BUILD / f"{pdf.stem}.log"
    require(log_path.exists(), "Compilation log is missing")
    log_text = log_path.read_text(encoding="utf-8", errors="replace")
    require("Overfull \\hbox" not in log_text, "Overfull box in LaTeX log")
    require("undefined references" not in log_text.lower(), "Undefined references")
    require("Output written on" in log_text and "(10 pages" in log_text, "Bad build log")

    tex_text = TEX.read_text(encoding="utf-8")
    is_draft = "\\drafttrue" in tex_text
    if not args.allow_draft:
        require(not is_draft, "Draft mode is still enabled")
        require("AUTHOR REVIEW DRAFT" not in all_text, "Draft watermark remains")

    digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
    mode = "draft accepted for review" if is_draft else "final"
    print(f"PASS: {pdf.name}")
    print(f"mode: {mode}")
    print(f"forecasts: {len(forecasts)}")
    print("pages: 10")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
