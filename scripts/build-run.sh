#!/bin/bash

MAX_LINE_LENGTH=200
SOURCE_PATH='../src'
CURRENT_DIR=$(pwd)

BROKER_PATH="${SOURCE_PATH}/broker"

bold=$(tput bold)
normal=$(tput sgr0)

packages=(
    "menu-app/main.py"
    "broker/broker"
    "broker/broker/auth"
)

function check_base_dir() {

    SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

    if [ $CURRENT_DIR != $SCRIPT_DIR ]; then
        printf "Error: run this script from its folder, please\n"
        exit 1
    fi

    return 0
}

function style() {
    printf "\n${bold}Checking code style ...${normal}\n"
    # pycodestyle --show-source --show-pep8 --format=pylint ../

    for package in ${packages[@]}; do
        printf "\t> Checking $package..."
        pycodestyle --format=pylint --max-line-length=$MAX_LINE_LENGTH "${SOURCE_PATH}/$package" --exclude='*build*'

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
    pytest -s "${SOURCE_PATH}"
    return $?
}

MAIN_FILE="${SOURCE_PATH}/menu-app/main.py"

INIT_PATH=$PWD

check_base_dir

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


printf "Building Broker Package"
cd $CURRENT_DIR
cd $BROKER_PATH
# python3 -m build
pip install --upgrade .
if [ $? -ne 0 ]; then
    printf "Couldn't build broker package, exiting...\n"
    exit 1
fi


cd $INIT_PATH
${MAIN_FILE}
