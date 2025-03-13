#!/bin/bash

if [[ $# -eq 1 ]]; then # pass an argument to disable colors 
    NO_FORMAT="\033[0m"
    F_BOLD="\033[1m"
    C_MEDIUMPURPLE1="\033[38;5;141m"
    C_RED="\033[38;5;9m"
    C_GREEN="\033[38;5;2m"
fi

cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" || exit
. ../.venv/bin/activate
pip install -e ../test_out/design/

for test in tests/build/*.sh; do
    if [[ $test == tests/build/x-*.sh ]]; then
        continue
    fi
    echo -e "${C_MEDIUMPURPLE1}${F_BOLD}Running test $test${NO_FORMAT}"
    bash "$test"
    result=$?
    if [[ $test == *-should-fail.sh ]]; then
        if [ $result -eq 0 ]; then
            echo -e "${C_RED}${F_BOLD}Test $test should have failed but didn't${NO_FORMAT}"
            exit 1
        fi
    else
        if [ $result -ne 0 ]; then
            if [ $result -eq 124 ]; then 
                echo -e "${C_RED}${F_BOLD}Test $test failed because it timed out${NO_FORMAT}"
            else 
                echo -e "${C_RED}${F_BOLD}Test $test failed${NO_FORMAT}"
            fi
            exit 1
        fi
    fi
done

echo -e "${C_GREEN}${F_BOLD}All tests passed!${NO_FORMAT}"