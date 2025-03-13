#!/usr/bin/env python3
import asyncio
import json
import os
import socket
import sys

from ectf25.utils.decoder import DecoderIntf
from loguru import logger

logger.remove()
logger.add(sys.stdout, level="SUCCESS")


def conn():
    r = DecoderIntf("/dev/ttyACM0", timeout=10, write_timeout=10)

    return r


async def main():
    r = conn()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((os.environ["IP"], int(os.environ["CHANNEL_1_PORT"])))

    buf = b""
    while b"\n" not in buf:
        buf += s.recv(1024)
    payload = json.loads(buf.split(b"\n")[0])
    frame = bytearray.fromhex(payload["encoded"])

    for byte_offset in range(len(frame)):
        for bit_offset in range(8):
            new_frame = frame[:]
            new_frame[byte_offset] ^= 1 << bit_offset
            try:
                print(byte_offset, bit_offset)
                decoded = await asyncio.wait_for(
                    asyncio.to_thread(r.decode, new_frame), 10
                )
            except TimeoutError:
                # assume decoder crashed
                print(
                    f"POTENTIAL VULNERABILITY: flipping byte {byte_offset} bit {bit_offset} caused decoder to crash"
                )
                return
            except Exception as e:
                print(e)
            else:
                print(
                    f"POTENTIAL VULNERABILITY: flipping byte {byte_offset} bit {bit_offset} results in {decoded}"
                )


if __name__ == "__main__":
    asyncio.run(asyncio.wait_for(main(), timeout=90))
