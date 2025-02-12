test case 1: sanity check

-   1.0 generate subscription
-   1.1 test encode only
-   1.2 ensure list without any subscriptions returns 0 channels

test case 2: encode/decode

-   2-0: update subscription
-   2-1: ensure list returns 1 channel
-   2-2: decode w/ random frames
-   2-3: decode on channel 0 w/ random frames

test case 3: errors

-   3.1: update invalid (TODO)
-   3.2: decode invalid timestamp (both non-monotonic and outside subscription)
-   3.3: decode invalid channel w/ valid subscription for another channel

test case 4:

-   4.0: update w/ multiple subscriptions, ensure list returns 3 channels, decode w/ multiple subscriptions

test case 5: throughput

-   TODO `python -m ectf25.utils.stress_test --test-size 1000000 encode --dump test_out/stress_test_encoded_frames.json global.secrets`
