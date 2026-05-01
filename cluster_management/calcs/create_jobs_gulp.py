"""
Create multiple job.sh copies for GULP gin files.
It is more time efficient to queue multiple quick jobs (~ 3 min)
than one longer one (~48 h)."""

import argparse
import os


def main():
    parser = argparse.ArgumentParser(description='Create GULP job files')
    parser.add_argument('--name', '-n', default='xtal_OH_pf6',
                        help='System name prefix')
    parser.add_argument('--start', type=int, default=1,
                        help='Starting file number')
    parser.add_argument('--end', type=int, default=1000,
                        help='Ending file number')
    parser.add_argument('--gulp-path', default='/home/uccaleo/gulp-6.1.2/Src/gulp',
                        help='Path to GULP executable')
    
    args = parser.parse_args()
    
    for spg in [1, 2, 3, 9, 14, 19, 33]:
        for num in range(args.start, args.end + 1):
            gin_file = f'{args.name}_sg_{spg}_{num}_rigid_uff.gin'
            
            if os.path.exists(gin_file):
                print(f'Creating job for: {gin_file}')
                os.system(f'echo "{args.gulp_path} < {gin_file} > {gin_file[:-4]}.gout" > tmp')
                os.system(f'cp job.sh job_sg_{spg}_{num}.sh')
                os.system(f'cat tmp >> job_sg_{spg}_{num}.sh')

    print(f'Done for {spg} {num}')


if __name__ == "__main__":
    main()
