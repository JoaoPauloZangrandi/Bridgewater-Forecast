"""Build original figures used in the submission.

The figures contain no scraped artwork. Values come from the source ledger and
the scenario matrix; they are intentionally simple enough to audit by eye.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import patches
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated"
SCENARIOS = ROOT / "data" / "scenario_matrix.csv"

INK = "#13222f"
BLUE = "#2f6f91"
TEAL = "#2f8077"
GOLD = "#c28a2c"
RED = "#a84f45"
PAPER = "#f7f7f4"
GRID = "#d8dde0"


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
    fig, ax = plt.subplots(figsize=(10.4, 4.2), facecolor=PAPER)
    ax.set_facecolor(PAPER)
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0, 4.2)
    ax.axis("off")

    nodes = [
        (0.15, 2.35, 1.75, 0.9, "AI capability\nand diffusion", BLUE),
        (2.25, 2.35, 1.75, 0.9, "Compute, power,\nmineral demand", TEAL),
        (4.35, 2.35, 1.75, 0.9, "Chokepoint rents\nand dependence", GOLD),
        (6.45, 2.35, 1.75, 0.9, "Subsidies, controls,\nlocalization", RED),
        (8.55, 2.35, 1.7, 0.9, "Duplicated capacity\nand higher cost", INK),
    ]
    for x, y, w, h, label, color in nodes:
        ax.add_patch(
            patches.FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="round,pad=0.02,rounding_size=0.04",
                linewidth=1.1,
                edgecolor=color,
                facecolor="white",
            )
        )
        ax.text(
            x + w / 2,
            y + h / 2,
            label,
            ha="center",
            va="center",
            color=INK,
            fontsize=9.3,
            fontweight="semibold",
        )

    for idx in range(len(nodes) - 1):
        x1, y1, w1, h1, *_ = nodes[idx]
        x2, y2, *_ = nodes[idx + 1]
        ax.annotate(
            "",
            xy=(x2 - 0.04, y2 + 0.45),
            xytext=(x1 + w1 + 0.04, y1 + 0.45),
            arrowprops=dict(arrowstyle="-|>", color="#65727b", lw=1.2),
        )

    ax.annotate(
        "",
        xy=(1.0, 2.28),
        xytext=(9.35, 2.28),
        arrowprops=dict(
            arrowstyle="-|>",
            color=RED,
            lw=1.25,
            connectionstyle="arc3,rad=-0.36",
        ),
    )
    ax.text(
        5.18,
        0.58,
        "Strategic rivalry raises the option value of domestic capability",
        ha="center",
        color=RED,
        fontsize=8.6,
        fontweight="semibold",
    )

    ax.annotate(
        "",
        xy=(2.52, 3.34),
        xytext=(8.75, 3.34),
        arrowprops=dict(
            arrowstyle="-|>",
            color=BLUE,
            lw=1.1,
            linestyle="--",
            connectionstyle="arc3,rad=0.12",
        ),
    )
    ax.text(
        5.55,
        4.00,
        "Counter-loop: efficiency, substitution, and weak returns reduce resource intensity",
        ha="center",
        color=BLUE,
        fontsize=8.4,
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
            ]
            for row in rows
        ]
    )

    fig, ax = plt.subplots(figsize=(7.0, 5.7), facecolor=PAPER)
    ax.set_facecolor(PAPER)
    image = ax.imshow(matrix, cmap="RdYlBu_r", vmin=10, vmax=95, aspect="auto")
    ax.set_xticks(range(3))
    ax.set_xticklabels(
        ["Abundant\nintelligence 25%", "Bottlenecked\nboom 50%", "Capex\nretrenchment 25%"],
        fontsize=8.3,
        color=INK,
    )
    ax.set_yticks(range(len(ids)))
    ax.set_yticklabels(ids, fontsize=8.2, color=INK)
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
                color="white" if value < 38 or value > 72 else INK,
                fontsize=8.2,
                fontweight="semibold",
            )

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(
        "Conditional probability by coherent macro scenario (%)",
        loc="left",
        fontsize=10.2,
        color=INK,
        fontweight="bold",
        pad=9,
    )
    bar = fig.colorbar(image, ax=ax, fraction=0.035, pad=0.04)
    bar.ax.tick_params(labelsize=7, length=2, colors=INK)
    bar.outline.set_visible(False)
    save(fig, "scenario_heatmap.png")


def evidence_dashboard() -> None:
    fig, axes = plt.subplots(1, 4, figsize=(10.6, 2.25), facecolor=PAPER)
    fig.subplots_adjust(wspace=0.35)

    panels = [
        ("U.S. firms using AI", 18, 35, 0, 45, "%", "2025/26 actual", "F02 threshold"),
        ("U.S. data-center power", 11.8, 12, 0, 16, "%", "2030 DOE midpoint", "F05 threshold"),
        ("Top refiner share", 72, 65, 0, 80, "%", "2025 actual", "F08 threshold"),
        ("Trade on MFN terms", 72, 65, 0, 85, "%", "early-2026 actual", "F10 threshold"),
    ]

    for ax, panel in zip(axes, panels):
        title, base, threshold, low, high, unit, base_label, threshold_label = panel
        ax.set_facecolor(PAPER)
        ax.set_xlim(low, high)
        ax.set_ylim(-0.3, 1.25)
        ax.hlines(0.48, low, high, color=GRID, linewidth=4)
        ax.scatter(base, 0.48, s=75, color=BLUE, zorder=3)
        ax.scatter(threshold, 0.48, s=85, marker="|", linewidth=3, color=RED, zorder=4)
        ax.text(
            base,
            0.78,
            f"{base:g}{unit}",
            ha="center",
            fontsize=8.7,
            color=BLUE,
            fontweight="bold",
        )
        ax.text(
            threshold,
            0.12,
            f"{threshold:g}{unit}",
            ha="center",
            fontsize=8.7,
            color=RED,
            fontweight="bold",
        )
        ax.text(
            0.01,
            -0.20,
            f"● {base_label}\n| {threshold_label}",
            transform=ax.transAxes,
            fontsize=6.8,
            color=INK,
            va="top",
        )
        ax.set_title(title, fontsize=8.7, color=INK, fontweight="semibold", pad=3)
        ax.set_yticks([])
        ax.set_xticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    save(fig, "evidence_dashboard.png")


def main() -> None:
    causal_loop()
    scenario_heatmap()
    evidence_dashboard()
    print("Built causal_loop.png, scenario_heatmap.png, evidence_dashboard.png")


if __name__ == "__main__":
    main()
