#!/bin/bash

# invalid timestamps (non-increasing)
if timeout 5s python modified_tester.py --secrets ../test_out/global.secrets --timing --port /dev/ttyACM0 rand2 -s 40 -e 40 -c 1; then
	exit 1
fi

# invalid timestamps (outside subscription)
if timeout 5s python modified_tester.py --secrets ../test_out/global.secrets --timing --port /dev/ttyACM0 rand2 -s 96 -e 96 -c 1; then
	exit 1
fi

exit 0