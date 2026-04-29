"""
Create different crystals with random coordinates.
"""

from pathlib import Path
from pyxtal import pyxtal
from pyxtal.molecule import pyxtal_molecule



def dist_counterions(atoms):
    """Return True if S-(C/H) distances are acceptable."""
    symbols = atoms.get_chemical_symbols()
    sulfur_indices = [i for i, s in enumerate(symbols) if s == "S"]

    for idx in sulfur_indices:
        distances = atoms.get_distances(idx, range(len(atoms)))
        # Only consider distances to C/H atoms
        relevant = [
            dist for dist, sym in zip(distances, symbols)
            if sym in ["C", "H"]
        ]
        if not relevant:
            return False

        min_dist = min(relevant)

        # Reject unphysical or extremely large distances
        if min_dist < 0 or min_dist > 100:
            return False

    return True


def file_writer(atoms, out_dir, x, sg):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    base = out_dir / f"xtal_OH_{sg}_{x}"
    atoms.write(str(base) + ".cif")


def create_random_xtal_cell(
    path_cat=r"C:\Users\aleon\OneDrive\Desktop\gfn-ff-best-ranked.xyz",
    path_an=r"C:\Users\aleon\OneDrive\Desktop\gfn-ff-best-ranked.xyz",
    out_dir=r"C:\Users\aleon\OneDrive\Desktop"
):

    cat = pyxtal_molecule(path_cat)
    an  = pyxtal_molecule(path_an)

    crystal = pyxtal(molecular=True)

    for x in range(1, 11):
        for sg in range(1, 231):

            # First attempt
            crystal.from_random(2, sg, [cat, an], [1, 4])
            ase_obj = crystal.to_ase()
            print(f"Generated trial for SG {sg}")

            if dist_counterions(ase_obj):
                file_writer(ase_obj, out_dir, x, sg)
                continue

            # Retry until acceptable
            print("Retrying due to failed distance check")
            while True:
                crystal.from_random(2, sg, [cat, an], [1, 4])
                ase_obj = crystal.to_ase()

                if dist_counterions(ase_obj):
                    file_writer(ase_obj, out_dir, x, sg)
                    break


if __name__ == "__main__":
    create_random_xtal_cell()
