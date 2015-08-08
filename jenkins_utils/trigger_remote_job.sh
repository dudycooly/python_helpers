#!/bin/bash -ex

# Install dependencies to virtual env
echo "Installing dependencies...."
pip install -r requirements.txt

# Execute python script
python remote_trigger.py