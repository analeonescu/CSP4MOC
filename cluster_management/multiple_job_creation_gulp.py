"""
Create job.sh scripts for GULP .gin files.
"""

import os
import glob


sys_name = "xtal_OH_pf6"

for gin_path in sorted(glob.glob(f"{sys_name}_sg_*_*_rigid_uff.gin")):
    gin_file = os.path.basename(gin_path)
    idx = gin_file.split("_sg_")[1].replace("_rigid_uff.gin", "")
    job_sh = f"job_sg_{idx}.sh"
    
    if not os.path.exists(job_sh):
        print(f"Creating {job_sh}")
        os.system(f"cp job.sh {job_sh}")
