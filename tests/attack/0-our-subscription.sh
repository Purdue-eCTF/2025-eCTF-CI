#!/bin/sh 

timeout 15s python -m ectf25.tv.subscribe ../attack_out/our.sub /dev/ttyACM0 || exit $?