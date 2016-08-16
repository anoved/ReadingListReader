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

consumer_key = ""
redirect_uri = ""

# Initialize Pocket API
request_token = Pocket.get_request_token(consumer_key=consumer_key, redirect_uri=redirect_uri)
auth_url = Pocket.get_auth_url(code=request_token, redirect_uri=redirect_uri)
user_credentials = Pocket.get_credentials(consumer_key=consumer_key, code=request_token)
access_token = user_credentials['access_token']

# Get the Reading List items
rlr = ReadingListReader()
articles = rlr.read(show="unread")

for article in articles:
    (add_status, add_message) = Pocket.add(article['url'].encode('utf-8'), title=article['title'].encode('utf-8'), tags='reading_list')
    if 200 == add_status:
        if args.verbose:
            print article['url'].encode('utf-8')
    else:
        print >> sys.stderr, add_message
        ap.exit(-1)
