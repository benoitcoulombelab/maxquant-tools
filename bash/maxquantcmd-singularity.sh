#!/bin/bash
#SBATCH --account=def-coulomb
#SBATCH --time=5-00:00:00
#SBATCH --mail-type=NONE
#SBATCH --output=maxquant-%A.out
#SBATCH --error=maxquant-%A.out

bind_args=()
if [ -d conf ]
then
  for file in conf/*
  do
    filename=$(basename "$file")
    bind_args+=("-B" "$file:/opt/MaxQuant/bin/conf/$filename")
  done
  echo "Extra bind arguments for singularity are: " "${bind_args[@]}"
fi
args+=("$@")
if [ $# -eq 0 ]
then
  args+=("--help")
fi

singularity run \
  -B /scratch,/project,/home \
  "${bind_args[@]}" \
  "$MAXQUANT/maxquant-$MAXQUANT_VERSION.sif" \
  "${args[@]}"
