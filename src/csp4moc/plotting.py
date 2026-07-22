"""Plotting helpers for CSP4MOC results."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure


def energy_density_plot(
    results: pd.DataFrame,
    energy_column: str = "energy",
    density_column: str = "density",
    title: str = "Energy vs density",
    **scatter_kwargs,
) -> Figure:
    """Plot energy against density and return a Plotly figure."""
    required_columns = {energy_column, density_column}
    missing_columns = required_columns.difference(results.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise KeyError(f"Missing required columns: {missing}")

    figure = px.scatter(
        results,
        x=density_column,
        y=energy_column,
        title=title,
        **scatter_kwargs,
    )
    figure.update_layout(
        xaxis_title=density_column,
        yaxis_title=energy_column,
    )

    return figure
