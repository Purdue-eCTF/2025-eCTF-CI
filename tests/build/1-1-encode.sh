#!/bin/sh
timeout 5s python modified_tester.py --secrets ../test_out/global.secrets --stub-decoder json ../frames/x_c0.json || exit $?