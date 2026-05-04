"""
Submit GULP jobs to the cluster for incomplete optimizations.
Stops at 1000 submissions (cluster limit on Kathleen/Myriad).
"""

import os
import glob
import subprocess


MAX_JOBS = 1000
sys_name = "xtal_OH_pf6"


def submit_missing_jobs(system: str, max_jobs: int = MAX_JOBS) -> int:
    """Submit jobs for .gin files without corresponding .gout files."""
    pattern = f"{system}_sg_*_*_rigid_uff.gin"
    gin_files = sorted(glob.glob(pattern))
    
    submitted = 0
    for gin_path in gin_files:
        if submitted >= max_jobs:
            break
        
        gin_file = os.path.basename(gin_path)
        gout_file = gin_file.replace(".gin", ".gout")
        
        if not os.path.exists(gout_file):
            job_sh = gin_file.replace(".gin", ".sh")
            if os.path.exists(job_sh):
                idx = gin_file.split("_sg_")[1].replace("_rigid_uff.gin", "")
                job_name = f"{system.replace('xtal_', '')}_{idx}"
                subprocess.run(["qsub", "-N", job_name, job_sh], check=True)
                submitted += 1
    
    return submitted


if __name__ == "__main__":
    n = submit_missing_jobs(sys_name)
    print(f"Submitted {n} jobs (max: {MAX_JOBS})")
        