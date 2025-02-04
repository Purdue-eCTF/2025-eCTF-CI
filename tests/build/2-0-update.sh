#!/bin/bash

timeout 2s python modified_subscribe.py ../test_out/subscription.bin /dev/ttyACM0 || exit $?
