#!/bin/bash
#SBATCH --account=def-coulomb
#SBATCH --time=5-00:00:00
#SBATCH --mail-type=NONE
#SBATCH --output=maxquant-%A.out
#SBATCH --error=maxquant-%A.out

dotnet "$MAXQUANT"/bin/MaxQuantCmd.exe "$@"
