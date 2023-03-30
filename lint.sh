#!/bin/bash

source .venv/bin/activate

black --version
isort --version
flake8 --version


echo "===== BLACK ====="
black .

echo "===== ISORT ====="
isort .

echo "===== FLAKE_8 ====="
flake8 .

deactivate
