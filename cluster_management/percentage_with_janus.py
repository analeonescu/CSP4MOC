"""
Calculate the percentage of structures that have been optimized with Janus.

Usage:
    python percentage_with_janus.py [--system SYS_NAME] [--directory DIR]

Defaults: system='xtal_SO3_NMe4', directory='./'
"""

import argparse
import os
from pathlib import Path


def count_files(directory: Path, prefix: str, suffix: str) -> int:
    """Count files matching prefix and suffix in a directory."""
    return sum(1 for f in os.listdir(directory) if f.startswith(prefix) and f.endswith(suffix))


def main(system_name: str = "xtal_SO3_NMe4", directory: str = ".") -> None:
    """Calculate and display the percentage of optimized structures."""
    directory = Path(directory)
    
    if not directory.is_dir():
        print(f"Error: {directory} is not a valid directory")
        return

    ext_xyz_count = count_files(directory, system_name, ".extxyz")
    cif_count = count_files(directory, system_name, ".cif")

    if cif_count == 0:
        print(f"No .cif files found for system '{system_name}' in {directory}")
        return

    percentage = round(ext_xyz_count / cif_count * 100, 2)
    
    # print(f"System: {system_name}")
    # print(f"Directory: {directory.resolve()}")
    # print(f"Optimized (.extxyz): {ext_xyz_count}")
    # print(f"Total (.cif): {cif_count}")
    print(f"Percentage: {percentage}%")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--system", "-s", default="xtal_SO3_NMe4", help="System name prefix")
    parser.add_argument("--directory", "-d", default=".", help="Directory to search")
    args = parser.parse_args()
    
    main(args.system, args.directory)