#!/bin/bash
rm -f ../test_out/subscription.bin
timeout 10s python -m ectf25_design.gen_subscription ../test_out/global.secrets ../test_out/subscription.bin 0xDEADBEEF 32 63 1 || exit $?