#!/usr/bin/env python3
# bitflip each bit in the encoded frame and see if decoder crashes or responds with a successful decrypt
# used to detect teams that don't verify length fields in the frame, etc
import json
import os
import socket
import sys

from loguru import logger
from serial import SerialTimeoutException

from attack_utils import conn, run_attack

logger.remove()
logger.add(sys.stdout, level="SUCCESS")


def main():
    r = conn()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((os.environ["IP"], int(os.environ["CHANNEL_1_PORT"])))

    buf = b""
    while b"\n" not in buf:
        buf += s.recv(1024)
    payload = json.loads(buf.split(b"\n")[0])
    frame = bytearray.fromhex(payload["encoded"])

    first_vuln = True
    for byte_offset in range(len(frame)):
        for bit_offset in range(8):
            new_frame = frame[:]
            new_frame[byte_offset] ^= 1 << bit_offset
            try:
                print(byte_offset, bit_offset)
                decoded = r.decode(new_frame)
            except SerialTimeoutException:
                # assume decoder crashed
                print(
                    f"POTENTIAL VULNERABILITY: flipping byte {byte_offset} bit {bit_offset} in encoded frame caused decoder to crash"
                )
                sys.stdout.flush()
                os._exit(0)
            except Exception as e:
                print(e)
            else:
                if first_vuln:
                    first_vuln = False
                    print(
                        "POTENTIAL VULNERABILITY: flipping bits in encoded frame results in valid decode, Ctrl-F 'Decode bitflip details' in logs for more detail"
                    )
                print(
                    f"Decode bitflip details: flipping byte {byte_offset} bit {bit_offset} in encoded frame results in {decoded}"
                )


if __name__ == "__main__":
    run_attack(main, timeout=90)
