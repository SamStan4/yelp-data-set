#!/usr/bin/env bash

RED='\033[31m'
BLUE='\033[34m'

if ! nslookup google.com > /dev/null 2>&1; then
    echo -e "${RED}ERROR: internet connection is unstable${RESET}"
    exit 1
fi

VENV_DIR="virtual_environment"
if [ -d "$VENV_DIR" ]; then
    rm -rf "$VENV_DIR"
fi

echo -e "${BLUE}creating virtual environment in current directory...${RESET}"

python3 -m venv virtual_environment > /dev/null

source virtual_environment/bin/activate

pip install pyqt5 > /dev/null

pip install psycopg2-binary > /dev/null

deactivate

echo -e "${BLUE}...done -- virtual environment created in current directory${RESET}"