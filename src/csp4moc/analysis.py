"""Analysis helpers for CSP4MOC results."""

from __future__ import annotations

from pathlib import Path
from typing import Union

import pandas as pd

from .io import (
    extract_gulp_energy,
    extract_xtb_energy,
    parse_output_directory,
)

PathLike = Union[str, Path]


def load_gulp_results(
    directory: PathLike,
    pattern: str = "*.gout",
    recursive: bool = True,
) -> pd.DataFrame:
    """Load GULP energies from matching output files."""
    return parse_output_directory(
        directory=directory,
        pattern=pattern,
        parser=extract_gulp_energy,
        recursive=recursive,
    )


def load_xtb_results(
    directory: PathLike,
    pattern: str = "*.xyz",
    recursive: bool = True,
) -> pd.DataFrame:
    """Load xTB energies from matching output files."""
    return parse_output_directory(
        directory=directory,
        pattern=pattern,
        parser=extract_xtb_energy,
        recursive=recursive,
    )


def rank_structures(
    results: pd.DataFrame,
    energy_column: str = "energy",
    ascending: bool = True,
) -> pd.DataFrame:
    """Return results sorted by energy with missing energies removed."""
    if energy_column not in results.columns:
        raise KeyError(f"Missing required column: {energy_column}")

    return (
        results.dropna(subset=[energy_column])
        .sort_values(energy_column, ascending=ascending)
        .reset_index(drop=True)
    )


def add_relative_energy(
    results: pd.DataFrame,
    energy_column: str = "energy",
    output_column: str = "relative_energy",
) -> pd.DataFrame:
    """Add energy relative to the lowest-energy row."""
    if energy_column not in results.columns:
        raise KeyError(f"Missing required column: {energy_column}")

    result = results.copy()
    valid_energies = result[energy_column].dropna()

    if valid_energies.empty:
        result[output_column] = pd.NA
    else:
        result[output_column] = result[energy_column] - valid_energies.min()

    return result


def filter_energy_window(
    results: pd.DataFrame,
    maximum_relative_energy: float,
    energy_column: str = "relative_energy",
) -> pd.DataFrame:
    """Keep structures within a relative energy window."""
    if energy_column not in results.columns:
        raise KeyError(f"Missing required column: {energy_column}")

    return results[
        results[energy_column].le(maximum_relative_energy)
    ].reset_index(drop=True)
