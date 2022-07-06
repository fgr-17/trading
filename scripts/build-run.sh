#!/bin/bash

MAX_LINE_LENGTH=200
SOURCE_PATH='../src'

function style() {
    printf "Checking code style ...\n"
    # pycodestyle --show-source --show-pep8 --format=pylint ../
    pycodestyle --format=pylint --max-line-length=$MAX_LINE_LENGTH "${SOURCE_PATH}/main.py"
    pycodestyle --format=pylint --max-line-length=$MAX_LINE_LENGTH "${SOURCE_PATH}/broker"
    return $?
}

function lint() {
    printf "Linting source files ...\n"
    pylint --max-line-length=$MAX_LINE_LENGTH "${SOURCE_PATH}/broker"
    pylint --max-line-length=$MAX_LINE_LENGTH "${SOURCE_PATH}/main.py"
    return $?
}

function test() {
    printf "Running unit tests ...\n"
    pytest "${SOURCE_PATH}"
    return $?
}

MAIN_FILE="${SOURCE_PATH}/main.py"

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

${MAIN_FILE}
