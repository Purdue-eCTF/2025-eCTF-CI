#!/bin/bash
rm -f ../test_out/subscription.bin
timeout 10s python -m ectf25_design.gen_subscription ../test_out/secrets/secrets.json ../test_out/subscription.bin 0xDEADBEEF 0 63 1 || exit $?