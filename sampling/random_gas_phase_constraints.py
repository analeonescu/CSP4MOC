"""
Creates different cluster/counterion .xyz files (non-periodic, gasphase)
with random coordinates, with a predetermined cutoff distance between 
different ionic components.
"""

from pathlib import Path
from pyxtal import pyxtal
from pyxtal.molecule import pyxtal_molecule


def dist_counterions(atoms, counterion_centre="S", cage_surface=["C", "H"]):
    """Return True if S-(C/H) distances are within the cutoff distance.
    Args:
        atoms (ase.Atoms): ASE Atoms object containing the structure.
        counterion_centre (str): Atom symbol representing the counterion centre.
        cage_surface (list): Atoms on the cage surface that interact with counterions."""

    symbols = atoms.get_chemical_symbols()
    ci_indices = [i for i, s in enumerate(symbols) if s == counterion_centre]

    for idx in ci_indices:
        distances = atoms.get_distances(idx, range(len(atoms)))
        relevant = [
            dist for dist, symbol in zip(distances, symbols)
            if symbol in cage_surface
        ]
        if not relevant:
            return False
        min_dist = min(relevant)
        if min_dist < 4 or min_dist > 12:
            return False

    return True


def file_writer(atoms, out_dir, idx):
    """Write the ASE Atoms object to an XYZ file in the specified output directory.
    Args:
        atoms (ase.Atoms): ASE Atoms object containing the structure to be written.
        out_dir (str): Path to the output directory.
        idx (int): Index for the file name."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"xtal_{idx}"
    atoms.write(str(path) + ".xyz")


def create_random_xtal_cell(
    path_cation=r"C:\Users\aleon\OneDrive\Desktop\gfn-ff-best-ranked.xyz",
    num_cations=1,
    path_anion=r"C:\Users\aleon\OneDrive\Desktop\gfn-ff-best-ranked.xyz",
    num_anions=4,
    out_dir=r"C:\Users\aleon\OneDrive\Desktop",
):
    """Generate random non-periodic structures with specified cation and anion molecules,
    ensuring that the distance between counterions and cage surface atoms is
    within a specified cutoff range.
    Args:
        path_cation (str): Path to the file containing the cation molecule.
        path_anion (str): Path to the file containing the anion molecule.
        out_dir (str): Path to the output directory where generated XYZ files will be saved.
    """

    cation = pyxtal_molecule(path_cation)
    anion = pyxtal_molecule(path_anion)
    crystal = pyxtal(molecular=True)

    for idx in range(1, 11):
        try:
            crystal.from_random(3, 1, [cation, anion], [num_cations, num_anions])
            ase_obj = crystal.to_ase()
            print(f"Generated trial {idx}")

            if dist_counterions(ase_obj):
                file_writer(ase_obj, out_dir, idx)
                continue

            print("Retrying due to failed distance check...")
            while True:
                crystal.from_random(3, 1, [cation, anion], [num_cations, num_anions])
                ase_obj = crystal.to_ase()
                if dist_counterions(ase_obj):
                    file_writer(ase_obj, out_dir, idx)
                    break

        except Exception as e:
            print(f"Skipped idx {idx}: {e}")


if __name__ == "__main__":
    create_random_xtal_cell()