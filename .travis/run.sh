#!/bin/bash

set -e

if [[ $TRAVIS_OS_NAME == 'osx' || "${TOXENV}" == "pypy" ]]; then
    # initialize our pyenv
    PYENV_ROOT="$HOME/.pyenv"
    PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
fi
source ~/.venv/bin/activate
tox