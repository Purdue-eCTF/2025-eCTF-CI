
timeout 0.5s python -m ectf25.tv.list /dev/ttyACM0

if [ "$?" -ne 0 ]; then
  exit 1
fi