#!/bin/bash

timeout 0.5s python -m ectf25.tv.subscribe ../test_out/subscription.bin /dev/ttyACM0 || exit
