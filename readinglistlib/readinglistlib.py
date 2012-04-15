import os
import subprocess
import plistlib
import datetime
from copy import deepcopy

class ReadingListReader:
	
	# input is path to a Safari bookmarks file; if None, use default file	
	def __init__(self, input=None):
		
		if None == input:
			input = os.path.expanduser('~/Library/Safari/Bookmarks.plist')
					
		# Read and parse the bookmarks file
		pipe = subprocess.Popen(('/usr/bin/plutil', '-convert', 'xml1', '-o', '-', input), shell=False, stdout=subprocess.PIPE).stdout
		xml = plistlib.readPlist(pipe)
		pipe.close()
		
		# Locate reading list section
		section = filter(lambda record: 'com.apple.ReadingList' == record.get('Title'), xml['Children'])
		reading_list = section[0].get('Children')
		if None == reading_list:
			reading_list = []
		
		# Assemble list of bookmark items
		self._articles = []
		for item in reading_list:
			
			# Use epoch time as a placeholder for undefined dates
			# (potentially facilitates sorting and filtering)
			added = item['ReadingList'].get('DateAdded')
			if None == added:
				added = datetime.datetime.min
			viewed = item['ReadingList'].get('DateLastViewed')
			if None == viewed:
				viewed = datetime.datetime.min
			
			self._articles.append({
					'title': item['URIDictionary']['title'],
					'url': item['URLString'],
					'preview': item['ReadingList'].get('PreviewText',''),
					'date': item['ReadingList']['DateLastFetched'],
					'added': added,
					'viewed': viewed,
					'uuid': item['WebBookmarkUUID'],
					'synckey': item['Sync'].get('Key'),
					'syncserverid': item['Sync'].get('ServerID')})
	
	# show specifies what articles to return: 'unread' or 'read'; if None, all.
	# sortfield is one of the _articles dictionary keys
	# ascending determines sort order; if false, sort is descending order
	# dateformat is used to format dates; if None, datetime objects are returned
	def read(self, show='unread', sortfield='date', ascending=True, dateformat=None):
		
		# Filter, sort, and return a fresh copy of the internal article list
		articles = deepcopy(self._articles)
		
		# Filter article list to show only unread or read articles, if requested		
		if 'unread' == show:
			articles = filter(lambda record: datetime.datetime.min == record['viewed'], articles)
		elif 'read' == show:
			articles = filter(lambda record: datetime.datetime.min != record['viewed'], articles)
		else:
			pass
		
		# Sort articles.
		articles = sorted(articles, key=lambda record: record[sortfield])
		if not ascending:
			articles.reverse()
		
		# Replace any datetime.min sort/filter placeholders with None
		articles = map(self.resetUndefinedDates, articles)
		
		# If a date format (such as '%a %b %d %H:%M:%S %Y') is specified,
		# convert all defined dates to that format and undefined dates to ''.
		if None != dateformat:
			articles = map(self.formatDates, articles, [dateformat for i in range(len(articles))])
					
		return articles
	
	def resetUndefinedDates(self, article):
		if datetime.datetime.min == article['viewed']:
			article['viewed'] = None
		if datetime.datetime.min == article['added']:
			article['added'] = None	
		return article
	
	def formatDates(self, article, dateformat):
		if None != article['viewed']:
			article['viewed'] = article['viewed'].strftime(dateformat)
		else:
			article['viewed'] = ''
		if None != article['added']:
			article['added'] = article['added'].strftime(dateformat)
		else:
			article['added'] = ''
		article['date'] = article['date'].strftime(dateformat)
		return article

