#!/usr/bin/env python3
import json

from ectf25.utils.decoder import DecoderIntf


def conn():
    r = DecoderIntf("/dev/ttyACM0")

    return r


def main():
    with open("../attack_out/recording.json") as f:
        recording = json.load(f)
    r = conn()

    for msg in recording:
        frame = bytearray.fromhex(msg["encoded"])
        print(r.decode(frame))


if __name__ == "__main__":
    main()
