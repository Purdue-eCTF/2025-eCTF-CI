#!/bin/sh
echo Setting up attacks
if [ -f ../test_out/design/setup.py ]; then
    pip uninstall ectf25_design
else
    pip install -e ../test_out/design/ || pip uninstall ectf25_design
fi

read -r IP CHANNEL_0_PORT CHANNEL_1_PORT CHANNEL_2_PORT CHANNEL_3_PORT CHANNEL_4_PORT < ../test_out/ports.txt
export IP CHANNEL_0_PORT CHANNEL_1_PORT CHANNEL_2_PORT CHANNEL_3_PORT CHANNEL_4_PORT

export PYTHONPATH="$PWD"

timeout 15s python -m ectf25.tv.subscribe ../test_out/own.sub /dev/ttyACM0 || exit $?
timeout 15s python -m ectf25.tv.subscribe ../test_out/expired.sub /dev/ttyACM0 || exit $?
