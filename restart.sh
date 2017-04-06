#!/bin/sh
forever stopall
python3 tool/log.py "restart"
sh run.sh
