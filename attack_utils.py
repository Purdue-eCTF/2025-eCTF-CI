import asyncio
import inspect
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
    with open("../test_out/README.md") as f:
        return int(list(f)[3].split(" ")[-1], 16)


def p32(i):
    return struct.pack("<I", i)


def p64(i):
    return struct.pack("<Q", i)


def u32(s):
    return struct.unpack("<I", s)


def u64(s):
    return struct.unpack("<Q", s)


def match_flag(s):
    if isinstance(s, str):
        decoded = s
    else:
        decoded = s.decode("utf-8", errors="ignore")
    m = re.search(
        r"([a-fA-F0-9]{16})\^ flag \^",
        decoded,
    )

    if m:
        return m.group(1)
    else:
        return None


def wrap_flag(s, scenario):
    if isinstance(s, str):
        decoded = s
    else:
        decoded = s.decode("utf-8", errors="ignore")
    flag = match_flag(decoded)
    if flag is None:
        print(f"Invalid flag {decoded}")
        return None
    return f"ectf{{{scenario}_{flag}}}"


def recording_playback():
    with open("../test_out/recording.json") as f:
        recording = json.load(f)
    r = conn()

    for msg in recording[:10]:
        frame = bytearray.fromhex(msg["encoded"])
        decoded = r.decode(frame)
        if flag := match_flag(decoded):
            return flag


class LimitedAttackTV(TV):
    # modifications:
    # print decode on one line
    # exit immediately if flag is decoded
    # decodes first 10 frames only
    def __init__(
        self, sat_host: str, sat_port: int, dec_port: str, dec_baud: int = 115200
    ):
        self.flag = None
        super().__init__(sat_host, sat_port, dec_port, dec_baud)

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

                    if flag := match_flag(decoded):
                        self.flag = flag  # returning :tm:
                        return
                    i += 1
        except Exception:
            logger.critical("Decoder crashed!")
            self.crash.set()
            raise


def run_attack(f, timeout: int):
    if inspect.iscoroutinefunction(f):
        coro = f()
    else:
        coro = asyncio.to_thread(f)
    try:
        asyncio.run(asyncio.wait_for(coro, timeout))
    except TimeoutError:
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(124)
