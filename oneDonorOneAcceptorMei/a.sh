#!/bin/sh
#SBATCH --partition=et1_new,et1_old,et2,et2_medmem,et3,et4_medmem,et4_bigmem
#SBATCH --mem=8G
#SBATCH --job-name={g}_{T}_{ene}
#SBATCH --output=./output/sl_{g}_{T}_{ene}.out
#SBATCH --error=./output/sl_{g}_{T}_{ene}.err
#SBATCH -n 4
#SBATCH -c 1
#SBATCH -t 7000

python -u  star_DA1_MultiChannel.py 300 0 | gzip > out_{g}_{T}_{ene}.gz
