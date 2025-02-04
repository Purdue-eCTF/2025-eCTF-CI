"""
Author: Ben Janis
Date: 2025

This source file is part of an example system for MITRE's 2025 Embedded System CTF
(eCTF). This code is being provided only for educational purposes for the 2025 MITRE
eCTF competition, and may not meet MITRE standards for quality. Use this code at your
own risk!

Copyright: Copyright (c) 2025 The MITRE Corporation
"""

import argparse
import time

from ectf25.utils.decoder import DecoderIntf
from loguru import logger


def main():
	# Define and parse command line arguments
	parser = argparse.ArgumentParser(
		prog="ectf25.tv.list",
		description="List the channels with a valid subscription on the Decoder",
	)
	parser.add_argument(
		"port",
		help="Serial port to the Decoder (see https://rules.ectf.mitre.org/2025/getting_started/boot_reference for platform-specific instructions)",
	)
	args = parser.parse_args()

	# Open Decoder interface
	decoder = DecoderIntf(args.port)

	# Run the list command
	start = time.perf_counter()
	subscriptions = decoder.list()
	end = time.perf_counter()

	# Print the results
	for channel, start, end in subscriptions:
		logger.info(f"Found subscription: Channel {channel} {start}:{end}")

	if end - start < 0.5:
		logger.success("List successful")
	else:
		logger.error(f"List timed out: {end - start}s")
		exit(1)


if __name__ == "__main__":
	main()
