#!/bin/sh

REQUESTS=$1
ab -p test/example.json -c 30 -n $REQUESTS http://127.0.0.1:514/gelf
