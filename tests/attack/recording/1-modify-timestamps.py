#!/usr/bin/env python3
import json
import struct

from ectf25.utils.decoder import DecoderIntf


def conn():
    r = DecoderIntf("/dev/ttyACM0")

    return r


def main():
    with open("../attack_out/recording.json") as f:
        recording = json.load(f)
    r = conn()

    listing = r.list()
    channel_1 = next(c for c in listing if c[0] == 1)
    for msg, timestamp in zip(recording, range(channel_1[1], channel_1[2]), strict=False):
        new_frame = bytearray.fromhex(msg["encoded"])
        new_frame[4:12] = struct.pack("<Q", timestamp)
        print(r.decode(new_frame))


if __name__ == "__main__":
    main()
