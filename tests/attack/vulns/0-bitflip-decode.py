import json
import os

from ectf25.utils.decoder import DecoderIntf
from pwn import *


def conn():
    r = DecoderIntf("/dev/ttyACM0")

    return r


def main():
    r = conn()
    s = remote(os.environ["IP"], os.environ["CHANNEL_1_PORT"])

    payload = json.loads(s.recvline())
    frame = bytearray.fromhex(payload["encoded"])

    for byte_offset in range(len(frame)):
        for bit_offset in range(8):
            new_frame = frame[:]
            new_frame[byte_offset] ^= 1 << bit_offset
            print(r.decode(new_frame))


if __name__ == "__main__":
    main()
