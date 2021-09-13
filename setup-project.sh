#!/bin/bash

mkdir -p resources/git/hooks

git config core.hooksPath resources/git/hooks

echo $'#/bin/sh\n\nblack ./\n\npython lint.py --path ./src ./tests ./bin\n\nmake test' > resources/git/hooks/pre-commit

chmod a+x resources/git/hooks/pre-commit

# Install development requirements
pip install virtualenv
virtualenv -p python3 .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements-devel.txt
