
# todo encoded frame with invalid channel

echo "TODO: 2-1-decode-invalid-channel-should-fail"

# timeout 5s python -m ectf25.utils.tester --secrets TODO --stub-encoder --num-frames 20 --port /dev/ttyACM0 --dump-decoded decoded_frames rand

# if [ "$?" -ne 0 ]; then
#   exit 1
# fi

# rm decoded_frames