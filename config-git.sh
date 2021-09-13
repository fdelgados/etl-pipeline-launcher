#!/bin/bash

mkdir -p resources/git/hooks

git config core.hooksPath resources/git/hooks

echo $'#/bin/sh\n\nblack ./\n\npython lint.py --path ./src ./tests ./bin\n\nmake test' > resources/git/hooks/pre-commit

chmod a+x .git/hooks/pre-commit
