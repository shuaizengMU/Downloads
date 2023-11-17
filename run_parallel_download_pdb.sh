#!/bin/bash
#-------------------------------------------------------------------------------
#  SBATCH CONFIG
#-------------------------------------------------------------------------------
#SBATCH -p general
#SBATCH -t 0-21:00
#SBATCH -N 1  # number of nodes
#SBATCH -n 8  # number of cores (AKA tasks)
#SBATCH --mem=60G
#
## labels and outputs
#SBATCH -J MF  # give the job a custom name
#SBATCH -o ./parallel_download_pdb.out  # give the job output a custom name
#
#-------------------------------------------------------------------------------

source ~/data/anaconda3/bin/activate ~/data/anaconda3/envs/venv_pl
python parallel_download_pdb.py 