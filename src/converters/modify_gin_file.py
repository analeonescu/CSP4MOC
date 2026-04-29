"""
Modify GULP input files (.gin) for different theory levels.

Usage:
    python modify_uff_rigid.py --theory uff --dir . --pattern "xtal_*.gin"
    python modify_uff_rigid.py --theory gfnff --dir . --pattern "xtal_*.gin"
"""

import argparse
import glob
import os
import sys


def modify_gulp_input(file_path, theory):
    """
    Modify a GULP input file for the specified theory level.
    
    Parameters
    ----------
    file_path : str
        Path to the .gin input file.
    theory : str
        Theory level: 'uff' or 'gfnff'
    """
    if theory == 'uff':
        target_word = 'opti'
        replacement_word = 'opti conp rigid'
        new_lines = [
            '\nlibrary uff.lib',
            '\nmaxcyc 100',
            '\n',
            f'output xyz {os.path.basename(file_path).strip(".gin")}_uff.cif'
        ]
    elif theory == 'gfnff':
        target_word = 'opti'
        replacement_word = 'gfnff opti conp'
        new_lines = [
            '\nmaxcyc 100',
            '\n',
            f'output xyz {os.path.basename(file_path).strip(".gin")}_gfnff.cif'
        ]
    else:
        raise ValueError(f"Unknown theory: {theory}. Use 'uff' or 'gfnff'")
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Replace target word
    for i, line in enumerate(lines):
        lines[i] = line.replace(target_word, replacement_word)
    
    # Add new lines at the end
    lines.extend(new_lines)
    
    with open(file_path, 'w') as file:
        file.writelines(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Modify GULP input files for different theory levels'
    )
    parser.add_argument('--theory', '-t', required=True, choices=['uff', 'gfnff'],
                        help='Theory level: uff (Universal Force Field) or gfnff (GFN-FF)')
    parser.add_argument('--dir', '-d', default='.',
                        help='Directory containing .gin files (default: current directory)')
    parser.add_argument('--pattern', '-p', default='*.gin',
                        help='File pattern to match (default: *.gin)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be modified without changing files')
    
    args = parser.parse_args()
    
    # Change to target directory
    if args.dir != '.':
        os.chdir(args.dir)
    
    # Find matching files
    files = sorted(glob.glob(args.pattern))
    
    if not files:
        print(f"No files found matching: {args.pattern}")
        return 1
    
    print(f"Found {len(files)} file(s) to modify")
    print(f"Theory level: {args.theory}")
    
    if args.dry_run:
        print("\nDry run - files that would be modified:")
        for f in files:
            print(f"  {f}")
        return 0
    
    # Process each file
    for i, file_path in enumerate(files, 1):
        try:
            modify_gulp_input(file_path, args.theory)
            print(f"Modified: {file_path}")
        except Exception as e:
            print(f"Error modifying {file_path}: {e}")
    
    print(f"\nDone: {len(files)} file(s) processed")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())