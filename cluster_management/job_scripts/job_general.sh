#!/bin/bash -l
#$ -l gpu=1
#$ -l h_rt=18:00:00
#$ -l mem=15G
#$ -N comp_2_sys1_1to100

#$ -wd /home/uccaleo/Scratch/SO3_NMe4_2_cages

module unload compilers mpi
module unload cuda/7.5.18/gnu-4.9.2
module load cuda/11.3.1/gnu-10.2.0

cd /home/uccaleo/Scratch/SO3_NMe4_2_cages

ulimit -s unlimited

