#!/usr/bin/env python3
import asyncio
import json

from ectf25.utils.decoder import DecoderIntf


def conn():
    r = DecoderIntf("/dev/ttyACM0", timeout=10, write_timeout=10)

    return r


async def main():
    with open("../attack_out/recording.json") as f:
        recording = json.load(f)
    r = conn()

    for msg in recording:
        frame = bytearray.fromhex(msg["encoded"])
        print(r.decode(frame))


if __name__ == "__main__":
    asyncio.run(asyncio.wait_for(main(), 30))
