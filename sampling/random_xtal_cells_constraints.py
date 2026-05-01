"""
Create different cluter/ counterion unit cells with random coordinates 
with a predetermined cutoff distance bwteen different ionic components.
If the cutoff distance is too large, the structures will not geometry
optimise as there is essentially no interaction between the cluster and counterions.
If the cutoff distance is too small, the geometry otpimisation might fail 
due to unphysically close contacts.
"""

from pathlib import Path
from pyxtal import pyxtal
from pyxtal.molecule import pyxtal_molecule


def dist_counterions(atoms, counterion_centre = "S", cage_surface =["C", "H"]):
    """Return True if S-(C/H) distances are within the cutoff distance.
    Args:
        atoms (ase.Atoms): ASE Atoms object containing the structure.
        counterion_centre (str): Atom symbol representing the counterion centre (e.g.
        for sulfate that is "S").
        cage_surface (list): List representing atoms on the cage surface that can interact with 
        the counterions or other cages."""
        
    symbols = atoms.get_chemical_symbols()
    ci_indices = [i for i, s in enumerate(symbols) if s == counterion_centre]

    for idx in ci_indices:
        distances = atoms.get_distances(idx, range(len(atoms)))
        # Only consider distances to C/H atoms as a simplification
        relevant = [
            dist for dist, symbol in zip(distances, symbols)
            if symbol in ["C", "H"]
            ]
        if not relevant:
            return False

        min_dist = min(relevant)

        # Reject unphysical or extremely large distances
        if min_dist < 4 or min_dist > 12:
            return False

    return True


def file_writer(atoms, out_dir, idx, spg):
    '''Write the ASE Atoms object to a CIF file in the specified output directory.
    Args:
        atoms (ase.Atoms): ASE Atoms object containing the structure to be written.
        out_dir (str): Path to the output directory.
        idx (int): Index for the file name.
        spg (int): Space group number.'''
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"xtal_{spg}_{idx}"
    atoms.write(str(path) + ".cif")
    # for non-periodic systems, use:
    # atoms.write(str(path) + ".xyz")



def create_random_xtal_cell(
    path_cation = r"C:\Users\aleon\OneDrive\Desktop\gfn-ff-best-ranked.xyz",
    num_cations = 1,
    path_anion = r"C:\Users\aleon\OneDrive\Desktop\gfn-ff-best-ranked.xyz",
    num_anions = 4,
    out_dir = r"C:\Users\aleon\OneDrive\Desktop"
    ):
    """Generate random crystal structures with specified cation and anion molecules, 
    ensuring that the distance between counterions and cage surface atoms is 
    within a specified cutoff range.
    Args:
        path_cation (str): Path to the file containing the cation molecule.
        path_anion (str): Path to the file containing the anion molecule.
        out_dir (str): Path to the output directory where generated CIF files will be saved."""
    
    
    cation = pyxtal_molecule(path_cation)
    anion = pyxtal_molecule(path_anion)

    crystal = pyxtal(molecular = True)

    for idx in range(1, 11):
        for spg in range(1, 231): # Loop through space groups 1 to 230; not all spg's will give an output based on the point group of the cation and anion
            # for non-priodic systems, use spg = 1 for all
            # First attempt
            crystal.from_random(3, spg, [cation, anion], [num_cations, num_anions])  # by default generate 3D crystals, but 2D could be used
            ase_obj = crystal.to_ase()
            print(f"Generated trial for SPG {spg}")

            if dist_counterions(ase_obj):
                file_writer(ase_obj, out_dir, idx, spg)
                continue

            # Retry until cutoff is acceptable
            print("Retrying due to failed distance check")
            
            while True:
                crystal.from_random(3, spg, [cation, anion], [num_cations, num_anions])
                ase_obj = crystal.to_ase()

                if dist_counterions(ase_obj):
                    file_writer(ase_obj, out_dir, idx, spg)
                    break


if __name__ == "__main__":
    create_random_xtal_cell()
