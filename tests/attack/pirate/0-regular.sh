#!/bin/sh 

timeout 15s python modified_tv.py "$IP" "$CHANNEL_3_PORT" /dev/ttyACM0 || exit $?