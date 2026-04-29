#!/bin/bash -l
#$ -S /bin/bash


# 2. Request one hour of wallclock time (format hours:minutes:seconds).
#$ -l h_rt=00:20:00


# 3. Request 1 gigabyte of RAM per core
#$ -l mem=1G


# 4. Set the name of the job.
#$ -N test_run_simulation


# 6. Select the MPI parallel environment and 80 processor 
# you need at least 80 for kathleen given larger core space
#$ -pe mpi 80


#$ -wd /home/uccaleo/Scratch/SO3_NMe4_uff_rigid
# note that your wd needs to be in Scratch!


# Your work should be done in $TMPDIR


# Run the application and put the output into a file called date.txt#
export GULP_LIB='/home/uccaleo/ACFS/gulp-6.1.2/Libraries/'
