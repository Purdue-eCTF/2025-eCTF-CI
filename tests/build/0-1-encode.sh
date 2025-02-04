#!/bin/sh
cd ../test_out || exit 1
timeout 5s python modified_tester.py --secrets secrets/secrets.json --stub-decoder --perf json ../frames/x_c0.json || exit 1