#!/bin/bash
echo Setting up attacks
pip uninstall -y ectf25_design
if [[ ! -f ../test_out/design/setup.py ]]; then
    pip install -e ../test_out/design/ || pip uninstall -y ectf25_design
fi

read -r IP CHANNEL_0_PORT CHANNEL_1_PORT CHANNEL_2_PORT CHANNEL_3_PORT CHANNEL_4_PORT < ../test_out/ports.txt
export IP CHANNEL_0_PORT CHANNEL_1_PORT CHANNEL_2_PORT CHANNEL_3_PORT CHANNEL_4_PORT

PYTHONPATH="$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" && pwd)"
export PYTHONPATH

timeout 15s python -m ectf25.tv.subscribe ../test_out/own.sub /dev/ttyACM0 || exit $?
timeout 15s python -m ectf25.tv.subscribe ../test_out/expired.sub /dev/ttyACM0 || exit $?
