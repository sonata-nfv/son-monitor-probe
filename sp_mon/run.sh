#!/bin/bash

python /opt/Monitoring/main.py &
tail -f /dev/null
