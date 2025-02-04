#!/bin/bash
cd ../test_out || exit 1
timeout 0.5s python -m ectf25.tv.list /dev/ttyACM0 || exit 1

# TODO check output
