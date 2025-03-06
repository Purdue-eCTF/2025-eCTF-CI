#!/bin/sh

timeout 30s python -m ectf25.tv.run "$IP" "$CHANNEL_4_PORT" /dev/ttyACM0 || exit $?