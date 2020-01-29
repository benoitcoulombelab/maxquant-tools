#!/bin/bash

VENV="$HOME/maxquant-coulombe-venv"

if [ "$1" == "clean" ]
then
    echo "Removing python virtual environment at $VENV"
    rm -R "$VENV"
fi
if [ ! -d "$VENV" ]
then
    echo "Creating python virtual environment at $VENV"
    python3 -m venv "$VENV"
fi
echo "Updating python libraries"
pip uninstall -y MaxquantParameters
pip install git+https://github.com/benoitcoulombelab/maxquant-parameters.git
