#!/bin/sh

timeout 15s python modified_tester.py --stub-encoder json --hex ../attack_out/recording.json || exit $?