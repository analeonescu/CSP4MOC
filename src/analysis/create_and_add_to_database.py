"""Add CIF structures to an ASE database."""
from ase.io import read
from ase.db import connect
import os
from pathlib import Path

# Configuration
base_dir = Path('.')
database = 'my_database.db'

# File pattern: use {sg}, {i}, {j} as placeholders
file_pattern = 'xtal_OH_SO4_4_units_sg_{sg}_{i}_{j}.cif'

# Range settings
sg_start = 1
sg_end = 34
i_start = 1
i_end = 2001
j_start = 1
j_end = 6


def add_to_database():
    """Add CIF files to ASE database based on pattern."""
    count = 0
    
    for sg in range(sg_start, sg_end):
        for i in range(i_start, i_end):
            for j in range(j_start, j_end):
                filename = file_pattern.format(sg=sg, i=i, j=j)
                filepath = base_dir / filename
                
                if filepath.exists():
                    try:
                        structure = read(filepath)
                        db = connect(database)
                        db.write(structure, data={'sg': sg, 'xtb_str_idx': i, 'idx': j})
                        print(f'Added {filename} to database')
                        count += 1
                    except Exception as e:
                        print(f'Error reading {filename}: {e}')
    
    print(f'Done. Added {count} structures to {database}')


if __name__ == '__main__':
    add_to_database()
