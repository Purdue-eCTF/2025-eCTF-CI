#!/usr/bin/env python3
import asyncio
import json
import os
import sys

from ectf25.utils.decoder import DecoderIntf
from loguru import logger

from attack_utils import recording_playback, run_attack

logger.remove()
logger.add(sys.stdout, level="INFO")


def conn():
    r = DecoderIntf("/dev/ttyACM0", timeout=5, write_timeout=5)

    return r


if __name__ == "__main__":
    run_attack(recording_playback, 30)
