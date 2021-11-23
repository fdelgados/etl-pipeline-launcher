#!/bin/bash

git config core.hooksPath doc/git_hooks

chmod a+x doc/git_hooks/pre-commit
