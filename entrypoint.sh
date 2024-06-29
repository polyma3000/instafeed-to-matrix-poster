#!/bin/sh

while true; do
    python app.py &
    sleep $SLEEP_TIME_SECONDS
done
