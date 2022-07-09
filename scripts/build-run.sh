#!/bin/bash

MAX_LINE_LENGTH=200
SOURCE_PATH='../src'

bold=$(tput bold)
normal=$(tput sgr0)

packages=(
    "main.py"
    "broker"
    "broker/auth"
)


function style() {
    printf "\n${bold}Checking code style ...${normal}\n"
    # pycodestyle --show-source --show-pep8 --format=pylint ../

    for package in ${packages[@]}; do
        printf "\t> Checking $package..."
        pycodestyle --format=pylint --max-line-length=$MAX_LINE_LENGTH "${SOURCE_PATH}/$package"

        if [ $? -ne 0 ]; then
            return 1
        fi

        printf "OK\n"

    done
    return 0
}

function lint() {
    printf "\n${bold}Linting source files ...${normal}\n"

    for package in ${packages[@]}; do
        printf "\t> Checking $package..."
        pylint --max-line-length=$MAX_LINE_LENGTH $SOURCE_PATH/$package

        if [ $? -ne 0 ]; then
            return 1
        fi

    done
    return 0
}

function test() {
    printf "\n${bold}Running unit tests ...${normal}\n"
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
    printf "Please check linter issues before continue...\n"
    exit 1
fi

test
if [ $? -ne 0 ]; then
    printf "Please test cases before continue...\n"
    exit 1
fi

${MAIN_FILE}
