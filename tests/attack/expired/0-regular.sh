#!/bin/sh 

timeout 15s python -m ectf25.tv.subscribe ../attack_out/expired.sub /dev/ttyACM0 || exit $?

timeout 15s python modified_tv.py "$IP" "$CHANNEL_2_PORT" /dev/ttyACM0 || exit $?