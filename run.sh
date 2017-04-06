#!/bin/sh
forever start -c python3 src/slack_watcher.py
forever start -c python3 src/twitter_watcher.py TWITTER_ID_HERE
