#!/bin/bash

NO_FORMAT="\033[0m"
F_BOLD="\033[1m"
C_MEDIUMPURPLE1="\033[38;5;141m"
C_RED="\033[38;5;9m"
C_GREEN="\033[38;5;2m"

cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" || exit
. ../.venv/bin/activate

read -r IP CHANNEL_1_PORT CHANNEL_2_PORT CHANNEL_3_PORT CHANNEL_4_PORT < ports.txt
export IP CHANNEL_1_PORT CHANNEL_2_PORT CHANNEL_3_PORT CHANNEL_4_PORT

for test in tests/attack/global/*.sh tests/attack/"$1"/*.sh; do
    if [[ $test == tests/attack/x-*.sh ]]; then
        continue
    fi
    echo -e "${C_MEDIUMPURPLE1}${F_BOLD}Running test $test${NO_FORMAT}"
    bash "$test" 2>&1 | tee temp_output
    grep -aEo "[a-z0-9]{16}^ flag ^" temp_output | sed "s/^/POTENTIAL FLAG: ectf{$1_/"
done

rm temp_output

if [ $passed -ne $num_tests ]; then
    echo -e "${C_RED}${F_BOLD}Passed ${passed}/${num_tests} tests${NO_FORMAT}"
fi
echo -e "${C_GREEN}${F_BOLD}All tests passed!${NO_FORMAT}"