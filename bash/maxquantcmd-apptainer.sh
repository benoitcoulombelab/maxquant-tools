#!/bin/bash
#SBATCH --account=def-coulomb
#SBATCH --time=5-00:00:00
#SBATCH --mail-type=NONE
#SBATCH --output=maxquant-%A.out
#SBATCH --error=maxquant-%A.out

set -e

home=$(readlink -f ~)
scratch=$(readlink -f ~/scratch)
project=(~/projects/*)
project=${project[0]}
project=$(readlink -f "$project/..")
workdir="${SLURM_TMPDIR:-$PWD}"

bind_args=()
if [ -d conf ]
then
  for file in conf/*
  do
    filename=$(basename "$file")
    bind_args+=("-B" "$file:/opt/MaxQuant/bin/conf/$filename")
  done
  echo "Extra bind arguments for apptainer are: " "${bind_args[@]}"
fi
args+=("$@")
if [ $# -eq 0 ]
then
  args+=("--help")
fi

apptainer run \
  -C -W "$workdir" --pwd "$PWD" \
  -B "$home","$scratch","$project" \
  "${bind_args[@]}" \
  "$MAXQUANT/maxquant-$MAXQUANT_VERSION.sif" \
  "${args[@]}"
