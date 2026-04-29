"""
Automate xTB GFN-FF calculations for multiple structures.
Creates directories and runs xTB for each structure.
"""

import argparse
import os
import sys


def run_xtb(file_num, base_dir, input_pattern):
    """Run xTB calculation for a single structure."""
    dir_path = os.path.join(base_dir, str(file_num))
    
    # Create directory
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    # Move file to directory
    input_file = input_pattern.format(file_num)
    if os.path.exists(input_file):
        os.system(f'mv {input_file} {dir_path}/')
    else:
        print(f"Warning: {input_file} not found")
        return False
    
    # Change to directory and run xTB
    os.chdir(dir_path)
    os.system(f'xtb --gfnff --md {input_file} coord > xtb_{file_num}.log')
    
    print(f"Completed: {file_num}")
    return True


def main():
    parser = argparse.ArgumentParser(description='Automate xTB GFN-FF calculations')
    parser.add_argument('--start', '-s', type=int, default=1,
                        help='Starting file number (default: 1)')
    parser.add_argument('--end', '-e', type=int, default=100,
                        help='Ending file number (default: 100)')
    parser.add_argument('--dir', '-d', default='.',
                        help='Base directory (default: current)')
    parser.add_argument('--pattern', '-p', default='xtal_test_for_xtb_{}.xyz',
                        help='Input file pattern with {} for number (default: name_#.xyz)')
    
    args = parser.parse_args()
    
    # Change to base directory
    if args.dir != '.':
        os.chdir(args.dir)
    
    base_dir = os.getcwd()
    
    for file_num in range(args.start, args.end + 1):
        run_xtb(file_num, base_dir, args.pattern)
    
    print(f"Done: processed {args.end - args.start + 1} file(s)")


if __name__ == "__main__":
    main()