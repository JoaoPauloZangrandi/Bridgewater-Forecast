"""Build original figures used in the submission.

The figures contain no scraped artwork. Values come from the source ledger and
the scenario matrix; they are intentionally simple enough to audit by eye.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated"
SCENARIOS = ROOT / "data" / "scenario_matrix.csv"

INK = "#202829"
MUTED = "#687170"
ACCENT = "#145c58"
COPPER = "#a36a32"
RUST = "#a2473d"
PALE = "#eaf0ee"
GRID = "#d5dcda"
WHITE = "#ffffff"


def save(fig: plt.Figure, filename: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        OUT / filename,
        dpi=220,
        bbox_inches="tight",
        facecolor=WHITE,
        pad_inches=0.04,
    )
    plt.close(fig)


def causal_loop() -> None:
    fig, ax = plt.subplots(figsize=(10.6, 3.35), facecolor=WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 3.35)
    ax.axis("off")

    nodes = [
        (0.85, "AI capability\nand diffusion"),
        (3.08, "Compute, power,\nand mineral demand"),
        (5.30, "Chokepoint rents\nand dependence"),
        (7.52, "Subsidies, controls,\nand localization"),
        (9.75, "Duplicated capacity\nand higher cost"),
    ]
    for idx, (x, label) in enumerate(nodes, start=1):
        ax.add_patch(patches.Circle((x, 1.72), 0.24, facecolor=ACCENT, edgecolor="none"))
        ax.text(
            x,
            1.72,
            f"{idx:02d}",
            ha="center",
            va="center",
            color=WHITE,
            fontsize=8.5,
            fontweight="bold",
        )
        ax.text(
            x,
            1.20,
            label,
            ha="center",
            va="top",
            color=INK,
            fontsize=8.6,
            fontweight="bold",
            linespacing=1.18,
        )

    for idx in range(len(nodes) - 1):
        x1, _ = nodes[idx]
        x2, _ = nodes[idx + 1]
        ax.annotate(
            "",
            xy=(x2 - 0.29, 1.72),
            xytext=(x1 + 0.29, 1.72),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0),
        )

    ax.annotate(
        "",
        xy=(0.88, 2.03),
        xytext=(9.72, 2.03),
        arrowprops=dict(
            arrowstyle="-|>",
            color=COPPER,
            lw=1.25,
            connectionstyle="arc3,rad=0.28",
        ),
    )
    ax.text(
        5.30,
        3.10,
        "REINFORCING LOOP  /  Strategic rivalry raises the option value of domestic capacity",
        ha="center",
        color=COPPER,
        fontsize=8.0,
        fontweight="bold",
    )

    ax.annotate(
        "",
        xy=(3.05, 0.77),
        xytext=(9.70, 0.77),
        arrowprops=dict(
            arrowstyle="-|>",
            color=MUTED,
            lw=1.1,
            linestyle="--",
            connectionstyle="arc3,rad=-0.15",
        ),
    )
    ax.text(
        6.35,
        0.13,
        "COUNTER-LOOP  /  Efficiency, substitution, and weak returns reduce resource intensity",
        ha="center",
        color=MUTED,
        fontsize=7.8,
        fontweight="bold",
    )
    save(fig, "causal_loop.png")


def scenario_heatmap() -> None:
    with SCENARIOS.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    ids = [row["id"] for row in rows]
    matrix = np.array(
        [
            [
                float(row["abundant_intelligence"]),
                float(row["bottlenecked_boom"]),
                float(row["capex_retrenchment"]),
                float(row["mixture_probability"]),
            ]
            for row in rows
        ]
    )

    cmap = LinearSegmentedColormap.from_list(
        "institutional_teal",
        ["#f3f6f5", "#d8e5e2", "#8eb6af", ACCENT],
        N=256,
    )
    fig, ax = plt.subplots(figsize=(7.8, 5.55), facecolor=WHITE)
    ax.set_facecolor(WHITE)
    ax.imshow(matrix, cmap=cmap, vmin=10, vmax=95, aspect="auto")
    ax.set_xticks(range(4))
    ax.set_xticklabels(
        [
            "ABUNDANT AI\n25% weight",
            "BOTTLENECKED BOOM\n50% weight",
            "RETRENCHMENT\n25% weight",
            "FINAL\nP(YES)",
        ],
        fontsize=7.8,
        color=INK,
        fontweight="bold",
    )
    ax.set_yticks(range(len(ids)))
    ax.set_yticklabels(ids, fontsize=8.0, color=INK, fontweight="bold")
    ax.tick_params(length=0)

    for row_idx in range(matrix.shape[0]):
        for col_idx in range(matrix.shape[1]):
            value = matrix[row_idx, col_idx]
            ax.text(
                col_idx,
                row_idx,
                f"{value:.0f}",
                ha="center",
                va="center",
                color=WHITE if value > 72 else INK,
                fontsize=8.3 if col_idx == 3 else 8.0,
                fontweight="bold",
            )

    ax.axvline(2.5, color=ACCENT, linewidth=1.25)
    ax.add_patch(
        patches.Rectangle(
            (2.5, -0.5),
            1.0,
            len(ids),
            fill=False,
            linewidth=1.2,
            edgecolor=ACCENT,
        )
    )
    for boundary in (4.5, 7.5):
        ax.axhline(boundary, color=WHITE, linewidth=2.0)

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(
        "EXHIBIT 3  /  SCENARIO CONDITIONALS AND FINAL PROBABILITY (%)",
        loc="left",
        fontsize=10.0,
        color=ACCENT,
        fontweight="bold",
        pad=10,
    )
    ax.text(
        0.0,
        -0.105,
        "Final = 25/50/25 weighted mean; white separators mark analytical bundles.",
        transform=ax.transAxes,
        color=MUTED,
        fontsize=7.0,
        va="top",
    )
    save(fig, "scenario_heatmap.png")


def evidence_dashboard() -> None:
    fig, ax = plt.subplots(figsize=(10.6, 4.15), facecolor=WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 4.15)
    ax.axis("off")

    panels = [
        ("F02", "U.S. firms using AI", 64, 18, 35, 0, 45, "2025/26 actual", "YES if >= 35%"),
        ("F05", "U.S. data-center power", 52, 11.8, 12, 0, 16, "2030 DOE midpoint", "YES if > 12%"),
        ("F08", "Top-country refiner share", 83, 72, 65, 40, 80, "2025 actual", "YES if > 65%"),
        ("F10", "Trade on MFN terms", 57, 72, 65, 40, 85, "early-2026 actual", "YES if <= 65%"),
    ]

    ax.text(
        0.0,
        4.02,
        "EXHIBIT 1  /  STARTING POINT VERSUS RESOLUTION THRESHOLD",
        color=ACCENT,
        fontsize=9.2,
        fontweight="bold",
        va="top",
    )
    ax.plot([0, 10.6], [3.78, 3.78], color=ACCENT, lw=0.9)

    for idx, panel in enumerate(panels):
        forecast_id, title, probability, base, threshold, low, high, base_label, threshold_label = panel
        y = 3.18 - idx * 0.86
        x0, x1 = 4.15, 8.95
        base_x = x0 + (base - low) / (high - low) * (x1 - x0)
        threshold_x = x0 + (threshold - low) / (high - low) * (x1 - x0)

        ax.text(0.0, y + 0.13, forecast_id, color=ACCENT, fontsize=8.0, fontweight="bold")
        ax.text(0.48, y + 0.13, title, color=INK, fontsize=9.4, fontweight="bold")
        ax.plot([x0, x1], [y, y], color=GRID, linewidth=2.6, solid_capstyle="round")
        ax.scatter(base_x, y, s=58, color=ACCENT, zorder=3)
        ax.scatter(
            threshold_x,
            y,
            s=105,
            marker="|",
            linewidth=2.6,
            color=INK,
            zorder=4,
        )
        ax.text(
            base_x,
            y + 0.18,
            f"{base:g}%",
            ha="center",
            fontsize=8.6,
            color=ACCENT,
            fontweight="bold",
        )
        ax.text(
            threshold_x,
            y - 0.20,
            f"{threshold:g}%",
            ha="center",
            fontsize=8.2,
            color=INK,
            fontweight="bold",
        )
        ax.text(
            x0,
            y - 0.29,
            base_label.upper(),
            fontsize=6.6,
            color=MUTED,
            va="top",
        )
        ax.text(
            x1,
            y - 0.29,
            threshold_label,
            fontsize=6.6,
            color=MUTED,
            ha="right",
            va="top",
        )
        ax.text(
            10.55,
            y + 0.03,
            f"{probability}%",
            fontsize=11.2,
            color=ACCENT,
            ha="right",
            va="center",
            fontweight="bold",
        )
        ax.text(10.55, y - 0.19, "P(YES)", fontsize=6.5, color=MUTED, ha="right")

        if idx < len(panels) - 1:
            ax.plot([0, 10.6], [y - 0.51, y - 0.51], color=GRID, lw=0.55)

    save(fig, "evidence_dashboard.png")


def trade_matrix() -> None:
    fig, ax = plt.subplots(figsize=(10.6, 3.55), facecolor=WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(-0.22, 2.05)
    ax.set_ylim(-0.22, 2.35)
    ax.axis("off")

    quadrants = [
        (0, 0, WHITE, "REBALANCING", "Lower surplus;\nlimited discrimination", MUTED),
        (1, 0, WHITE, "POLICY TRACTION", "Protection rises;\nChina's surplus falls", MUTED),
        (0, 1, WHITE, "REROUTING", "Surplus persists;\nuniversal rules stabilize", MUTED),
        (1, 1, PALE, "ASSURED-ACCESS REGIME", "Imbalance and discrimination\nreinforce each other", ACCENT),
    ]
    for x, y, face, title, body, color in quadrants:
        ax.add_patch(
            patches.Rectangle(
                (x, y),
                1,
                1,
                linewidth=0.7,
                edgecolor=GRID,
                facecolor=face,
            )
        )
        ax.add_patch(
            patches.Rectangle(
                (x + 0.06, y + 0.81),
                0.22,
                0.025,
                linewidth=0,
                facecolor=color,
            )
        )
        ax.text(
            x + 0.06,
            y + 0.70,
            title,
            color=color,
            fontsize=8.0,
            fontweight="bold",
            va="center",
        )
        ax.text(
            x + 0.06,
            y + 0.37,
            body,
            color=INK,
            fontsize=8.8,
            fontweight="normal",
            va="center",
            linespacing=1.25,
        )

    ax.text(
        1.0,
        -0.12,
        "RULE FRAGMENTATION  /  F10 + F12",
        ha="center",
        va="center",
        color=INK,
        fontsize=7.6,
        fontweight="bold",
    )
    ax.text(
        -0.14,
        1.0,
        "CHINA SURPLUS  /  F09",
        ha="center",
        va="center",
        rotation=90,
        color=INK,
        fontsize=7.6,
        fontweight="bold",
    )
    ax.text(
        0.0,
        2.23,
        "EXHIBIT 4  /  JOINT OUTCOME MAP",
        color=ACCENT,
        fontsize=7.5,
        fontweight="bold",
        va="center",
    )
    ax.text(
        2.0,
        2.23,
        "F11 is the institutional overlay: adjudication can remain blocked in every quadrant.",
        color=MUTED,
        fontsize=7.4,
        ha="right",
        va="center",
    )
    save(fig, "trade_matrix.png")


def main() -> None:
    causal_loop()
    scenario_heatmap()
    evidence_dashboard()
    trade_matrix()
    print(
        "Built causal_loop.png, scenario_heatmap.png, "
        "evidence_dashboard.png, trade_matrix.png"
    )


if __name__ == "__main__":
    main()
