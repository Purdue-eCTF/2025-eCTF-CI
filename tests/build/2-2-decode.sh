#!/bin/bash

timeout 5s python -m ectf25.utils.tester --secrets ../test_out/secrets/secrets.json --port /dev/ttyACM0 --dump-raw ../test_out/raw_frames.json --dump-decoded ../test_out/decoded_frames.json rand -n 20 -c 1 || exit 1

diff <(python -m json.tool ../test_out/raw_frames.json) <(python -m json.tool ../test_out/decoded_frames.json) || exit 1
# rm decoded_frames