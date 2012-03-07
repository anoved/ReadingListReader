#!/usr/bin/env python

# Requires https://github.com/mrtazz/InstapaperLibrary
from instapaperlib import Instapaper

# Standard library modules
import argparse
import subprocess
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

# Get the Reading List article URLs.
# Assumes readinglistreader.py is in the current directory; if not,
# modify Popen args to specify the correct path.
try:
	reading_list_pipe = subprocess.Popen(('/usr/bin/env', 'python', 'readinglistreader.py', '--fields', 'url', '--forcequotes'), shell=False, stdout=subprocess.PIPE).stdout
except OSError:
	print >> sys.stderr, 'Could not read Reading List. (%s)' % sys.exc_info()[1]
	ap.exit(-1)

# Add each Reading List article URL to Instapaper.
for article_url in reading_list_pipe:
	article_url = article_url.rstrip('\n').strip('"')
	(add_status, add_message) = instapaper.add_item(article_url)
	
	# 201: Added
	# 400: Rejected (malformed request or exceeded rate limit; probably missing a parameter)
	# 403: Invalid username or password; in most cases probably should have been caught above.
	# 500: The service encountered an error.
	if 201 == add_status:
		if args.verbose:
			print article_url
	else:
		print >> sys.stderr, add_message
		reading_list_pipe.close()
		ap.exit(-1)

reading_list_pipe.close()
