#!/bin/bash -l
#$ -l gpu=1
#$ -P Free
#$ -A UCL_chemM_Slater
#$ -l h_rt=24:00:0
#$ -l mem=15G
#$ -N two_molecule_job
#$ -cwd
# Your work should be done in $TMPDIR

source /shared/ucl/apps/bin/defmods
module load python/miniconda3/4.10.3
source $UCL_CONDA_PATH/etc/profile.d/conda.sh
cd /home/uccaleo/Scratch

ulimit -s unlimited
# janus geomopt --struct <insert your structure here> --arch mace --steps 2000 --fmax 0.005 --opt-cell-fully --model-path ./model/mofs_v2.model --device cuda --pressure 0.01
# this can be automated with e.g. jobs_janus.py, which will create a job script for each system and space group, and then you can submit them with qsub






