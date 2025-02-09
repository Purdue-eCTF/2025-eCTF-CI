#!/bin/bash

timeout 5s python modified_subscribe.py ../test_out/subscription.bin /dev/ttyACM0 || exit $?
