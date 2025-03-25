#!/bin/bash

power_cycle() {
	USB_RETRY_COUNT=0
	/usr/sbin/uhubctl -l 1-1 -a cycle > /dev/null 2>/dev/null

	echo -n "Waiting for USB to connect"
	while [ ! -e "/dev/disk/by-label/DAPLINK" ]; do
        if [ "$USB_RETRY_COUNT" -gt 100 ]; then
			echo -e "%%FAILED%%\nReason: USB connection timeout"
			exit 47
		fi
		echo -n "."
        sleep 0.2
		((USB_RETRY_COUNT++))
	done
	echo
}

if [[ $# -eq 0 ]]; then
	power_cycle
else # pass an argument to enable retries
	POWER_CYCLE_RETRYCOUNT=0
    while [[ "$POWER_CYCLE_RETRYCOUNT" -lt 5 ]];do
		power_cycle
		sleep 3
        if timeout 2s python3 -m ectf25.tv.list /dev/ttyACM0 >/dev/null 2>&1; then
			exit 0
		fi

		((POWER_CYCLE_RETRYCOUNT++))
	done

	echo -e "%%FAILED%%\nReason: Power cycle timeout"
	exit 47
fi
