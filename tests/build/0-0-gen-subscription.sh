#!/bin/bash
cd ../test_out || exit 1
rm -f subscription.bin
timeout 0.5s python -m ectf25_design.gen_subscription secrets/secrets.json subscription.bin 0xDEADBEEF 0 63 1 || exit 1