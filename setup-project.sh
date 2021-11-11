#!/bin/bash

mkdir -p resources/git/hooks

git config core.hooksPath resources/git/hooks

PRE_COMMIT_HOOK=$'#!/bin/sh\n
MODIFIED_FILES=$(git diff --stat --cached --name-only -- `find . -name \'*.py\'` 2>&1)
if [ ! -z "$MODIFIED_FILES" ]
then
    black $MODIFIED_FILES
    flake8 $MODIFIED_FILES
    make unit-tests
fi'

echo "$PRE_COMMIT_HOOK" > resources/git/hooks/pre-commit

chmod a+x resources/git/hooks/pre-commit

# Install development requirements
pip install virtualenv
virtualenv -p python3 .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements-devel.txt
