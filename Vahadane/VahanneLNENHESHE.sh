#!/bin/bash
#SBATCH --job-name=VAhanneHESHELNEN
#SBATCH --output=VahanneHESHELNEN.out
#SBATCH --partition=high_p
#SBATCH --account=gcs
##SBATCH --cpus-per-task=10
#SBATCH --mem-per-cpu=2GB
eval "$(conda shell.bash hook)"
conda activate ImgProcess
python HESHE_NormLNEN.py --inputdir ~/ln_LNEN_work_mathian/Tiles512_512/ --outputdir ~/ln_LNEN_work_mathian/Tiles_512_512_1stBasth_VahanneNorm_HESHE/
  
