#!/usr/bin/env python3
import asyncio
import os
import sys

from ectf25.utils.decoder import DecoderIntf
from loguru import logger

logger.remove()
logger.add(sys.stdout, level="SUCCESS")


def conn():
    r = DecoderIntf("/dev/ttyACM0", timeout=5, write_timeout=5)

    return r


async def main():
    r = conn()

    with open("../attack_out/own.sub", "rb") as f:
        subscription = bytearray(f.read())

    print(f"orig listing: {r.list()}")
    for byte_offset in range(len(subscription)):
        for bit_offset in range(8):
            new_subscription = subscription[:]
            new_subscription[byte_offset] ^= 1 << bit_offset
            try:
                print(byte_offset, bit_offset)
                orig_list = await asyncio.wait_for(asyncio.to_thread(r.list), 10)
                await asyncio.wait_for(
                    asyncio.to_thread(r.subscribe, new_subscription), 10
                )
                new_list = await asyncio.wait_for(asyncio.to_thread(r.list), 10)
                if new_list != orig_list:
                    print(
                        f"POTENTIAL VULNERABILITY: flipping byte {byte_offset} bit {bit_offset} in subscription results in {new_list}"
                    )
            except TimeoutError:
                # assume decoder crashed
                print(
                    f"POTENTIAL VULNERABILITY: flipping byte {byte_offset} bit {bit_offset} in subscription caused decoder to crash"
                )
                sys.stdout.flush()
                os._exit(0)

            except Exception as e:
                print(e)


if __name__ == "__main__":
    try:
        asyncio.run(asyncio.wait_for(main(), timeout=90))
    except TimeoutError:
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(124)
