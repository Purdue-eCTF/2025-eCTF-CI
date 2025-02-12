#!/bin/bash

timeout 120s python -m ectf25.utils.stress_test --test-size 100000 encode ../test_out/global.secrets || exit $?