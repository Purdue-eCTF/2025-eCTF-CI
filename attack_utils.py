import asyncio
import json
import os
import sys

from ectf25.utils.decoder import DecoderIntf


def conn():
    r = DecoderIntf("/dev/ttyACM0", timeout=5, write_timeout=5)

    return r


def get_decoder_id():
    with open("../attack_out/README.md") as f:
        return int(list(f)[3].split(" ")[-1], 16)


async def recording_playback():
    with open("../attack_out/recording.json") as f:
        recording = json.load(f)
    r = conn()

    for msg in recording:
        frame = bytearray.fromhex(msg["encoded"])
        print(await asyncio.wait_for(asyncio.to_thread(r.decode, frame), 10))


def run_attack(f, timeout: int):
    try:
        asyncio.run(asyncio.wait_for(f(), timeout))
    except TimeoutError:
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(124)
