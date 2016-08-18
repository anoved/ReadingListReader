#!/usr/bin/env python

# Requires https://github.com/samuelkordik/pocketlib

from readinglistlib import ReadingListReader
from pocket.pocket import Pocket


import argparse
import sys

# Configure and consume command line arguments.
ap = argparse.ArgumentParser(description='This script adds your Safari Reading List articles to Pocket.')
ap.add_argument('-v', '--verbose', action='store_true', help='Print article URLs as they are added.')
args = ap.parse_args()

consumer_key = "" # Insert your consumer key here (https://getpocket.com/developer/apps/)
redirect_uri = "" # TODO: Currently obselete/phishing threat in this version 

# Manually trigger pocket authentication
access_token = Pocket.auth(consumer_key=consumer_key, redirect_uri=redirect_uri)
pocket_instance = Pocket(consumer_key, access_token)

# Get the Reading List items
rlr = ReadingListReader()
articles = rlr.read(show="unread")

for article in articles:
    print pocket_instance.bulk_add(url=article['url'].encode('utf-8'), tags='reading_list')
    print "Added:", article['url']

# commit bulk_add changes
pocket_instance.commit()
