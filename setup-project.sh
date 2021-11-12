#!/bin/bash

mkdir -p resources/git/hooks

git config core.hooksPath resources/git/hooks

PRE_COMMIT_HOOK=$'#!/bin/sh\n
MODIFIED_FILES=$(git diff --stat --cached --name-only -- `find . -name \'*.py\'` 2>&1)
if [ ! -z "$MODIFIED_FILES" ]
then
    black --line-length 79 $MODIFIED_FILES
    flake8 --ignore=E203,W503 $MODIFIED_FILES
    if [ $? -eq 0 ]
    then
        make unit-tests
    else
        exit 1
    fi
fi'

echo "$PRE_COMMIT_HOOK" > resources/git/hooks/pre-commit

chmod a+x resources/git/hooks/pre-commit

