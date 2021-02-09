#!/bin/bash

VENV="$MAXQUANT_TOOLS"/venv

if [ "$1" == "clean" ]
then
    echo "Removing python virtual environment at $VENV"
    rm -R "$VENV"
    exit 0
fi
if [ ! -d "$VENV" ]
then
    echo "Creating python virtual environment at $VENV"
    python3 -m venv "$VENV"
fi
VERSION=$(git --git-dir="$MAXQUANT_TOOLS"/.git rev-parse --abbrev-ref HEAD)
echo "Updating python libraries using $VERSION"
"$VENV"/bin/pip uninstall -y MaxquantTools
"$VENV"/bin/pip install git+file://"$MAXQUANT_TOOLS"@"$VERSION"
