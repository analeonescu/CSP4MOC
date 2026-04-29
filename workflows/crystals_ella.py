from pyxtal import pyxtal
from pyxtal.molecule import pyxtal_molecule
from pyxtal.interface import gulp
from pyxtal.lattice import Lattice
# In[5]:
#path = input('Insert your path here: ')
my_crystal_1 = pyxtal_molecule('unit.xyz') # either me cage or so3/ so3-so3 cage 
my_crystal_2 = ... # the other one
c1 = pyxtal(molecular=True) #indicates we are looking at a molecular crystal
l2 = Lattice.from_para(16.5, 16.5, 16.5, 90, 90, 90) # 50 50 50
x=1
while x<=10:
    c1.from_random(3, 1, [my_crystal1, my_crysatl2], [1,2], lattice=l2) # 3 = 3d, 1 = space group

    ase_c1 = c1.to_ase()
    filename = 'cage_crystal_2_units_' + str(x) + '.xyz'
    ase_c1.write(filename, format ='extxyz')
    filename = 'cage_crystal_2_units_' + str(x) + '.cif'
    ase_c1.write(filename, format ='cif')
    x=x+1
    print(x)
    
    






from pathlib import Path
from pyxtal import pyxtal
from pyxtal.molecule import pyxtal_molecule
from pyxtal.lattice import Lattice

# Load molecules
mol1 = pyxtal_molecule("unit.xyz")      # e.g. Me cage or SO3 cage
mol2 = ...                              # the other molecule

# Prepare crystal generator
crystal = pyxtal(molecular=True)
lattice = Lattice.from_para(16.5, 16.5, 16.5, 90, 90, 90)

# Output prefix
prefix = "cage_crystal_2_units"

for i in range(1, 11):

    # Generate random structure: 3D, SG=1
    crystal.from_random(
        3, 1,
        [mol1, mol2],   # molecules
        [1, 2],         # stoichiometry
        lattice=lattice
    )

    ase_obj = crystal.to_ase()

    # Write files
    xyz_file = Path(f"{prefix}_{i}.xyz")
    cif_file = Path(f"{prefix}_{i}.cif")

    ase_obj.write(xyz_file, format="extxyz")
    ase_obj.write(cif_file, format="cif")

    print(f"Generated structure {i}")
