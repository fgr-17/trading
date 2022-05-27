#!/bin/bash


function style() {
    printf "\n===================================\n"
    printf "Checking code style ...\n"
    printf "===================================\n\n"
    pycodestyle --show-source --show-pep8 --format=pylint ../
    pycodestyle --format=pylint ../
    return $?
}


lint() {
    printf "\n===================================\n"
    printf "Linting source files ...\n"
    printf "===================================\n\n"
    pylint ../
    return $?
}

test() {
    printf "\n===================================\n"
    printf "Running unit tests ...\n"
    printf "===================================\n\n"
    pytest ../
    return $?
}



MAIN_FILE=main.py


style
lint
test


