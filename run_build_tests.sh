#!/bin/bash

NO_FORMAT="\033[0m"
F_BOLD="\033[1m"
C_MEDIUMPURPLE1="\033[38;5;141m"
C_RED="\033[38;5;9m"
C_GREEN="\033[38;5;2m"

export TEST_BUILD_DIR=$1

for test in tests/build/*.sh; do
    if [[ $test == tests/build/x-*.sh ]]; then
        continue
    fi
    echo -e "${C_MEDIUMPURPLE1}${F_BOLD}Running test $test${NO_FORMAT}"
    sh $test
    result=$?
    if [[ $test == *-should-fail.sh ]]; then
        if [ $result -eq 0 ]; then
            echo -e "${C_RED}${F_BOLD}Test $test should have failed but didn't${NO_FORMAT}"
            exit 1
        fi
    else
        if [ $result -ne 0 ]; then
            echo -e "${C_RED}${F_BOLD}Test $test failed${NO_FORMAT}"
            exit 1
        fi
    fi
done

echo -e "${C_GREEN}${F_BOLD}All tests passed!${NO_FORMAT}"