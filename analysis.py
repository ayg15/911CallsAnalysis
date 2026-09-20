"""Data loading, feature engineering, and aggregations for 911 call data."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


REQUIRED_COLUMNS = {
    "lat",
    "lng",
    "desc",
    "zip",
    "title",
    "timeStamp",
    "twp",
    "addr",
    "e",
}
DAY_ORDER = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def load_calls(csv_path: str | Path) -> pd.DataFrame:
    """Load a 911 calls CSV file and validate the expected source columns."""
    path = Path(csv_path)
    if not path.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {path}. Download 911.csv as described in README.md."
        )

    calls = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(calls.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(sorted(missing))}")
    return calls


def prepare_calls(calls: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of the data with the notebook's derived features added."""
    missing = REQUIRED_COLUMNS.difference(calls.columns)
    if missing:
        raise ValueError(f"Data is missing required columns: {', '.join(sorted(missing))}")

    prepared = calls.copy()
    prepared["timeStamp"] = pd.to_datetime(prepared["timeStamp"], errors="raise")
    prepared["reason"] = prepared["title"].str.partition(":")[0].str.strip()
    prepared["hour"] = prepared["timeStamp"].dt.hour
    prepared["month"] = prepared["timeStamp"].dt.month
    prepared["day_of_week"] = prepared["timeStamp"].dt.dayofweek.map(
        dict(enumerate(DAY_ORDER))
    )
    prepared["date"] = prepared["timeStamp"].dt.date
    return prepared


def summarize_calls(calls: pd.DataFrame, top_n: int = 5) -> dict[str, Any]:
    """Return the headline statistics shown in the original notebook."""
    return {
        "row_count": len(calls),
        "unique_titles": int(calls["title"].nunique()),
        "top_zip_codes": calls["zip"].value_counts().head(top_n),
        "top_townships": calls["twp"].value_counts().head(top_n),
        "calls_by_reason": calls["reason"].value_counts(),
    }


def calls_by_month(calls: pd.DataFrame) -> pd.Series:
    """Count calls by chronological year-month periods."""
    periods = calls["timeStamp"].dt.to_period("M")
    return calls.groupby(periods).size().sort_index().rename("calls")


def calls_by_date(calls: pd.DataFrame, reason: str | None = None) -> pd.Series:
    """Count calls by date, optionally filtered to one reason."""
    selected = calls if reason is None else calls[calls["reason"] == reason]
    return selected.groupby("date").size().sort_index().rename("calls")


def calls_by_weekday_hour(calls: pd.DataFrame) -> pd.DataFrame:
    """Build the weekday-by-hour table used by the heatmaps."""
    table = calls.pivot_table(
        index="day_of_week", columns="hour", values="reason", aggfunc="count", fill_value=0
    )
    return table.reindex(index=DAY_ORDER, columns=range(24), fill_value=0)


def calls_by_weekday_month(calls: pd.DataFrame) -> pd.DataFrame:
    """Build the weekday-by-month table used by the heatmaps."""
    table = calls.pivot_table(
        index="day_of_week", columns="month", values="reason", aggfunc="count", fill_value=0
    )
    return table.reindex(index=DAY_ORDER, fill_value=0)
