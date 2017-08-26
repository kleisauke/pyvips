#!/bin/bash

set -e

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    # install pyenv
    git clone --depth 1 https://github.com/pyenv/pyenv ~/.pyenv
    PYENV_ROOT="$HOME/.pyenv"
    PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"

    case "${TOXENV}" in
        py27)
            curl -O https://bootstrap.pypa.io/get-pip.py
            python get-pip.py --user
            ;;
        py33)
            pyenv install 3.3.6
            pyenv global 3.3.6
            ;;
        py34)
            pyenv install 3.4.6
            pyenv global 3.4.6
            ;;
        py35)
            pyenv install 3.5.3
            pyenv global 3.5.3
            ;;
        py36)
            pyenv install 3.6.1
            pyenv global 3.6.1
            ;;
        pypy)
            pyenv install "$PYPY_VERSION"
            pyenv global "$PYPY_VERSION"
            ;;
    esac
    pyenv rehash
    python -m pip install --user virtualenv
else
    pip install virtualenv
fi

python -m virtualenv ~/.venv
source ~/.venv/bin/activate
pip install tox