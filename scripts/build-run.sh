#!/bin/bash


function style() {
    printf "Checking code style ...\n"
    # pycodestyle --show-source --show-pep8 --format=pylint ../
    pycodestyle --format=pylint ../main.py
    pycodestyle --format=pylint ../broker
    return $?
}


lint() {
    printf "Linting source files ...\n"
    pylint ../broker
    return $?
}

test() {
    printf "Running unit tests ...\n"
    pytest ../
    return $?
}



MAIN_FILE=main.py


style
if [ $? -ne 0 ]; then
    printf "Please check code style before continue...\n"
    exit 1
fi

lint
if [ $? -ne 0 ]; then
    printf "Please check lint issues before continue...\n"
    exit 1
fi

test
if [ $? -ne 0 ]; then
    printf "Please test cases before continue...\n"
    exit 1
fi

cd ..
./${MAIN_FILE}
