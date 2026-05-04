"""
Read energy and density from GULP .gout output files.
Used to process outputs from UFF4MOF, UFF rigid, and GFN-FF optimizations.
Can handle different file naming conventions based on mode.

Modes:
    'simple' : {sys_name}_optimized_{n}.gout
    'spg'    : {sys_name}_sg_{spg}_{n}.gout
    'idx'    : {sys_name}_sg_{spg}_{n}_{idx}_new.gout
"""

import pandas as pd
from pathlib import Path

base_dir = Path(r'C:\Users\aleon\OneDrive\Desktop\so3_nme4_4_units')
output_csv = 'energies.csv'
num_structures = 1000
num_space_groups = 100
sys_name = 'xtal_SO3_NMe4'

mode = 'spg'
extract_density = True
num_indices = 1
spgs = None  # e.g., [1, 2, 3, 9, 14, 19, 33]


def read_energy_gout(file_path: Path) -> float | None:
    """Extract final energy from GULP .gout file."""
    energy_dic = {}

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line_list = line.split()
                if len(line_list) > 0 and 'Cycle:' in line_list:
                    if 'Gnorm:**************' not in line:
                        try:
                            energy_dic[int(line_list[1])] = float(line_list[3])
                        except (ValueError, IndexError):
                            pass
    except FileNotFoundError:
        return None

    return list(energy_dic.values())[-1] if energy_dic else None


def read_density_gout(file_path: Path) -> float | None:
    """Extract density from GULP .gout file."""
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if 'Density' in line:
                    line_list = line.split()
                    for i, token in enumerate(line_list):
                        if token == 'Density' and i + 1 < len(line_list):
                            return float(line_list[i + 1])
    except FileNotFoundError:
        pass
    return None


final_energies = {}
densities = {}
saved_csvs = []

if mode == 'simple':
    for x in range(1, num_structures + 1):
        file_path = base_dir / f'xtal_OH_optimized_{x}' / 'gulp_opt.ginout'
        energy = read_energy_gout(file_path)
        if energy is not None:
            final_energies[x] = energy

elif mode == 'spg':
    sg_list = spgs if spgs else range(1, num_space_groups + 1)

    for sg in sg_list:
        if not (base_dir / f'{sys_name}_sg_{sg}_1.gout').exists():
            continue

        spg_energies = {}
        spg_densities = {}

        for n in range(1, num_structures + 1):
            file_path = base_dir / f'{sys_name}_sg_{sg}_{n}.gout'
            energy = read_energy_gout(file_path)
            if energy is not None:
                spg_energies[n] = energy
                if extract_density:
                    density = read_density_gout(file_path)
                    if density is not None:
                        spg_densities[n] = density

        if spg_energies:
            # Build DataFrame aligned on index — pandas handles missing keys as NaN
            df = pd.DataFrame({'Energies': spg_energies, 'Densities': spg_densities})
            df = df.sort_values(by='Energies')
            prefix = sys_name.replace('xtal_', '')
            out = f'{prefix}_{sg}.csv'
            df.to_csv(out)
            saved_csvs.append(out)
            print(f"Saved space group {sg} to {out}")

elif mode == 'idx':
    spg_list = spgs if spgs else [1, 2, 3, 9, 14, 19, 33]

    for spg in spg_list:
        final_energies = {}
        densities = {}

        for n in range(1, num_structures + 1):
            for idx in range(1, num_indices + 1):
                file_path = base_dir / f'{sys_name}_sg_{spg}_{n}_{idx}_new.gout'
                key = f'{n}_{idx}'
                energy = read_energy_gout(file_path)
                if energy is not None:
                    final_energies[key] = energy
                    if extract_density:
                        density = read_density_gout(file_path)
                        if density is not None:
                            densities[key] = density

        if final_energies:
            # Build DataFrame aligned on index — pandas handles missing keys as NaN
            df = pd.DataFrame({'Energies': final_energies, 'Densities': densities})
            df = df.sort_values(by='Energies')
            prefix = sys_name.replace('xtal_', '')
            out = f'{prefix}_{spg}.csv'
            df.to_csv(out)
            saved_csvs.append(out)
            print(f"Saved space group {spg} to {out}")

# save results

if mode in ('spg', 'idx') and saved_csvs:
    prefix = sys_name.replace('xtal_', '')
    concat_df = pd.concat([pd.read_csv(f) for f in saved_csvs], axis=1)
    concat_df.to_csv(f'{prefix}_all_sg.csv')
    print(f"Concatenated {len(saved_csvs)} files to {prefix}_all_sg.csv")

elif mode == 'simple' and final_energies:
    df = pd.DataFrame({'Energies': final_energies})
    df = df.sort_values(by='Energies')
    df.to_csv(output_csv)
    print(f"Saved energies to {output_csv}")