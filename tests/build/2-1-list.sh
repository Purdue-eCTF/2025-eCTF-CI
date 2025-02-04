#!/bin/bash
output="$(timeout 2s python modified_list.py /dev/ttyACM0 2>&1)" || exit 1
printf "%s" "$output"
printf "%s" "$output" | grep "Reported 1 subscribed channels" || exit 1