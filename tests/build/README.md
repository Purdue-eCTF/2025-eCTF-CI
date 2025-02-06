test case 1: sanity check

-   1.0 generate subscription
-   1.1 test encode only
-   1.2 test list without any subscriptions returns 0 channels

test case 2: encode/decode

-   2-0: update subscription
-   2-1: test list returns 1 channel
-   2-2: test decode on rand

test case 3: errors

-   3.1:update invalid
-   3.2: decode invalid timestamp
-   3.3: decode invalid channel

TODO `python -m ectf25.utils.stress_test --test-size 1000000 encode --dump test_out/stress_test_encoded_frames.json global.secrets`
