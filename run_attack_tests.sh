#!/bin/bash
if [[ $# -eq 0 ]]; then # pass an argument to disable colors 
    NO_FORMAT="\033[0m"
    F_BOLD="\033[1m"
    C_MEDIUMPURPLE1="\033[38;5;141m"
    C_RED="\033[38;5;9m"
    C_GREEN="\033[38;5;2m"
fi

cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" || exit
. ../.venv/bin/activate
if [[ -f ../test_out/design/setup.py ]]; then
    pip uninstall ectf25_design
else
    pip install -e ../test_out/design/ || pip uninstall ectf25_design
fi

read -r IP CHANNEL_0_PORT CHANNEL_1_PORT CHANNEL_2_PORT CHANNEL_3_PORT CHANNEL_4_PORT < ../test_out/ports.txt
export IP CHANNEL_0_PORT CHANNEL_1_PORT CHANNEL_2_PORT CHANNEL_3_PORT CHANNEL_4_PORT
export LOGURU_LEVEL=INFO
export PYTHONPATH=$PWD

trap "rm -f temp_output" EXIT
for test in tests/attack/*/*; do
    if [[ $test == */x-*.sh ]] || [[ $test == *.md ]]; then
        continue
    fi
    scenario=$(basename "$(dirname "$test")")
    echo -e "${C_MEDIUMPURPLE1}${F_BOLD}Running test $test${NO_FORMAT}"
    "$test" 2>&1 | tee temp_output
    if [[ ${PIPESTATUS[0]} -eq 124 ]]; then 
        echo -e "${C_RED}${F_BOLD}Test $test failed because it timed out${NO_FORMAT}"
    fi

    if [[ $scenario != 0-global ]]; then # global tests handle this themselves
        grep -aEo "[a-z0-9]{16}\^ flag \^" temp_output | sed "s/^/POTENTIAL FLAG: ectf{${scenario}_/;s/\^ flag \^$/}/"
    fi

    if ! timeout 3s python3 -m ectf25.tv.list /dev/ttyACM0 >/dev/null 2>&1; then
        echo "Decoder crashed, rebooting"
        ./power_cycle.sh 1
    fi
done

echo -e "${C_MEDIUMPURPLE1}${F_BOLD}All tests complete!${NO_FORMAT}"