"""Tests for data loading, feature engineering, and aggregations."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from analysis import (
    DAY_ORDER,
    calls_by_month,
    calls_by_weekday_hour,
    load_calls,
    prepare_calls,
    summarize_calls,
)


def sample_calls() -> pd.DataFrame:
    """Return a small source-format dataset spanning a year boundary."""
    return pd.DataFrame(
        {
            "lat": [40.1, 40.2, 40.3],
            "lng": [-75.1, -75.2, -75.3],
            "desc": ["Call one", "Call two", "Call three"],
            "zip": [19401, 19401, 19402],
            "title": ["EMS: TEST", "Fire: TEST", "Traffic: TEST"],
            "timeStamp": [
                "2015-12-31 23:00:00",
                "2016-01-01 00:00:00",
                "2016-01-02 12:00:00",
            ],
            "twp": ["A", "A", "B"],
            "addr": ["1 Main St", "2 Main St", "3 Main St"],
            "e": [1, 1, 1],
        }
    )


class AnalysisTests(unittest.TestCase):
    def test_prepare_calls_adds_features_without_mutating_source(self) -> None:
        source = sample_calls()
        prepared = prepare_calls(source)

        self.assertEqual(source["timeStamp"].dtype, object)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(prepared["timeStamp"]))
        self.assertEqual(prepared["reason"].tolist(), ["EMS", "Fire", "Traffic"])
        self.assertEqual(prepared["hour"].tolist(), [23, 0, 12])
        self.assertEqual(prepared["day_of_week"].tolist(), ["Thu", "Fri", "Sat"])

    def test_monthly_counts_remain_chronological_across_years(self) -> None:
        monthly = calls_by_month(prepare_calls(sample_calls()))

        self.assertEqual(monthly.index.astype(str).tolist(), ["2015-12", "2016-01"])
        self.assertEqual(monthly.tolist(), [1, 2])

    def test_weekday_hour_table_has_stable_shape_and_order(self) -> None:
        table = calls_by_weekday_hour(prepare_calls(sample_calls()))

        self.assertEqual(table.index.tolist(), DAY_ORDER)
        self.assertEqual(table.columns.tolist(), list(range(24)))
        self.assertEqual(table.shape, (7, 24))
        self.assertEqual(int(table.to_numpy().sum()), 3)

    def test_summary_matches_source_data(self) -> None:
        summary = summarize_calls(prepare_calls(sample_calls()), top_n=1)

        self.assertEqual(summary["row_count"], 3)
        self.assertEqual(summary["unique_titles"], 3)
        self.assertEqual(summary["top_townships"].index.tolist(), ["A"])

    def test_load_calls_rejects_missing_columns(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "invalid.csv"
            pd.DataFrame({"title": ["EMS: TEST"]}).to_csv(csv_path, index=False)

            with self.assertRaisesRegex(ValueError, "missing required columns"):
                load_calls(csv_path)


if __name__ == "__main__":
    unittest.main()
