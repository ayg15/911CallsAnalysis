"""Plotting functions for the 911 calls analysis."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure

from analysis import (
    DAY_ORDER,
    calls_by_date,
    calls_by_month,
    calls_by_weekday_hour,
    calls_by_weekday_month,
)


def _finish_axes(ax: plt.Axes, title: str, xlabel: str, ylabel: str) -> Figure:
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.figure.tight_layout()
    return ax.figure


def plot_calls_by_reason(calls: pd.DataFrame) -> Figure:
    """Plot the total number of calls for each reason."""
    fig, ax = plt.subplots(figsize=(8, 5))
    order = calls["reason"].value_counts().index
    sns.countplot(
        data=calls,
        x="reason",
        hue="reason",
        order=order,
        palette="viridis",
        legend=False,
        ax=ax,
    )
    return _finish_axes(ax, "911 calls by reason", "Reason", "Calls")


def plot_calls_by_weekday(calls: pd.DataFrame) -> Figure:
    """Plot weekday totals split by call reason."""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(
        data=calls,
        x="day_of_week",
        hue="reason",
        order=DAY_ORDER,
        palette="viridis",
        ax=ax,
    )
    ax.legend(title="Reason", bbox_to_anchor=(1.02, 1), loc="upper left")
    return _finish_axes(ax, "911 calls by weekday", "Day of week", "Calls")


def plot_calls_by_month(calls: pd.DataFrame) -> Figure:
    """Plot monthly totals split by call reason."""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=calls, x="month", hue="reason", palette="viridis", ax=ax)
    ax.legend(title="Reason", bbox_to_anchor=(1.02, 1), loc="upper left")
    return _finish_axes(ax, "911 calls by month", "Month", "Calls")


def plot_monthly_trend(calls: pd.DataFrame) -> Figure:
    """Plot total calls along a chronological monthly timeline."""
    monthly = calls_by_month(calls)
    fig, ax = plt.subplots(figsize=(10, 5))
    positions = range(len(monthly))
    ax.plot(positions, monthly.to_numpy(), marker="o")
    ax.set_xticks(list(positions), monthly.index.astype(str), rotation=45, ha="right")
    return _finish_axes(ax, "Monthly call volume", "Year-month", "Calls")


def plot_monthly_regression(calls: pd.DataFrame) -> Figure:
    """Plot a linear fit against chronologically ordered months."""
    monthly = calls_by_month(calls)
    regression_data = pd.DataFrame(
        {"month_index": range(len(monthly)), "calls": monthly.to_numpy()}
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.regplot(data=regression_data, x="month_index", y="calls", ax=ax)
    ax.set_xticks(
        regression_data["month_index"], monthly.index.astype(str), rotation=45, ha="right"
    )
    return _finish_axes(
        ax, "Monthly call volume with linear fit", "Year-month", "Calls"
    )


def plot_daily_calls(calls: pd.DataFrame, reason: str | None = None) -> Figure:
    """Plot daily call volume for all calls or one reason."""
    daily = calls_by_date(calls, reason)
    fig, ax = plt.subplots(figsize=(11, 5))
    daily.plot(ax=ax)
    title = "Daily 911 call volume" if reason is None else f"Daily {reason} call volume"
    return _finish_axes(ax, title, "Date", "Calls")


def plot_weekday_hour_heatmap(calls: pd.DataFrame) -> Figure:
    """Plot call volume by weekday and hour."""
    fig, ax = plt.subplots(figsize=(11, 7))
    sns.heatmap(calls_by_weekday_hour(calls), cmap="viridis", ax=ax)
    return _finish_axes(ax, "Calls by weekday and hour", "Hour", "Day of week")


def plot_weekday_hour_clustermap(calls: pd.DataFrame) -> Figure:
    """Cluster weekdays and hours by their call-volume profiles."""
    grid = sns.clustermap(calls_by_weekday_hour(calls), cmap="viridis", figsize=(11, 9))
    grid.fig.suptitle("Clustered calls by weekday and hour", y=1.02)
    return grid.fig


def plot_weekday_month_heatmap(calls: pd.DataFrame) -> Figure:
    """Plot call volume by weekday and month."""
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(calls_by_weekday_month(calls), cmap="viridis", ax=ax)
    return _finish_axes(ax, "Calls by weekday and month", "Month", "Day of week")


def plot_weekday_month_clustermap(calls: pd.DataFrame) -> Figure:
    """Cluster weekdays and months by their call-volume profiles."""
    grid = sns.clustermap(calls_by_weekday_month(calls), cmap="viridis", figsize=(10, 8))
    grid.fig.suptitle("Clustered calls by weekday and month", y=1.02)
    return grid.fig
