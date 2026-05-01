"""
Create different cluster/counterion unit cells with specified 
initial unit cell parameters; this adds some bia to the unit cell dimensions,
but significantly speeds up the file generation.
"""

from pathlib import Path
from pyxtal import pyxtal
from pyxtal.molecule import pyxtal_molecule


def file_writer(atoms, out_dir, idx, spg):
    '''Write the ASE Atoms object to a CIF file in the specified output directory.'''
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"xtal_{spg}_{idx}"
    atoms.write(str(path) + ".cif")


def create_random_xtal_cell(
    path_cation=r"\path\to\cation.xyz",
    num_cations=4,
    path_anion=r"\path\to\anion.xyz",
    num_anions=16,
    out_dir=r"\path\to\output",
):
    """Generate random crystal structures with specified cation and anion molecules
    and fixed initial unit cell parameters.

    Args:
        path_cation (str): Path to the file containing the cation molecule.
        path_anion (str): Path to the file containing the anion molecule.
        out_dir (str): Output directory for generated CIF files.
    """

    cation = pyxtal_molecule(path_cation)
    anion = pyxtal_molecule(path_anion)

    crystal = pyxtal(molecular=True)

    # Pack cell params into the format pyxtal expects: [a, b, c, alpha, beta, gamma]
    cell_params = [50, 50, 50, 90, 90, 90]

    for idx in range(1, 11):
        for spg in range(1, 231):
            try:
                crystal.from_random(3, spg, [cation, anion], 
                                    [num_cations, num_anions],
                                    lattice=cell_params,
                                    )
                ase_obj = crystal.to_ase()
                file_writer(ase_obj, out_dir, idx, spg)
                print(f"Written: SPG {spg}, idx {idx}")

            except Exception as e:
                # Many space groups are incompatible with the given molecules/cell;
                # silently skip rather than crashing the whole run.
                print(f"Skipped SPG {spg}: {e}")


if __name__ == "__main__":
    create_random_xtal_cell()