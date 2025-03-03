#!/bin/sh

timeout 30s python modified_tester.py --stub-encoder json --hex ../attack_out/recording.json || exit $?