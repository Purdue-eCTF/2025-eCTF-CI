#!/usr/bin/env python3
# add extra bytes on the end of encoded frame and see if team crashes or decodes a valid frame
# used to detect teams which read as many bytes as possible from uart and don't validate length
import json
import os
import random
import socket
import sys

from loguru import logger

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
    # don't do too long otherwise it will overrun end buffer and always segfault
    for append_length in range(1, 33):
        rand_bytes = random.randbytes(append_length)
        new_frame = frame + rand_bytes
        try:
            decoded = r.decode(new_frame)
        except TimeoutError:
            # assume decoder crashed
            print(
                f"POTENTIAL VULNERABILITY: appending {append_length} random bytes ({rand_bytes.hex()}) to encoded frame caused decoder to crash"
            )
            sys.stdout.flush()
            os._exit(0)
        except Exception as e:
            print(e)
        else:
            if first_vuln:
                first_vuln = False
                print(
                    "POTENTIAL VULNERABILITY: appending random bytes to an encoded frame results in valid decode, Ctrl-F 'Append bytes details' in logs for more detail"
                )
            print(
                f"Append bytes details: appending {append_length} random bytes ({rand_bytes.hex()}) to encoded frame results in {decoded}"
            )


if __name__ == "__main__":
    run_attack(main, timeout=90)
