#!/bin/bash
rm -f ../test_out/subscription.bin
timeout 10s python -m ectf25_design.gen_subscription ../test_out/global.secrets ../test_out/subscription.bin 0xDEADBEEF 200 232 2 || exit $?
timeout 2s python modified_subscribe.py ../test_out/subscription.bin /dev/ttyACM0 || exit $?

rm -f ../test_out/subscription.bin
timeout 10s python -m ectf25_design.gen_subscription ../test_out/global.secrets ../test_out/subscription.bin 0xDEADBEEF 200 232 3 || exit $?
timeout 2s python modified_subscribe.py ../test_out/subscription.bin /dev/ttyACM0 || exit $?


output="$(timeout 2s python modified_list.py /dev/ttyACM0 2>&1)" || exit 1
printf "%s" "$output"
printf "%s" "$output" | grep "Reported 3 subscribed channels" || exit 1

timeout 5s python modified_tester.py --secrets ../test_out/global.secrets --timing --port /dev/ttyACM0 --dump-raw ../test_out/raw_frames.json --dump-decoded ../test_out/decoded_frames.json rand2 -s 200 -e 232 -c 2 3 || exit $?

diff <(python -m json.tool ../test_out/raw_frames.json) <(python -m json.tool ../test_out/decoded_frames.json) || exit $?
