#!/usr/bin/env python

# Requires https://github.com/samuelkordik/pocketlib

from readinglistlib import ReadingListReader
from pocketlib import Pocket


import argparse
import sys

# Configure and consume command line arguments.
ap = argparse.ArgumentParser(description='This script adds your Safari Reading List articles to Pocket.')
ap.add_argument('-v', '--verbose', action='store_true', help='Print article URLs as they are added.')
args = ap.parse_args()

# Initialize Pocket API
pocket = Pocket()

if pocket.is_authed() is False:
    print 'You need to authorize this script through Pocket before using it'
    print 'Follow these steps:'
    pocket.auth()

# Get the Reading List items
rlr = ReadingListReader()
articles = rlr.read(show="unread")

for article in articles:
    (add_status, add_message) = pocket.add_item(article['url'].encode('utf-8'), title=article['title'].encode('utf-8'), tags='reading_list')
    if 200 == add_status:
        if args.verbose:
            print article['url'].encode('utf-8')
    else:
        print >> sys.stderr, add_message
        ap.exit(-1)
