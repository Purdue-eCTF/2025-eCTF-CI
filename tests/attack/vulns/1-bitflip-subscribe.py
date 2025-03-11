#!/usr/bin/env python3
import sys

from ectf25.utils.decoder import DecoderIntf
from loguru import logger

logger.remove()
logger.add(sys.stdout, level="SUCCESS")


def conn():
    r = DecoderIntf("/dev/ttyACM0")

    return r


def main():
    r = conn()

    with open("../attack_out/our.sub", "rb") as f:
        subscription = bytearray(f.read())

    print(f"orig listing: {r.list()}")
    for byte_offset in range(len(subscription)):
        for bit_offset in range(8):
            new_subscription = subscription[:]
            new_subscription[byte_offset] ^= 1 << bit_offset
            try:
                print(byte_offset, bit_offset)
                orig_list = r.list()
                r.subscribe(new_subscription)
                new_list = r.list()
                if new_list != orig_list:
                    print(
                        f"POTENTIAL VULNERABILITY: flipping byte {byte_offset} bit {bit_offset} results in {new_list}"
                    )
            except Exception as e:
                print(e)


if __name__ == "__main__":
    main()
