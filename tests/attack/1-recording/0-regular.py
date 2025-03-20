#!/usr/bin/env python3
import sys

from loguru import logger

from attack_utils import recording_playback, run_attack

logger.remove()
logger.add(sys.stdout, level="INFO")


if __name__ == "__main__":
    run_attack(recording_playback, 30)
