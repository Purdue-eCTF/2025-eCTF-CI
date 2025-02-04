#!/bin/bash
timeout 0.5s python -m ectf25.tv.list /dev/ttyACM0 || exit 1

# TODO check output
