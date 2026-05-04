"""Add CIF structures to an ASE database."""
from ase.io import read
from ase.db import connect
from pathlib import Path

# Configuration
base_dir = Path('.')
database = 'my_database.db'
sys_name = 'xtal_OH_SO4_4_units'  # Example system name, adjust as needed

i_start = 1
i_end = 2001
j_start = 1
j_end = 6


def add_to_database():
    """Add CIF files to ASE database based on pattern."""
    count = 0
    
    for spg in [1, 2, 3, 9, 14, 19, 33]:  # space groups allowed by the cage symmetries
        for i in range(i_start, i_end):
            for j in range(j_start, j_end):
                filename = f'{sys_name}_spg_{spg}_{i}_{j}.cif'
                filepath = base_dir / filename
                
                if filepath.exists():
                    try:
                        structure = read(filepath)
                        db = connect(database)
                        db.write(structure, data={'spg': spg, 'xtb_str_idx': i, 'idx_2': j})
                        print(f'Added {filename} to database')
                        count += 1
                    except Exception as e:
                        print(f'Error reading {filename}: {e}')
    
    print(f'Done. Added {count} structures to {database}')


if __name__ == '__main__':
    add_to_database()
