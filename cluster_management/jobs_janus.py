from pathlib import Path
import subprocess

sys_name_list = ['SO3_NMe4', 'Me_SO4']
space_groups = [1, 2, 3, 9, 14, 19, 33]

for name in sys_name_list:
    for spg in space_groups:

        # Prepare job script path
        job_script = Path(f"job_{name}_{spg}.sh")

        # Start fresh from template
        subprocess.run(["cp", "job.sh", job_script])

        # Collect lines to append
        lines_to_add = []

        for num in range(1, 2001):
            for idx in range(1, 4):

                cif = Path(f"xtal_{name}_sg_{spg}_{num}_{idx}_rigid_uff.cif")
                extxyz = Path(f"xtal_Me_SO4_sg_1_1_3_rigid_uff-opt.extxyz")

                if cif.exists() and not extxyz.exists():
                    output_prefix = cif.stem.replace("_rigid_uff", "")
                    cmd = (
                        f"\n\njanus geomopt "
                        f"--struct {cif} "
                        f"--arch mace "
                        f"--steps 2000 "
                        f"--fmax 0.005 "
                        f"--opt-cell-fully "
                        f"--model-path ../mace_mof/mofs_v2.model "
                        f"--device cuda "
                        f"--pressure 0.01 "
                        f"> {output_prefix}"
                    )
                    lines_to_add.append(cmd)

        # Append all commands at once
        if lines_to_add:
            job_script.write_text(job_script.read_text() + "".join(lines_to_add))

        # Submit job
        subprocess.run(["qsub", "-N", f"{name}_{spg}", str(job_script)])
