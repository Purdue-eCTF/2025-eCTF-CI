#!/bin/sh 

# intentionally don't exit on failure in case nosub works
timeout 15s python -m ectf25.tv.subscribe ../test_out/pirated.sub /dev/ttyACM0
status=$?
if [ "$status" -eq 124 ]; then
	exit $status;
fi

timeout 15s python modified_tv.py "$IP" "$CHANNEL_3_PORT" /dev/ttyACM0 || exit $?