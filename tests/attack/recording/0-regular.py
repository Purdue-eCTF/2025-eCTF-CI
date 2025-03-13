#!/usr/bin/env python3
import asyncio
import json
import os
import sys

from ectf25.utils.decoder import DecoderIntf


def conn():
    r = DecoderIntf("/dev/ttyACM0", timeout=5, write_timeout=5)

    return r


async def main():
    with open("../attack_out/recording.json") as f:
        recording = json.load(f)
    r = conn()

    for msg in recording:
        frame = bytearray.fromhex(msg["encoded"])
        print(await asyncio.wait_for(asyncio.to_thread(r.decode, frame), 10))


if __name__ == "__main__":
    try:
        asyncio.run(asyncio.wait_for(main(), 30))
    except TimeoutError:
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(124)
