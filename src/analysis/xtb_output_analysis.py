'''Analyses output files (long .xyz files) produced by xtb calculations and
extracts the energy values from them, then stores them in a csv.
'''
import pandas as pd
from pathlib import Path

# Configuration
file_path_dir = Path(r'C:\Users\aleon\OneDrive\Desktop\xtb_SO3_NMe4')
csv_name = 'xtb_energies_SO3_NMe4.csv'
num_conformations = 100


def find_energy(file_path: str) -> float | None:
    """Extract energy value from an xtb output xyz file."""
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('energy:'):
                    return float(line.split()[1])
        print(f"No line starting with 'energy:' found in {file_path}.")
        return None
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as error:
        print(f"An error occurred: {error}")
        return None


energy_dict = {}

for file_num in range(1, num_conformations + 1):
    file_path = file_path_dir / str(file_num) / 'xtbopt.xyz'
    energy_value = find_energy(str(file_path))
    if energy_value:
        energy_dict[file_num] = energy_value

energy_df = pd.DataFrame(energy_dict.items(), columns=['Conformation no.', 'Energy/ Eh'])
energy_df.sort_values(by='Energy/ Eh', inplace=True)
energy_df.to_csv(csv_name, index=False)
print(f"Saved energies to {csv_name}")


