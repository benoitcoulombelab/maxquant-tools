#!/bin/bash
#SBATCH --account=def-coulomb
#SBATCH --time=5-00:00:00
#SBATCH --mail-type=NONE
#SBATCH --output=maxquant-%A.out
#SBATCH --error=maxquant-%A.out

# Start this script with this command and change parameters to proper values:
# sbatch --cpus-per-task=8 --mem=40G maxquant.sh

fixargs=("-p" "mqpar.xml" "-d" "$PWD" "-o" "mqpar-run.xml")
if [ -n "$SLURM_CPUS_PER_TASK" ]
then
  fixargs+=("-t" "$SLURM_CPUS_PER_TASK")
fi

fixparameters "${fixargs[@]}"
mono "$MAXQUANT"/bin/MaxQuantCmd.exe ./mqpar-run.xml
