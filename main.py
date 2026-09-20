"""Command-line entry point for the complete 911 calls analysis."""

from __future__ import annotations

import argparse
from collections.abc import Iterator
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

from analysis import load_calls, prepare_calls, summarize_calls
from visualizations import (
    plot_calls_by_month,
    plot_calls_by_reason,
    plot_calls_by_weekday,
    plot_daily_calls,
    plot_monthly_regression,
    plot_monthly_trend,
    plot_weekday_hour_clustermap,
    plot_weekday_hour_heatmap,
    plot_weekday_month_clustermap,
    plot_weekday_month_heatmap,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyse the Montgomery County 911 calls dataset."
    )
    parser.add_argument("csv_path", nargs="?", default="911.csv", help="path to the source CSV")
    parser.add_argument(
        "--output-dir", default="output", help="directory in which PNG plots are saved"
    )
    parser.add_argument("--show", action="store_true", help="also display plots interactively")
    return parser.parse_args()


def print_summary(summary: dict[str, object]) -> None:
    """Print the analysis headline statistics in a readable format."""
    print(f"Rows: {summary['row_count']:,}")
    print(f"Unique titles: {summary['unique_titles']:,}")
    for label, key in (
        ("Top ZIP codes", "top_zip_codes"),
        ("Top townships", "top_townships"),
        ("Calls by reason", "calls_by_reason"),
    ):
        print(f"\n{label}:\n{summary[key].to_string()}")


def iter_plots(calls: pd.DataFrame) -> Iterator[tuple[str, Figure]]:
    """Yield each visualization so callers need to hold only one at a time."""
    yield "calls_by_reason", plot_calls_by_reason(calls)
    yield "calls_by_weekday", plot_calls_by_weekday(calls)
    yield "calls_by_month", plot_calls_by_month(calls)
    yield "monthly_trend", plot_monthly_trend(calls)
    yield "monthly_regression", plot_monthly_regression(calls)
    yield "daily_calls", plot_daily_calls(calls)
    yield "weekday_hour_heatmap", plot_weekday_hour_heatmap(calls)
    yield "weekday_hour_clustermap", plot_weekday_hour_clustermap(calls)
    yield "weekday_month_heatmap", plot_weekday_month_heatmap(calls)
    yield "weekday_month_clustermap", plot_weekday_month_clustermap(calls)
    for reason in calls["reason"].dropna().unique():
        yield f"daily_calls_{reason.lower()}", plot_daily_calls(calls, reason)


def save_plots(calls: pd.DataFrame, output_dir: Path, show: bool = False) -> int:
    """Save every plot and close it immediately unless interactive display is requested."""
    output_dir.mkdir(parents=True, exist_ok=True)
    plot_count = 0
    for name, figure in iter_plots(calls):
        figure.savefig(output_dir / f"{name}.png", dpi=150, bbox_inches="tight")
        plot_count += 1
        if not show:
            plt.close(figure)

    if show:
        plt.show()
    return plot_count


def main() -> None:
    args = parse_args()
    calls = prepare_calls(load_calls(args.csv_path))
    print_summary(summarize_calls(calls))

    output_dir = Path(args.output_dir)
    plot_count = save_plots(calls, output_dir, show=args.show)
    print(f"\nSaved {plot_count} plots to {output_dir.resolve()}")


if __name__ == "__main__":
    main()
