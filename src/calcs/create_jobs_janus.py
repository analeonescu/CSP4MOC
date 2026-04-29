"""
Create and submit Janus jobs for multiple structures.
"""

import argparse
import os
import sys


def create_job_file(name, spg, template_file='job.sh'):
    """Create a job file by copying from template."""
    job_file = f'job_{name}_{spg}.sh'
    
    if os.path.exists(template_file):
        os.system(f'cp {template_file} {job_file}')
    else:
        raise FileNotFoundError(f"Template file not found: {template_file}")
    
    return job_file


def main():
    parser = argparse.ArgumentParser(description='Create and submit Janus jobs')
    parser.add_argument('--names', '-n', nargs='+', default=['SO3_NMe4', 'Me_SO4'],
                        help='System names (default: SO3_NMe4 Me_SO4)')
    parser.add_argument('--spg', '-s', nargs='+', type=int, 
                        default=[1, 2, 3, 9, 14, 19, 33],
                        help='Space groups (default: 1 2 3 9 14 19 33)')
    parser.add_argument('--start', type=int, default=1,
                        help='Starting file number (default: 1)')
    parser.add_argument('--end', type=int, default=2000,
                        help='Ending file number (default: 2000)')
    parser.add_argument('--idx-range', type=int, nargs=2, default=[1, 4],
                        help='Index range (default: 1 4)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be created without submitting')
    
    args = parser.parse_args()
    
    for name in args.names:
        for spg in args.spg:
            job_file = create_job_file(name, spg)
            
            # Find matching files and add to job
            count = 0
            for num in range(args.start, args.end + 1):
                for idx in range(args.idx_range[0], args.idx_range[1]):
                    path = f'xtal_{name}_sg_{spg}_{num}_{idx}_rigid_uff.cif'
                    
                    if os.path.exists(path):
                        with open(job_file, 'a') as f:
                            f.write(f'\njanus geomopt --struct {path} --arch mace --steps 2000 --fmax 0.005 --opt-cell-fully --model-path ../mace_mof/mofs_v2.model --device cuda --pressure 0.01 > {path[:-13]}\n')
                        count += 1
            
            print(f"Job {name}_{spg}: {count} structures")
            
            if not args.dry_run:
                os.system(f'qsub -N {name}_{spg} {job_file}')
    
    print("Done")


if __name__ == "__main__":
    main()
