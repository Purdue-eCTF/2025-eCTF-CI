#!/bin/bash
output="$(timeout 0.5s python -m ectf25.tv.list /dev/ttyACM0 2>&1)" || exit 1
printf "%s" "$output"
printf "%s" "$output" | grep "Reported 0 subscribed channels"