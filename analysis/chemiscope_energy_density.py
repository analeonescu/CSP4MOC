'''
This script reads .extxyz files, extracts energy values, calculates density, and identifies space groups
from file names. It then compiles this information into a .json file for visualisation with Chemiscope.'''
import chemiscope
import ase.io
import re
import glob


def extract_energy_from_extxyz(file_path):
    """
    Extract energy values from a .extxyz file.

    Parameters:
        file_path (str): Path to the .extxyz file.

    Returns:
        list: A list of energy values (float) extracted from the file.
    """

    with open(file_path, 'r') as file:
        energy = None
        for line in file:
            # Look for lines containing the 'Energy=' pattern
            match = re.search(r'energy=([\-\d\.eE]+)', line)
            if match:
                energy = float(match.group(1))

    return energy

def get_spg(file_path):
    """
    Extracts the space group from the file name.

    Parameters:
        file_path (str): Path to the .extxyz file.

    Returns:
        int: The space group number extracted from the file name.
    """
    match = re.search(r'spg_(\d+)', file_path)
    if match is not None:
        return int(match.group(1))
    else:
        return 1

def get_density(file_path):
    try:
        atoms = ase.io.read(file_path)
        volume = atoms.get_volume()
        total_mass = atoms.get_masses().sum()  # density according to this is in amu/ Ang^3
        return total_mass/volume*1.66 
    except Exception as e:
        return 0

if __name__ == "__main__":
    files = sorted(glob.glob('*.extxyz'))

    all_structures = []
    energies = []
    densities = []
    spgs = []

    for file_path in files:
        atoms = ase.io.read(file_path)
        all_structures.append(atoms)

        energy = extract_energy_from_extxyz(file_path)
        density = get_density(file_path)
        spg = get_spg(file_path)

        energies.append(energy)
        densities.append(density)
        spgs.append(spg)

    with open("energies.txt", "w") as f:
        f.writelines(f"{e}\n" for e in energies)

    with open("densities.txt", "w") as f:
        f.writelines(f"{d}\n" for d in densities)

    with open("spg.txt", "w") as f:
        f.writelines(f"{s}\n" for s in spgs)

    properties = {
        "Total energy/eV": energies,
        "Density/ g cm^-3": densities,
        "Space group": {
            "target": "structure",
            "type": "string",
            "description": "Space group from filename",
            "values": spgs,
        }
    }

    chemiscope.write_input("structures.json", frames=all_structures, properties=properties)

    with open("chemiscope_standalone.html") as template, open("structures.json") as data, open("struct.html", "w") as out:
        out.write(template.read())
        out.write(data.read())
