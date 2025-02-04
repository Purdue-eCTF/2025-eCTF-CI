#!/bin/sh
timeout 5s python modified_tester.py --secrets secrets/secrets.json --stub-decoder --perf --dump-raw test_out/raw_frames.json --dump-encoded test_out/encoded_frames.json json frames/x_c0.json 	

if [ "$?" -ne 0 ]; then
  exit 1
fi