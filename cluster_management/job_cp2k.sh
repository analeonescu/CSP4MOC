#!/bin/bash -l
#$ -S /bin/bash
#$ -N final_janus
#$ -l h_rt=24:00:00
#$ -l mem=8G
#$ -pe mpi 16
#$ -cwd


# -----------------------------
# Environment setup
# -----------------------------

module unload compilers mpi gcc-libs

module load gcc-libs/10.2.0
module load compilers/gnu/10.2.0

# Required on Myriad
module load numactl/2.0.12
module load binutils/2.36.1/gnu-10.2.0
module load ucx/1.9.0/gnu-10.2.0

module load mpi/openmpi/4.0.5/gnu-10.2.0
module load openblas/0.3.13-openmp/gnu-10.2.0
module load cp2k/8.2/ompi/gnu-10.2.0

# Avoid stack overflow (important for CP2K)
ulimit -s unlimited

echo 'job is running'
gerun /shared/ucl/apps/cp2k/8.2/cp2k-8.2/bin/cp2k.popt < cp2k_input.inp > cp2k_output.out