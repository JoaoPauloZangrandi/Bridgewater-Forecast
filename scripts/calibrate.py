"""Reconcile independent forecast lenses and check the scenario mixture.

This is a decision aid, not a substitute for the entrant's judgment. Each
component probability must be defended from the source ledger before use.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "forecast_candidates.csv"
SCENARIOS = ROOT / "data" / "scenario_matrix.csv"
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
    rows: list[dict[str, str]] = []
    with INPUT.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            values = [
                float(row["prior"]),
                float(row["trend_view"]),
                float(row["policy_view"]),
                float(row["counter_view"]),
            ]
            row["model_probability"] = f"{100 * reconcile(values):.0f}"
            rows.append(row)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        r"\begin{tabular}{llrrrrr}",
        r"\toprule",
        r"ID & Cluster & Prior & Trend & Policy & Counter & Model \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(
            f"{row['id']} & {row['cluster'].replace('_', ' ')} & "
            f"{100 * float(row['prior']):.0f} & "
            f"{100 * float(row['trend_view']):.0f} & "
            f"{100 * float(row['policy_view']):.0f} & "
            f"{100 * float(row['counter_view']):.0f} & "
            f"{row['model_probability']} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    for row in rows:
        print(f"{row['id']}: {row['model_probability']}%")

    with SCENARIOS.open(encoding="utf-8", newline="") as handle:
        scenarios = list(csv.DictReader(handle))

    print("\nScenario-mixture audit (25% / 50% / 25%):")
    for row in scenarios:
        calculated = (
            0.25 * float(row["abundant_intelligence"])
            + 0.50 * float(row["bottlenecked_boom"])
            + 0.25 * float(row["capex_retrenchment"])
        )
        recorded = float(row["mixture_probability"])
        if abs(calculated - recorded) > 0.51:
            raise ValueError(
                f"{row['id']}: recorded {recorded:.0f} differs from "
                f"mixture {calculated:.1f}"
            )
        print(f"{row['id']}: mixture={calculated:.1f}%, recorded={recorded:.0f}%")


if __name__ == "__main__":
    main()
