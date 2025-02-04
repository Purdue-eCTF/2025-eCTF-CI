#!/bin/bash
# todo either input encoded frames + output or run encoder on rpi

echo "TODO: 1-1-decode.sh"

timeout 5s python -m ectf25.utils.tester --secrets ../test_out/secrets/secrets.json --port /dev/ttyACM0 --dump-decoded ../test_out/decoded_frames.json rand -n 20 || exit 1

# rm decoded_frames