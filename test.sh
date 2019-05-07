#!/bin/sh

set -e
set -x

./setup.py build
coverage3 run --branch --source iotdev ./setup.py test
coverage3 report -m
