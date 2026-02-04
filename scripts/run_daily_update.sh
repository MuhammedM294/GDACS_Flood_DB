#!/usr/bin/env bash

# Fail fast
set -euo pipefail

# ------- ENVIRONMENT SETUP -------

PROJECT_DIR="/eodc/private/tuwgeo/users/mabdelaa/repos/GDACS_Flood_DB"
VENV_DIR="$PROJECT_DIR/.venv"
PYTHON="$VENV_DIR/bin/python"

#-----ACTIVATE PROJECT-------
cd "$PROJECT_DIR"
source "$VENV_DIR/bin/activate"


# ------- RUN DAILY UPDATE SCRIPT -------

$PYTHON -m scripts.update_flood_db