# modified to print decode on one line, and exit immediately if flag is decoded
"""
Author: Ben Janis
Date: 2025
Desc: Generates update blobs for eCTF decoder.

This source file is part of an example system for MITRE's 2025 Embedded System CTF
(eCTF). This code is being provided only for educational purposes for the 2025 MITRE
eCTF competition, and may not meet MITRE standards for quality. Use this code at your
own risk!

Copyright: Copyright (c) 2025 The MITRE Corporation
"""

import argparse
import re

from ectf25.tv import TV
from loguru import logger


class AttackTV(TV):
    def decode(self):
        """Serve frames from the queue to the Decoder, printing the decoded results"""
        logger.info("Starting Decoder loop")
        try:
            while not self.crash.is_set():
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
        except Exception:
            logger.critical("Decoder crashed!")
            self.crash.set()
            raise


def main():
    parser = argparse.ArgumentParser(
        prog="ectf25.tv",
        description="Run the TV, pulling frames from the satellite, decoding using"
        " the Decoder, and printing to the terminal",
    )
    parser.add_argument("sat_host", help="TCP host of the satellite")
    parser.add_argument("sat_port", type=int, help="TCP port of the satellite")
    parser.add_argument(
        "dec_port",
        help="Serial port to the Decoder (see https://rules.ectf.mitre.org/2025/getting_started/boot_reference for platform-specific instructions)",
    )
    parser.add_argument(
        "--baud", type=int, default=115200, help="Baud rate of the serial port"
    )
    args = parser.parse_args()

    # run the TV
    tv = AttackTV(args.sat_host, args.sat_port, args.dec_port, args.baud)
    tv.run()


if __name__ == "__main__":
    main()
