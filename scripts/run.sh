#!/bin/bash
#
#SBATCH --job-name=palace-diffusion-bot
#SBATCH --comment="diffusion model text generation bot"
#SBATCH --mail-type=ALL
#SBATCH --mail-user=a.wright@campus.lmu.de
#SBATCH --chdir=/home/w/wrighta/code/ps/palace-diffusion/palace_diffusion
#SBATCH --output=/home/w/wrighta/code/ps/palace-diffusion/slurm.out
#SBATCH --ntasks=1

export 'PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512'
python main.py