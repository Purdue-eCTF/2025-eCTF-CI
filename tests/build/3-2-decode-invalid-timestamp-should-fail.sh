#!/bin/bash
# todo encoded frame with invalid timestamps (non-increasing)

echo "TODO: 3-2-decode-invalid-timestamp-should-fail"
exit 1

# timeout 5s python modified_tester.py --secrets TODO --stub-encoder --num-frames 20 --port /dev/ttyACM0 --dump-decoded decoded_frames rand

# if [ "$?" -ne 0 ]; then
#   exit 1
# fi

# rm decoded_frames