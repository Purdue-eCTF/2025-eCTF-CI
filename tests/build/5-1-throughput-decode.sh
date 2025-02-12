#!/bin/bash

for i in {1..4}; do
	rm -f ../test_out/subscription.bin
	timeout 10s python -m ectf25_design.gen_subscription ../test_out/global.secrets ../test_out/subscription.bin 0xDEADBEEF 0 18446744073709551615 "$i" || exit $?
	timeout 5s python modified_subscribe.py ../test_out/subscription.bin /dev/ttyACM0 || exit $?
done

timeout 120s python -m ectf25.utils.stress_test --test-size 10000 encode --dump ../test_out/stress_test_encoded_frames.json ../test_out/global.secrets
return_code=$?
if [ $return_code -ne 255 ]; then
	exit $return_code
fi

LOGURU_LEVEL=INFO timeout 120s python -m ectf25.utils.stress_test --test-size 10000 decode /dev/ttyACM0 ../test_out/stress_test_encoded_frames.json || exit $?
