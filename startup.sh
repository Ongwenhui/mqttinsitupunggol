#!/bin/bash
echo "shell script for starting predictions"
nohup python3 runMQTT.py 127.17.0.1 3000 &
disown %1
echo "predictions started"
