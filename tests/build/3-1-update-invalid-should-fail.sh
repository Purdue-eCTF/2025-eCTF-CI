#!/bin/bash
# todo bad file

timeout 5s python modified_subscribe.py <(head -c 256 /dev/urandom) /dev/ttyACM0
