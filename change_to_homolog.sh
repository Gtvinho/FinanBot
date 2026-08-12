#!/bin/bash

deactivate
echo "Antes: $(pwd)"

cd "$HOME/financeiro-bot-dev" || exit 1

echo "Depois: $(pwd)"

source .venv/bin/activate
python3 server_main.py