#!/bin/sh 

timeout 15s python -m ectf25.tv.subscribe ../attack_out/expired.sub /dev/ttyACM0 || exit $?

timeout 30s python -m ectf25.tv.run "$IP" "$CHANNEL_2_PORT" /dev/ttyACM0 || exit $?