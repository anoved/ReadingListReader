#!/usr/bin/env python

# Requires https://github.com/mrtazz/InstapaperLibrary
from instapaperlib import Instapaper

from readinglistlib import ReadingListReader

# Standard library modules
import argparse
import sys
import os
import re

# Configure and consume command line arguments.
ap = argparse.ArgumentParser(description='This script adds your Safari Reading List articles to Instapaper.')
ap.add_argument('-u', '--username', action='store', default='', help='Instapaper username or email.')
ap.add_argument('-p', '--password', action='store', default='', help='Instapaper password (if any).')
ap.add_argument('-v', '--verbose', action='store_true', help='Print article URLs as they are added.')
args = ap.parse_args()

if '' == args.username:
	# For compatibility with instapaperlib's instapaper.py tool,
	# attempt to read Instapaper username and password from ~/.instapaperrc.
	# (Login pattern modified to accept blank passwords.)
	login = re.compile("(.+?):(.*)")
	try:
		config = open(os.path.expanduser('~') + '/.instapaperrc')
		for line in config:
			matches = login.match(line)
			if matches:
				args.username = matches.group(1).strip()
				args.password = matches.group(2).strip()
				break
		if '' == args.username:
			print >> sys.stderr, 'No username:password line found in ~/.instapaperrc'
			ap.exit(-1)
	except IOError:
		ap.error('Please specify a username with -u/--username.')

# Log in to the Instapaper API.
instapaper = Instapaper(args.username, args.password)
(auth_status, auth_message) = instapaper.auth()

# 200: OK
# 403: Invalid username or password.
# 500: The service encountered an error.
if 200 != auth_status:
	print >> sys.stderr, auth_message
	ap.exit(-1)

# Get the Reading List items
rlr = ReadingListReader()
articles = rlr.read(show='unread')

for article in articles:

	(add_status, add_message) = instapaper.add_item(article['url'].encode('utf-8'), title=article['title'].encode('utf-8'))
	
	# 201: Added
	# 400: Rejected (malformed request or exceeded rate limit; probably missing a parameter)
	# 403: Invalid username or password; in most cases probably should have been caught above.
	# 500: The service encountered an error.
	if 201 == add_status:
		if args.verbose:
			print article['url'].encode('utf-8')
	else:
		print >> sys.stderr, add_message
		ap.exit(-1)
