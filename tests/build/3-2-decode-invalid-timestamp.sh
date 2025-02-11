#!/bin/bash

# invalid timestamps (non-increasing)
timeout 5s python modified_tester.py --secrets ../test_out/global.secrets --timing --port /dev/ttyACM0 rand2 -s 40 -e 40 -c 1 && exit 1

# invalid timestamps (outside subscription)
timeout 5s python modified_tester.py --secrets ../test_out/global.secrets --timing --port /dev/ttyACM0 rand2 -s 96 -e 96 -c 1 && exit 1


# if [ "$?" -ne 0 ]; then
#   exit 1
# fi

# rm decoded_frames