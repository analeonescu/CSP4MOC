"""
Submit GULP jobs to cluster if gin exists and gout doesn't.
Limits submissions to avoid hitting cluster limits.
"""

import argparse
import os


def main():
    parser = argparse.ArgumentParser(description='Submit GULP jobs to cluster')
    parser.add_argument('--name', '-n', default='xtal_OH_pf6',
                        help='System name prefix')
    parser.add_argument('--spg-start', type=int, default=1,
                        help='Starting space group')
    parser.add_argument('--spg-end', type=int, default=33,
                        help='Ending space group')
    parser.add_argument('--start', type=int, default=1,
                        help='Starting file number')
    parser.add_argument('--end', type=int, default=1000,
                        help='Ending file number')
    parser.add_argument('--max-jobs', type=int, default=1000,
                        help='Maximum jobs to submit')
    
    args = parser.parse_args()
    
    job_count = 0
    
    for spg in range(args.spg_start, args.spg_end + 1):
        for num in range(args.start, args.end + 1):
            gin_file = f'{args.name}_sg_{spg}_{num}_rigid_uff.gin'
            gout_file = f'{args.name}_sg_{spg}_{num}_rigid_uff.gout'
            job_file = f'job_sg_{spg}_{num}.sh'
            
            if os.path.exists(gin_file) and not os.path.exists(gout_file):
                if os.path.exists(job_file):
                    os.system(f'qsub -N {args.name.strip("xtal_")}_{spg}_{num} {job_file}')
                    job_count += 1
                    print(f'Submitted: {job_file}')
            
            if job_count >= args.max_jobs:
                print(f'Reached max jobs limit: {args.max_jobs}')
                break
        
        if job_count >= args.max_jobs:
            break
    
    print(f'Total jobs submitted: {job_count}')


if __name__ == "__main__":
    main()
        