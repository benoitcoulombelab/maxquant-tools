#!/bin/bash

VENV="$HOME/maxquant-coulomb-venv"
BASH="$VENV"/bash
MAXQUANT="$VENV"/maxquant
SEQTOOLS_BASH="$MAXQUANT"/bash
EMAIL="$USER_EMAIL"

if [ "$1" == "clean" ]
then
    echo "Removing python virtual environment at $VENV"
    rm -R "$VENV"
    exit 0
fi
if [[ ! "$EMAIL" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$ ]]
then
    echo "Could not find your email address. Did you run configure.sh?"
    exit 1
fi
if [ ! -d "$VENV" ]
then
    echo "Creating python virtual environment at $VENV"
    python3 -m venv "$VENV"
fi
echo "Updating python libraries"
pip uninstall -y MaxquantParameters
pip install git+https://github.com/benoitcoulombelab/maxquant-parameters.git
echo "Updating bash scripts"
rm -R "$BASH"
mkdir "$BASH"
git clone --depth 1 https://github.com/benoitcoulombelab/maxquant-parameters.git "$MAXQUANT"
cp "$MAXQUANT_BASH"/*.sh "$BASH"
find "$BASH" -type f -name "*.sh" -exec sed -i "s/christian\.poitras@ircm\.qc\.ca/$EMAIL/g" {} \;
rm -Rf "$MAXQUANT"
