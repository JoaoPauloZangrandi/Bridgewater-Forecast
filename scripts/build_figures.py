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

INK = "#172733"
MUTED = "#66757d"
BLUE = "#276a8a"
TEAL = "#2b7a72"
GOLD = "#ad761f"
RED = "#af4b42"
PAPER = "#f6f7f4"
PANEL = "#edf1f0"
GRID = "#d4dcde"
WHITE = "#ffffff"


def save(fig: plt.Figure, filename: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        OUT / filename,
        dpi=220,
        bbox_inches="tight",
        facecolor=PAPER,
        pad_inches=0.04,
    )
    plt.close(fig)


def causal_loop() -> None:
    fig, ax = plt.subplots(figsize=(10.6, 3.9), facecolor=PAPER)
    ax.set_facecolor(PAPER)
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 3.9)
    ax.axis("off")

    nodes = [
        (0.12, 2.16, 1.82, 0.88, "AI capability\nand diffusion", BLUE),
        (2.25, 2.16, 1.82, 0.88, "Compute, power,\nmineral demand", TEAL),
        (4.38, 2.16, 1.82, 0.88, "Chokepoint rents\nand dependence", GOLD),
        (6.51, 2.16, 1.82, 0.88, "Subsidies, controls,\nlocalization", RED),
        (8.64, 2.16, 1.82, 0.88, "Duplicated capacity\nand higher cost", INK),
    ]
    for x, y, w, h, label, color in nodes:
        ax.add_patch(
            patches.FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="round,pad=0.02,rounding_size=0.035",
                linewidth=0.8,
                edgecolor=GRID,
                facecolor=WHITE,
            )
        )
        ax.add_patch(
            patches.Rectangle(
                (x, y + h - 0.07),
                w,
                0.07,
                linewidth=0,
                facecolor=color,
            )
        )
        ax.text(
            x + w / 2,
            y + h / 2 - 0.01,
            label,
            ha="center",
            va="center",
            color=INK,
            fontsize=9.1,
            fontweight="bold",
        )

    for idx in range(len(nodes) - 1):
        x1, y1, w1, h1, *_ = nodes[idx]
        x2, y2, *_ = nodes[idx + 1]
        ax.annotate(
            "",
            xy=(x2 - 0.05, y2 + 0.44),
            xytext=(x1 + w1 + 0.05, y1 + 0.44),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1),
        )

    ax.annotate(
        "",
        xy=(1.02, 2.08),
        xytext=(9.48, 2.08),
        arrowprops=dict(
            arrowstyle="-|>",
            color=RED,
            lw=1.35,
            connectionstyle="arc3,rad=-0.34",
        ),
    )
    ax.text(
        5.30,
        0.45,
        "REINFORCING LOOP  |  Strategic rivalry raises the option value of domestic capacity",
        ha="center",
        color=RED,
        fontsize=8.2,
        fontweight="bold",
    )

    ax.annotate(
        "",
        xy=(2.50, 3.12),
        xytext=(8.82, 3.12),
        arrowprops=dict(
            arrowstyle="-|>",
            color=BLUE,
            lw=1.1,
            linestyle="--",
            connectionstyle="arc3,rad=0.13",
        ),
    )
    ax.text(
        5.63,
        3.73,
        "COUNTER-LOOP  |  Efficiency, substitution, and weak returns reduce resource intensity",
        ha="center",
        color=BLUE,
        fontsize=8.1,
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
        "assured_access",
        [BLUE, "#b8d2d7", PAPER, "#efd19d", RED],
        N=256,
    )
    fig, ax = plt.subplots(figsize=(7.8, 5.55), facecolor=PAPER)
    ax.set_facecolor(PAPER)
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
                color=WHITE if value < 34 or value > 78 else INK,
                fontsize=8.3 if col_idx == 3 else 8.0,
                fontweight="bold",
            )

    ax.axvline(2.5, color=INK, linewidth=1.2)
    ax.add_patch(
        patches.Rectangle(
            (2.5, -0.5),
            1.0,
            len(ids),
            fill=False,
            linewidth=1.2,
            edgecolor=INK,
        )
    )
    for boundary in (4.5, 7.5):
        ax.axhline(boundary, color=WHITE, linewidth=2.0)

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(
        "Scenario conditionals and the portfolio-consistent final probability (%)",
        loc="left",
        fontsize=10.0,
        color=INK,
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
    fig, axes = plt.subplots(2, 2, figsize=(10.6, 4.25), facecolor=PAPER)
    fig.subplots_adjust(wspace=0.08, hspace=0.18)

    panels = [
        ("F02", "U.S. firms using AI", 64, 18, 35, 0, 45, "2025/26 actual", "YES if >= 35%", BLUE),
        ("F05", "U.S. data-center power", 52, 11.8, 12, 0, 16, "2030 DOE midpoint", "YES if > 12%", TEAL),
        ("F08", "Top-country refiner share", 83, 72, 65, 40, 80, "2025 actual", "YES if > 65%", GOLD),
        ("F10", "Trade on MFN terms", 57, 72, 65, 40, 85, "early-2026 actual", "YES if <= 65%", RED),
    ]

    for ax, panel in zip(axes.flat, panels):
        forecast_id, title, probability, base, threshold, low, high, base_label, threshold_label, color = panel
        ax.set_facecolor(PANEL)
        ax.set_xlim(low, high)
        ax.set_ylim(0, 1)
        ax.hlines(0.42, low, high, color=GRID, linewidth=5)
        ax.scatter(base, 0.42, s=86, color=color, zorder=3)
        ax.scatter(
            threshold,
            0.42,
            s=110,
            marker="|",
            linewidth=3.2,
            color=INK,
            zorder=4,
        )
        ax.text(
            base,
            0.61,
            f"{base:g}%",
            ha="center",
            fontsize=10.0,
            color=color,
            fontweight="bold",
        )
        ax.text(
            threshold,
            0.19,
            f"{threshold:g}%",
            ha="center",
            fontsize=9.3,
            color=INK,
            fontweight="bold",
        )
        ax.text(
            0.03,
            0.91,
            forecast_id,
            transform=ax.transAxes,
            fontsize=7.2,
            color=color,
            va="center",
            fontweight="bold",
        )
        ax.text(
            0.13,
            0.91,
            title,
            transform=ax.transAxes,
            fontsize=9.2,
            color=INK,
            va="center",
            fontweight="bold",
        )
        ax.text(
            0.97,
            0.91,
            f"P(YES) {probability}%",
            transform=ax.transAxes,
            fontsize=8.1,
            color=color,
            ha="right",
            va="center",
            fontweight="bold",
        )
        ax.text(
            0.03,
            0.04,
            f"ANCHOR  {base_label}",
            transform=ax.transAxes,
            fontsize=6.7,
            color=MUTED,
            va="bottom",
        )
        ax.text(
            0.97,
            0.04,
            threshold_label,
            transform=ax.transAxes,
            fontsize=6.7,
            color=MUTED,
            ha="right",
            va="bottom",
        )
        ax.set_yticks([])
        ax.set_xticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    save(fig, "evidence_dashboard.png")


def trade_matrix() -> None:
    fig, ax = plt.subplots(figsize=(10.6, 3.55), facecolor=PAPER)
    ax.set_facecolor(PAPER)
    ax.set_xlim(-0.22, 2.05)
    ax.set_ylim(-0.22, 2.35)
    ax.axis("off")

    quadrants = [
        (0, 0, "#eef3f3", "REBALANCING", "Lower surplus;\nlimited discrimination", TEAL),
        (1, 0, "#f5eee7", "POLICY TRACTION", "Protection rises;\nChina's surplus falls", GOLD),
        (0, 1, "#edf2f5", "REROUTING", "Surplus persists;\nuniversal rules stabilize", BLUE),
        (1, 1, "#f5eae7", "ASSURED-ACCESS REGIME", "Imbalance and discrimination\nreinforce each other", RED),
    ]
    for x, y, face, title, body, color in quadrants:
        ax.add_patch(
            patches.Rectangle(
                (x, y),
                1,
                1,
                linewidth=0.8,
                edgecolor=WHITE,
                facecolor=face,
            )
        )
        ax.add_patch(
            patches.Rectangle(
                (x + 0.06, y + 0.81),
                0.16,
                0.035,
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
            fontsize=9.0,
            fontweight="bold",
            va="center",
            linespacing=1.25,
        )

    ax.text(
        1.0,
        -0.12,
        "RULE FRAGMENTATION  |  F10 + F12",
        ha="center",
        va="center",
        color=INK,
        fontsize=7.6,
        fontweight="bold",
    )
    ax.text(
        -0.14,
        1.0,
        "CHINA SURPLUS  |  F09",
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
        "JOINT OUTCOME MAP",
        color=BLUE,
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
