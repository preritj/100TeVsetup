#!/bin/bash

# Request an hour of runtime:
#SBATCH --time=40:00:00

# Default resources are 1 core with 2.8GB of memory per core.

# Use more cores:
#SBATCH -c 16
#SBATCH --mem-per-cpu=16G

# Specify a job name:
#SBATCH -J MGrun

# Specify an output file
#SBATCH -o MGrun.out
#SBATCH -e MGrun.out

# Run a command

module load root/5.34

python MGrun.py
