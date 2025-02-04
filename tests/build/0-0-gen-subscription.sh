#!/bin/bash
timeout 0.5s python -m ectf25_design.gen_subscription secrets/secrets.json test_out/subscription.bin 0xDEADBEEF 0 63 1

if [ "$?" -ne 0 ]; then
  exit 1
fi