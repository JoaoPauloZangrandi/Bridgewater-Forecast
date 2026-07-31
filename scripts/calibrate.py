"""Audit lens anchors, scenario conditionals, and final probabilities.

The four-lens anchor screens for an incoherent starting point. Final
probabilities come from the scenario mixture because it preserves dependence
across forecasts. Neither calculation is a fitted statistical model.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "forecast_candidates.csv"
SCENARIOS = ROOT / "data" / "scenario_matrix.csv"
FINAL = ROOT / "data" / "final_forecasts.csv"
OUTPUT = ROOT / "generated" / "calibration_table.tex"


def logit(probability: float) -> float:
    return math.log(probability / (1.0 - probability))


def logistic(value: float) -> float:
    return 1.0 / (1.0 + math.exp(-value))


def reconcile(probabilities: list[float]) -> float:
    """Use a robust center, then modestly extremize away from 0.5.

    The median limits one unstable lens; a 1.08 multiplier is deliberately
    smaller than an estimated Platt correction because this project has no
    challenge-specific calibration set.
    """

    logits = sorted(logit(value) for value in probabilities)
    center = (logits[1] + logits[2]) / 2.0
    return logistic(1.08 * center)


def main() -> None:
    candidates: list[dict[str, str]] = []
    with INPUT.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            values = [
                float(row["prior"]),
                float(row["trend_view"]),
                float(row["policy_view"]),
                float(row["counter_view"]),
            ]
            row["lens_anchor"] = f"{100 * reconcile(values):.0f}"
            candidates.append(row)

    with SCENARIOS.open(encoding="utf-8", newline="") as handle:
        scenarios = list(csv.DictReader(handle))
    with FINAL.open(encoding="utf-8", newline="") as handle:
        final_rows = list(csv.DictReader(handle))

    if not (len(candidates) == len(scenarios) == len(final_rows)):
        raise ValueError("Candidate, scenario, and final tables differ in length")

    lines = [
        r"\begin{tabular}{llrrrr}",
        r"\toprule",
        r"ID & Cluster & Lens anchor & Scenario mix & Final & Gap \\",
        r"\midrule",
    ]

    print("Probability audit:")
    for candidate, scenario, final in zip(candidates, scenarios, final_rows):
        forecast_id = candidate["id"]
        if not (forecast_id == scenario["id"] == final["id"]):
            raise ValueError(f"Forecast ordering mismatch at {forecast_id}")

        scenario_mix = (
            0.25 * float(scenario["abundant_intelligence"])
            + 0.50 * float(scenario["bottlenecked_boom"])
            + 0.25 * float(scenario["capex_retrenchment"])
        )
        recorded_mix = float(scenario["mixture_probability"])
        final_probability = float(final["probability"])
        if abs(scenario_mix - recorded_mix) > 0.51:
            raise ValueError(
                f"{forecast_id}: recorded mixture {recorded_mix:.0f} differs "
                f"from calculated mixture {scenario_mix:.1f}"
            )
        if abs(final_probability - recorded_mix) > 0.01:
            raise ValueError(
                f"{forecast_id}: final {final_probability:.0f} differs from "
                f"recorded mixture {recorded_mix:.0f}"
            )

        lens_anchor = float(candidate["lens_anchor"])
        gap = final_probability - lens_anchor
        print(
            f"{forecast_id}: lens={lens_anchor:.0f}%, "
            f"scenario={scenario_mix:.1f}%, final={final_probability:.0f}%, "
            f"gap={gap:+.0f}pp"
        )
        lines.append(
            f"{forecast_id} & {candidate['cluster'].replace('_', ' ')} & "
            f"{lens_anchor:.0f} & {scenario_mix:.1f} & "
            f"{final_probability:.0f} & {gap:+.0f} \\\\"
        )

    lines.extend([r"\bottomrule", r"\end{tabular}"])
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
