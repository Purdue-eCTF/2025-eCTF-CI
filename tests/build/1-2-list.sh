#!/bin/bash
output="$(timeout 5s python modified_list.py /dev/ttyACM0 2>&1)" || exit $?
printf "%s" "$output"
printf "%s" "$output" | grep "Reported 0 subscribed channels" || exit $?