#!/bin/bash

# todo encoded frame with invalid channel

timeout 5s python modified_tester.py --secrets ../test_out/global.secrets --timing --port /dev/ttyACM0 rand2 -s 40 -e 41 -c 2 || exit $?
# if [ "$?" -ne 0 ]; then
#   exit 1
# fi

# rm decoded_frames