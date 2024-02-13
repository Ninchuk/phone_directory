#!/bin/sh

set -e
set -x

pytest \
    --cov . \
    --cov-report xml \
    --no-cov-on-fail \
    --cov-branch \
    -x \
    -vv \
    tests

coverage report --skip-covered --show-missing
