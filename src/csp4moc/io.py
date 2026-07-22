"""Input/output helpers for CSP4MOC calculation results."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Callable, Iterable, List, Optional, Union

import pandas as pd
from ase import Atoms
from ase.io import read, write

PathLike = Union[str, Path]
EnergyParser = Callable[[str], Optional[float]]

AMU_PER_ANGSTROM3_TO_G_CM3 = 1.66053906660


def find_files(
    directory: PathLike,
    pattern: str,
    recursive: bool = False,
) -> List[Path]:
    """Return files matching pattern from a directory."""
    directory = Path(directory)

    if recursive:
        return sorted(directory.rglob(pattern))

    return sorted(directory.glob(pattern))


def read_text_file(path: PathLike) -> str:
    """Read a text file using replacement for invalid characters."""
    return Path(path).read_text(encoding="utf-8", errors="replace")


def read_structure(path: PathLike, index: Union[int, str] = -1) -> Atoms:
    """Read one structure with ASE."""
    return read(path, index=index)


def read_structures(
    paths: Iterable[PathLike],
    index: Union[int, str] = -1,
) -> List[Atoms]:
    """Read one structure from each path with ASE."""
    return [read_structure(path, index=index) for path in paths]


def write_extxyz(
    structures: Iterable[Atoms],
    output_path: PathLike,
) -> None:
    """Write structures to an extended XYZ file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write(output_path, list(structures), format="extxyz")


def extract_last_float(
    text: str,
    patterns: Iterable[str],
) -> Optional[float]:
    """Extract the final floating-point value matching any pattern."""
    matches = []

    for pattern in patterns:
        matches.extend(re.findall(pattern, text, flags=re.IGNORECASE))

    if not matches:
        return None

    return float(matches[-1])


def extract_gulp_energy(text: str) -> Optional[float]:
    """Extract the final energy from GULP output text."""
    energies = {}

    for line in text.splitlines():
        fields = line.split()
        if "Cycle:" not in fields or "Gnorm:**************" in line:
            continue

        try:
            energies[int(fields[1])] = float(fields[3])
        except (ValueError, IndexError):
            continue

    return list(energies.values())[-1] if energies else None


def read_energy_gout(file_path: PathLike) -> Optional[float]:
    """Extract final energy from a GULP .gout file."""
    try:
        return extract_gulp_energy(read_text_file(file_path))
    except FileNotFoundError:
        return None


def extract_gulp_density(text: str) -> Optional[float]:
    """Extract density from GULP output text."""
    for line in text.splitlines():
        fields = line.split()
        for index, token in enumerate(fields):
            if token == "Density" and index + 1 < len(fields):
                try:
                    return float(fields[index + 1])
                except ValueError:
                    continue

    return None


def read_density_gout(file_path: PathLike) -> Optional[float]:
    """Extract density from a GULP .gout file."""
    try:
        return extract_gulp_density(read_text_file(file_path))
    except FileNotFoundError:
        return None


def extract_xtb_energy(text: str) -> Optional[float]:
    """Extract energy from xTB XYZ metadata in Hartree."""
    for line in text.splitlines():
        fields = line.split()
        if fields and fields[0] == "energy:":
            try:
                return float(fields[1])
            except (ValueError, IndexError):
                return None

    return None


def find_energy(file_path: PathLike) -> Optional[float]:
    """Extract energy from an xTB output file."""
    try:
        return extract_xtb_energy(read_text_file(file_path))
    except FileNotFoundError:
        return None


def extract_energy_from_extxyz(text: str) -> Optional[float]:
    """Extract the final energy value from EXTXYZ metadata."""
    energy = None

    for match in re.finditer(
        r"energy\s*=\s*([-+]?\d*\.?\d+(?:[Ee][-+]?\d+)?)",
        text,
        flags=re.IGNORECASE,
    ):
        energy = float(match.group(1))

    return energy


def read_extxyz_energy(file_path: PathLike) -> Optional[float]:
    """Extract the final energy value from an EXTXYZ file."""
    try:
        return extract_energy_from_extxyz(read_text_file(file_path))
    except FileNotFoundError:
        return None


def get_spg(file_path: PathLike, default: int = 1) -> int:
    """Extract the space group number from a file name."""
    match = re.search(r"spg_(\d+)", str(file_path), flags=re.IGNORECASE)
    return int(match.group(1)) if match else default


def calculate_density(atoms: Atoms) -> Optional[float]:
    """Calculate density in g/cm^3 from an ASE Atoms object."""
    volume = atoms.get_volume()
    if volume <= 0:
        return None

    total_mass = atoms.get_masses().sum()
    return float(total_mass / volume * AMU_PER_ANGSTROM3_TO_G_CM3)


def get_density(file_path: PathLike) -> Optional[float]:
    """Read a structure and calculate its density in g/cm^3."""
    try:
        return calculate_density(read_structure(file_path))
    except (FileNotFoundError, OSError, ValueError):
        return None


def parse_output_file(
    path: PathLike,
    parser: EnergyParser,
) -> dict:
    """Parse one text output file using the supplied parser."""
    path = Path(path)
    return {"path": str(path), "energy": parser(read_text_file(path))}


def parse_output_directory(
    directory: PathLike,
    pattern: str,
    parser: EnergyParser,
    recursive: bool = True,
) -> pd.DataFrame:
    """Parse matching text output files into a pandas DataFrame."""
    records = []

    for path in find_files(directory, pattern, recursive=recursive):
        try:
            records.append(parse_output_file(path, parser))
        except OSError:
            records.append({"path": str(path), "energy": None})

    return pd.DataFrame(records, columns=["path", "energy"])
