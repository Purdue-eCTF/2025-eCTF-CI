#!/bin/sh 

timeout 15s python -m ectf25.tv.subscribe ../attack_out/pirated.sub /dev/ttyACM0 || exit $?

timeout 30s python -m ectf25.tv.run "$IP" "$CHANNEL_3_PORT" /dev/ttyACM0 || exit $?