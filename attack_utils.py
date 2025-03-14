import asyncio
import json
import os
import re
import struct
import sys

from ectf25.tv import TV
from ectf25.utils.decoder import DecoderIntf
from loguru import logger


def conn():
    r = DecoderIntf("/dev/ttyACM0", timeout=5, write_timeout=5)

    return r


def get_decoder_id():
    with open("../attack_out/README.md") as f:
        return int(list(f)[3].split(" ")[-1], 16)


def p32(i):
    return struct.pack("<I", i)


def p64(i):
    return struct.pack("<Q", i)


async def recording_playback():
    with open("../attack_out/recording.json") as f:
        recording = json.load(f)
    r = conn()

    for msg in recording[:10]:
        frame = bytearray.fromhex(msg["encoded"])
        print(await asyncio.wait_for(asyncio.to_thread(r.decode, frame), 10))


class LimitedAttackTV(TV):
    # attack tv but limited to first 10 frames
    def decode(self):
        """Serve frames from the queue to the Decoder, printing the decoded results"""
        logger.info("Starting Decoder loop")
        try:
            i = 0
            while not self.crash.is_set() and i < 10:
                if not self.to_decode.empty():
                    # Get an encoded frame from the queue
                    encoded = self.to_decode.get_nowait()

                    # Send the frame to be decoded
                    decoded = self.decoder.decode(encoded)

                    # Print the frame
                    try:
                        # if the frame contains printable text, pretty print it
                        logger.info((b"\n" + decoded).decode("utf-8"))
                    except UnicodeDecodeError:
                        # if we can't decode bytes, fall back to just printing the frame
                        logger.info(decoded)

                    if re.search(
                        r"[a-fA-F0-9]{16}\^ flag \^",
                        decoded.decode("utf-8", errors="ignore"),
                    ):
                        return
                    i += 1
        except Exception:
            logger.critical("Decoder crashed!")
            self.crash.set()
            raise


def run_attack(f, timeout: int):
    try:
        asyncio.run(asyncio.wait_for(f(), timeout))
    except TimeoutError:
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(124)
