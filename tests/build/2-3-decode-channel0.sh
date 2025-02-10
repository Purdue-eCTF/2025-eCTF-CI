#!/bin/bash

timeout 5s python modified_tester.py --secrets ../test_out/global.secrets --timing --port /dev/ttyACM0 --dump-raw ../test_out/raw_frames.json --dump-decoded ../test_out/decoded_frames.json rand2 -s 32 -e 63 -c 0 || exit $?

diff <(python -m json.tool ../test_out/raw_frames.json) <(python -m json.tool ../test_out/decoded_frames.json) || exit $?


# rm decoded_frames