#!/bin/bash
#
#SBATCH --job-name=llama
#SBATCH --comment=palace-text-gen
#SBATCH --chdir=/home/w/wrighta/code/ps/palace-diffusion/palace_diffusion
#SBATCH --output=/home/w/wrighta/code/ps/palace-diffusion/slurm.out
#SBATCH --ntasks=1

python main.py