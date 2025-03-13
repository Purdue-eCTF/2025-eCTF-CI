#!/usr/bin/env python3
import asyncio
import json
import struct
import subprocess

from ectf25.utils.decoder import DecoderIntf


def conn():
    r = DecoderIntf("/dev/ttyACM0")

    return r


async def main():
    with open("../attack_out/recording.json") as f:
        recording = json.load(f)
    r = conn()

    listing = r.list()
    channel_1 = next(c for c in listing if c[0] == 1)

    first_timestamp = recording[0]["timestamp"]
    first_frame = bytes.fromhex(recording[0]["encoded"])
    offset = first_frame.index(struct.pack("<Q", first_timestamp))
    print("found timestamp offset", offset)

    try:
        for msg, timestamp in zip(
            recording, range(channel_1[1], channel_1[2]), strict=False
        ):
            new_frame = bytearray.fromhex(msg["encoded"])
            new_frame[offset : offset + 8] = struct.pack("<Q", timestamp)
            print(await asyncio.wait_for(asyncio.to_thread(r.decode, new_frame), 10))
    except TimeoutError:
        print("Decoder crashed")


if __name__ == "__main__":
    asyncio.run(main())
