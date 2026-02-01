#!/bin/bash
set -euo pipefail

python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r dependencies.txt

python -m db

touch .env
echo "✅ Init complete"
