#!/bin/sh 

timeout 15s python -m ectf25.tv.subscribe ../test_out/own.sub /dev/ttyACM0 || exit $?
timeout 15s python -m ectf25.tv.subscribe ../test_out/expired.sub /dev/ttyACM0 || exit $?
