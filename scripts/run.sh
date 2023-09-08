#!/bin/bash
#
#SBATCH --job-name=llama
#SBATCH --comment=palace-text-gen
#SBATCH --chdir=/home/w/wrighta/code/ps/palace-diffusion/palace_diffusion
#SBATCH --output=/home/w/wrighta/code/ps/palace-diffusion/slurm.out
#SBATCH --ntasks=1

export 'PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512'
python main.py