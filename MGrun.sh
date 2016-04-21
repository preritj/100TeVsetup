#!/bin/bash

# Request an hour of runtime:
#SBATCH --time=100:00:00

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
#../tt/MG/bin/madevent run.cmd
#../tt/MG/bin/generate_events -f
# ./data/pjaiswal/test/bin/generate_events << EOF
# 0
# 0
# EOF
