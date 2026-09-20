"""Integration tests for plot generation and saving."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from analysis import prepare_calls
from main import save_plots


def plotting_calls() -> pd.DataFrame:
    """Return enough varied data to exercise heatmaps and cluster maps."""
    timestamps = pd.date_range("2020-01-01", periods=24 * 90, freq="h")
    timestamps = timestamps[
        [
            (timestamp.dayofweek * 3 + timestamp.hour + timestamp.month) % 7 != 0
            for timestamp in timestamps
        ]
    ]
    reasons = ("EMS", "Fire", "Traffic")
    row_count = len(timestamps)
    source = pd.DataFrame(
        {
            "lat": [40.1] * row_count,
            "lng": [-75.2] * row_count,
            "desc": ["Synthetic call"] * row_count,
            "zip": [19401 + index % 5 for index in range(row_count)],
            "title": [f"{reasons[index % 3]}: TEST" for index in range(row_count)],
            "timeStamp": timestamps,
            "twp": [f"Township {index % 6}" for index in range(row_count)],
            "addr": ["Test address"] * row_count,
            "e": [1] * row_count,
        }
    )
    return prepare_calls(source)


class PlotPipelineTests(unittest.TestCase):
    def test_save_plots_creates_every_plot_and_closes_figures(self) -> None:
        expected_names = {
            "calls_by_reason.png",
            "calls_by_weekday.png",
            "calls_by_month.png",
            "monthly_trend.png",
            "monthly_regression.png",
            "daily_calls.png",
            "weekday_hour_heatmap.png",
            "weekday_hour_clustermap.png",
            "weekday_month_heatmap.png",
            "weekday_month_clustermap.png",
            "daily_calls_ems.png",
            "daily_calls_fire.png",
            "daily_calls_traffic.png",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            plot_count = save_plots(plotting_calls(), output_dir)
            generated_names = {path.name for path in output_dir.glob("*.png")}

        self.assertEqual(plot_count, len(expected_names))
        self.assertEqual(generated_names, expected_names)
        self.assertEqual(plt.get_fignums(), [])


if __name__ == "__main__":
    unittest.main()
