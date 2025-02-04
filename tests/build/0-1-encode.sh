#!/bin/sh
timeout 5s python modified_tester.py --secrets ../test_out/secrets/secrets.json --stub-decoder --perf json ../frames/x_c0.json || exit 1