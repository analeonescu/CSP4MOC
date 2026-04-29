"""
CIF to EXTXYZ Converter

Convert CIF crystal structure files to extended XYZ format.
Can process multiple files and combine them into one.

Usage:
    python converter_cif_to_extxyz.py --input "*.cif" --output combined.extxyz
"""

import argparse
import glob
import os
import sys
import ase.io


def convert_cif_to_extxyz(cif_file, output_file, append=False):
    """
    Convert a single CIF file to EXTXYZ format.
    
    Parameters
    ----------
    cif_file : str
        Path to input CIF file.
    output_file : str
        Path for output EXTXYZ file.
    append : bool
        If True, append to output file instead of overwriting.
    """
    if not os.path.exists(cif_file):
        print(f"Warning: File not found: {cif_file}")
        return False
    
    try:
        # Read CIF file
        atoms = ase.io.read(cif_file, format='cif')
        
        # Write EXTXYZ file
        write_mode = 'a' if append else 'w'
        ase.io.write(output_file, images=atoms, format='extxyz', append=append)
        
        print(f"Converted: {cif_file} -> {output_file}")
        return True
        
    except Exception as e:
        print(f"Error converting {cif_file}: {e}")
        return False


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description='Convert CIF files to EXTXYZ format')
    parser.add_argument('--input', '-i', required=True, 
                        help='Input CIF file or pattern (e.g., "*.cif")')
    parser.add_argument('--output', '-o', default='combined.extxyz',
                        help='Output EXTXYZ file (default: combined.extxyz)')
    parser.add_argument('--no-append', action='store_true',
                        help='Overwrite output file instead of appending')
    
    args = parser.parse_args()
    
    # Check if input is a glob pattern or single file
    if '*' in args.input or '?' in args.input:
        # Multiple files - use glob
        cif_files = sorted(glob.glob(args.input))
        
        if not cif_files:
            print(f"No files found matching: {args.input}")
            return 1
            
        print(f"Found {len(cif_files)} file(s) to convert")
        
        append = not args.no_append
        success_count = 0
        
        for cif_file in cif_files:
            if convert_cif_to_extxyz(cif_file, args.output, append=append):
                success_count += 1
                append = True  # Append after first file
        
        print(f"Successfully converted {success_count}/{len(cif_files)} files")
        
    else:
        # Single file
        convert_cif_to_extxyz(args.input, args.output, append=False)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

