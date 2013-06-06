#!/usr/bin/env python

# This script posts items from your Reading List to your Pinboard account as
# bookmarks marked 'to read'. Learn about Pinboard at https://pinboard.in/tour/

from readinglistlib import ReadingListReader
import urllib

#
# Find your Pinboard API Token at https://pinboard.in/settings/password
# It will look something like apitoken = 'username:5CABE73682AAA9856010'
#
auth_token = '';
api_url = 'https://api.pinboard.in/v1/posts/add?'

rlr = ReadingListReader()
bookmarks = rlr.read()
for bookmark in bookmarks:
  params = urllib.urlencode({
			'url': bookmark['url'],
			'description': bookmark['title'],
			'extended': bookmark['preview'],
			'toread': 'yes',
			'auth_token': auth_token})
	urllib.urlopen(api_url + params)
	# validation of response result_code is left as an exercise for the reader
