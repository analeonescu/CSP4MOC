#!/bin/bash -l
#$ -S /bin/bash
#$ -l h_rt=00:20:00
#$ -l mem=1G
#$ -N test_run_simulation
#$ -pe mpi 80
#$ -wd /home/uccaleo/Scratch/SO3_NMe4_uff_rigid

# note that your wd needs to be in Scratch!
# Your work should be done in $TMPDIR

export GULP_LIB='/home/uccaleo/ACFS/gulp-6.1.2/Libraries/'
