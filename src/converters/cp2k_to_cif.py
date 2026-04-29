#!/usr/bin/env python3
"""
Convert CP2K restart file to CIF format.
Handles both Cartesian and fractional (scaled) coordinates.

Usage:
    python cp2k_to_cif.py input.restart output.cif
    python cp2k_to_cif.py input.restart output.cif --scaled    # for fractional coords
    python cp2k_to_cif.py input.restart output.cif --no-scale  # for Cartesian (default)
"""

import argparse
import math
import sys
from pathlib import Path


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0])


def norm(v):
    return math.sqrt(dot(v, v))


def det(a, b, c):
    return dot(a, cross(b, c))


def cart_to_frac(r, A, B, C):
    """Convert Cartesian to fractional coordinates."""
    vol = det(A, B, C)
    if abs(vol) < 1e-12:
        raise RuntimeError("Zero volume cell")

    x = dot(r, cross(B, C)) / vol
    y = dot(r, cross(C, A)) / vol
    z = dot(r, cross(A, B)) / vol
    return x, y, z


def angle(v1, v2):
    return math.degrees(math.acos(dot(v1, v2) / (norm(v1) * norm(v2))))


def wrap(u, eps=1e-10):
    """Wrap coordinate into [0,1)."""
    u = u % 1.0
    if u < eps or u >= 1.0 - eps:
        u = 0.0
    return u


def parse_cp2k(filename):
    """Parse CP2K restart file to extract cell and coordinates."""
    A = B = C = None
    atoms = []
    scaled = False

    in_cell = False
    in_coord = False

    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # CELL section
            if line.upper().startswith("&CELL"):
                in_cell = True
                continue
            if in_cell and line.upper().startswith("&END"):
                in_cell = False
                continue

            if in_cell:
                p = line.split()
                if p[0] == "A":
                    A = tuple(map(float, p[1:4]))
                elif p[0] == "B":
                    B = tuple(map(float, p[1:4]))
                elif p[0] == "C":
                    C = tuple(map(float, p[1:4]))

            # COORD section
            if line.upper().startswith("&COORD"):
                in_coord = True
                continue
            if in_coord and line.upper().startswith("&END"):
                in_coord = False
                continue

            if in_coord:
                if line.upper().startswith("SCALED"):
                    scaled = line.split()[1].upper() == "T"
                    continue

                p = line.split()
                if len(p) >= 4:
                    el = p[0]
                    r = tuple(map(float, p[1:4]))
                    atoms.append((el, r))

    if not (A and B and C):
        raise RuntimeError("Cell vectors not found")
    if not atoms:
        raise RuntimeError("No atoms found")

    return A, B, C, atoms, scaled


def write_cif(outfile, A, B, C, atoms, scaled, title):
    """Write CIF file from parsed data."""
    a = norm(A)
    b = norm(B)
    c = norm(C)

    alpha = angle(B, C)
    beta = angle(A, C)
    gamma = angle(A, B)

    with open(outfile, "w") as f:
        f.write(f"data_{title}\n")
        f.write("_audit_creation_method  'CP2K -> CIF'\n\n")

        f.write(f"_cell_length_a    {a:.6f}\n")
        f.write(f"_cell_length_b    {b:.6f}\n")
        f.write(f"_cell_length_c    {c:.6f}\n")
        f.write(f"_cell_angle_alpha {alpha:.6f}\n")
        f.write(f"_cell_angle_beta  {beta:.6f}\n")
        f.write(f"_cell_angle_gamma {gamma:.6f}\n\n")

        f.write("_space_group_name_H-M_alt  'P 1'\n")
        f.write("_space_group_IT_number    1\n\n")

        f.write("loop_\n")
        f.write("_atom_site_label\n")
        f.write("_atom_site_type_symbol\n")
        f.write("_atom_site_fract_x\n")
        f.write("_atom_site_fract_y\n")
        f.write("_atom_site_fract_z\n")

        counts = {}

        for el, r in atoms:
            if scaled:
                x, y, z = r
            else:
                x, y, z = cart_to_frac(r, A, B, C)

            # Wrap coordinates into [0,1)
            x = wrap(x)
            y = wrap(y)
            z = wrap(z)

            counts[el] = counts.get(el, 0) + 1
            label = f"{el}{counts[el]}"

            f.write(f"{label:6s} {el:2s} {x:.8f} {y:.8f} {z:.8f}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert CP2K restart file to CIF format'
    )
    parser.add_argument('input', help='Input CP2K restart file')
    parser.add_argument('output', help='Output CIF file')
    parser.add_argument('--scaled', action='store_true',
                        help='Treat coordinates as fractional (SCALED T)')
    parser.add_argument('--no-scale', action='store_true',
                        help='Convert Cartesian to fractional (default)')

    args = parser.parse_args()

    infile = Path(args.input)
    outfile = Path(args.output)

    A, B, C, atoms, file_scaled = parse_cp2k(infile)

    # Determine if we should treat as scaled
    # CLI flag overrides file setting
    if args.scaled:
        use_scaled = True
    elif args.no_scale:
        use_scaled = False
    else:
        use_scaled = file_scaled

    write_cif(outfile, A, B, C, atoms, use_scaled, infile.stem)

    print(f"Converted: {infile} -> {outfile}")
    print(f"Mode: {'scaled (fractional)' if use_scaled else 'Cartesian -> fractional'}")
