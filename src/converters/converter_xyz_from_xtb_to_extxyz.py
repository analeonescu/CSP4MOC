"""
XYZ to EXTXYZ Converter

Convert XYZ files from xTB optimizations to extended XYZ format.
Can process multiple directories and combine into one file.

Usage:
    python converter_xyz_from_xtb_to_extxyz.py --input "*/xtbopt.xyz" --output combined.extxyz

Examples:
    # Convert all xtbopt.xyz files in numbered directories
    python converter_xyz_from_xtb_to_extxyz.py -i "*/xtbopt.xyz" -o all_so3_nme4.extxyz

    # For directory structure like 1/xtal_SO3_NMe4_1.xyz, 2/xtal_SO3_NMe4_2.xyz
    python converter_xyz_from_xtb_to_extxyz.py -i "*/xtal_SO3_NMe4_*.xyz" -o so3_nme4.extxyz
"""

import argparse
import glob
import os
import sys

import ase.io


def convert_xyz_to_extxyz(xyz_file, output_file, append=False):
    """
    Convert a single XYZ file to EXTXYZ format.
    
    Parameters
    ----------
    xyz_file : str
        Path to input XYZ file.
    output_file : str
        Path for output EXTXYZ file.
    append : bool
        If True, append to output file instead of overwriting.
    
    Returns
    -------
    bool
        True if conversion successful, False otherwise.
    """
    if not os.path.exists(xyz_file):
        print(f"Warning: File not found: {xyz_file}")
        return False
    
    try:
        # Read XYZ file
        atoms = ase.io.read(xyz_file, format='xyz')
        
        # Write EXTXYZ file
        ase.io.write(output_file, images=atoms, format='extxyz', append=append)
        
        print(f"Converted: {xyz_file} -> {output_file}")
        return True
        
    except Exception as e:
        print(f"Error converting {xyz_file}: {e}")
        return False


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description='Convert XYZ files from xTB to EXTXYZ format'
    )
    parser.add_argument('--input', '-i', 
                        default='*/xtbopt.xyz',
                        help='Input XYZ file pattern (default: */xtbopt.xyz)')
    parser.add_argument('--output', '-o', default='combined.extxyz',
                        help='Output EXTXYZ file (default: combined.extxyz)')
    parser.add_argument('--no-append', action='store_true',
                        help='Overwrite output file instead of appending')
    
    args = parser.parse_args()
    
    # Find all XYZ files matching pattern
    xyz_files = sorted(glob.glob(args.input))
    
    if not xyz_files:
        print(f"No files found matching: {args.input}")
        return 1
    
    print(f"Found {len(xyz_files)} file(s) to convert")
    
    append = not args.no_append
    success_count = 0
    
    for xyz_file in xyz_files:
        if convert_xyz_to_extxyz(xyz_file, args.output, append=append):
            success_count += 1
            append = True  # Append after first file
    
    print(f"Successfully converted {success_count}/{len(xyz_files)} files")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

