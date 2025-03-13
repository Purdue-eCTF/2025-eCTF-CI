#!/bin/bash
USB_RETRY_COUNT=0
/usr/sbin/uhubctl -l 1-1 -a cycle > /dev/null 2>/dev/null

echo -n "Waiting for USB to connect"
while [ ! -e "/dev/disk/by-label/DAPLINK" ]; do
  if [ "$USB_RETRY_COUNT" -gt  20 ]; then
    echo -e "%%FAILED%%\nReason: USB connection timeout"
    exit 47
  fi
  echo -n "."
  sleep 1
  ((USB_RETRY_COUNT++))
done
echo
sleep 5