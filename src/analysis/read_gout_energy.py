"""Read energy and density from GULP .gout output files.
Used to process outputs from UFF4MOF, UFF rigid, and GFN-FF optimizations.
Can handle different file naming conventions based on mode."""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path

# Configuration
base_dir = Path(r'C:\Users\aleon\OneDrive\Desktop\so3_nme4_4_units')
output_csv = 'energies.csv'
num_structures = 1000
num_space_groups = 100

# System name prefix (e.g., 'xtal_SO3_Na', 'xtal_SO3_NMe4')
sys_name = 'xtal_SO3_NMe4'

# Mode: 'simple' for xtal_OH_optimized_{n}/gulp_opt.ginout
#       'spg'    for xtal_SO3_NMe4_sg_{sg}_{n}.gout
#       'idx'    for {sys_name}_sg_{sg}_{n}_{idx}_new.gout
mode = 'spg'

# Extract density (only applies to 'spg' and 'idx' modes)
extract_density = True

# Number of indices (for 'idx' mode)
num_indices = 1

# Specific space groups to process (None = all)
space_groups = None  # e.g., [1, 2, 3, 9, 14, 19, 33]


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
    
    if not energy_dic:
        return None
    
    return list(energy_dic.values())[-1]


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


def plot_convergence(energy_dic: dict, label: str):
    """Plot energy convergence for a single structure."""
    x_values = list(energy_dic.keys())
    y_values = list(energy_dic.values())
    plt.plot(x_values, y_values, label=label)


# Process files based on mode
final_energies = {}
densities = {}

if mode == 'simple':
    for x in range(1, num_structures + 1):
        file_path = base_dir / f'xtal_OH_optimized_{x}' / 'gulp_opt.ginout'
        energy = read_energy_gout(file_path)
        if energy is not None:
            final_energies[x] = energy

elif mode == 'spg':
    sg_list = space_groups if space_groups else range(1, num_space_groups + 1)
    
    for sg in sg_list:
        # Check if first file exists to verify space group
        if not (base_dir / f'{sys_name}_sg_{sg}_1.gout').exists():
            continue
        
        sg_energies = {}
        sg_densities = {}
        
        for n in range(1, num_structures + 1):
            file_path = base_dir / f'{sys_name}_sg_{sg}_{n}.gout'
            energy = read_energy_gout(file_path)
            if energy is not None:
                sg_energies[n] = energy
                if extract_density:
                    density = read_density_gout(file_path)
                    if density is not None:
                        sg_densities[n] = density
        
        if sg_energies:
            # Ensure all keys are aligned
            all_keys = set(sg_energies.keys()).union(sg_densities.keys()) if extract_density else sg_energies.keys()
            for key in all_keys:
                sg_energies.setdefault(key, np.nan)
                sg_densities.setdefault(key, np.nan)
            
            # Save per space group
            if extract_density and sg_densities:
                df = pd.DataFrame({
                    'Energies': [sg_energies[k] for k in all_keys],
                    'Densities': [sg_densities[k] for k in all_keys]
                }, index=list(all_keys))
            else:
                df = pd.DataFrame({
                    'Energies': list(sg_energies.values())
                }, index=list(sg_energies.keys()))
            
            df = df.sort_values(by=df.columns[0])
            prefix = sys_name.replace('xtal_', '')
            df.to_csv(f'{prefix}_{sg}.csv')
            print(f"Saved space group {sg} to {prefix}_{sg}.csv")

elif mode == 'idx':
    sg_list = space_groups if space_groups else [1, 2, 3, 9, 14, 19, 33]
    
    for sg in sg_list:
        for n in range(1, num_structures + 1):
            for idx in range(1, num_indices + 1):
                file_path = base_dir / f'{sys_name}_sg_{sg}_{n}_{idx}_new.gout'
                key = f'{n}_{idx}'
                
                energy = read_energy_gout(file_path)
                if energy is not None:
                    final_energies[key] = energy
                    if extract_density:
                        density = read_density_gout(file_path)
                        if density is not None:
                            densities[key] = density
        
        if final_energies:
            # Ensure all keys are aligned
            all_keys = set(final_energies.keys()).union(densities.keys())
            for key in all_keys:
                final_energies.setdefault(key, np.nan)
                densities.setdefault(key, np.nan)
            
            # Save per space group
            prefix = sys_name.replace('xtal_', '')
            df = pd.DataFrame({
                'Energies': [final_energies[k] for k in all_keys],
                'Densities': [densities[k] for k in all_keys]
            }, index=list(all_keys))
            df = df.sort_values(by='Energies')
            df.to_csv(f'{prefix}_{sg}.csv')
            print(f"Saved space group {sg} to {prefix}_{sg}.csv")
            
            final_energies.clear()
            densities.clear()

# Concatenate all CSV files if in spg/idx mode
if mode in ('spg', 'idx'):
    prefix = sys_name.replace('xtal_', '')
    sg_list = space_groups if space_groups else range(1, num_space_groups + 1)
    csv_files = [f'{prefix}_{sg}.csv' for sg in sg_list if (Path(f'{prefix}_{sg}.csv').exists())]
    
    if csv_files:
        concat_df = pd.concat([pd.read_csv(f) for f in csv_files], axis=1)
        concat_df.to_csv(f'{prefix}_all_sg.csv')
        print(f"Concatenated {len(csv_files)} files to {prefix}_all_sg.csv")

# Save overall results if in simple mode
if mode == 'simple' and final_energies:
    df = pd.DataFrame(final_energies.values(), index=list(final_energies.keys()))
    df = df.sort_values(by=df.columns[0])
    df.to_csv(output_csv)
    print(f"Saved energies to {output_csv}")

plt.legend(loc='upper right', bbox_to_anchor=(1, 1), ncol=5, prop={'size': 5})
plt.tight_layout()
plt.show()