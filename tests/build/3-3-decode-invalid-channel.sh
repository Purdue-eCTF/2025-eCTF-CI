#!/bin/bash

rm -f ../test_out/subscription.bin
timeout 10s python -m ectf25_design.gen_subscription ../test_out/global.secrets ../test_out/subscription.bin 0xDEADBEEF 128 160 1 || exit $?

if timeout 5s python modified_tester.py --secrets ../test_out/global.secrets --timing --port /dev/ttyACM0 rand2 -s 130 -e 130 -c 2; then
	exit 1
fi

exit 0