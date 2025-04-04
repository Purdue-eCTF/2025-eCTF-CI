#!/usr/bin/env python3
import sys

from loguru import logger

from attack_utils import recording_playback, run_attack

logger.remove()
logger.add(sys.stdout, level="INFO")


def main():
    flag = recording_playback()
    if flag:
        print(f"POTENTIAL FLAG: ectf{{recording_{flag}}}")


if __name__ == "__main__":
    run_attack(main, 30)
