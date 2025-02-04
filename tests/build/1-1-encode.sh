#!/bin/sh
timeout 0.5s python modified_tester.py --secrets ../test_out/secrets/secrets.json --stub-decoder json ../frames/x_c0.json || exit $?