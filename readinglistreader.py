#!/usr/bin/env python

import os
import sys
import shlex
import argparse
import datetime
import subprocess
import plistlib

# Configure CLI
fields = ['title', 'url', 'preview', 'date', 'added', 'viewed', 'uuid', 'synckey', 'syncserverid']
ap = argparse.ArgumentParser(description='This script outputs the contents of your Safari Reading List, a queue of temporary bookmarks representing articles you intend to read. By default, it prints the title and url of unread articles in chronological order, beginning with the oldest bookmark. Default output is compliant with CSV conventions.')
ap.add_argument('--separator', action='store', default=',', metavar='SEP', help='Separates field values. Specify \'tab\' to use an actual tab character. Defaults to \',\'.')
ap.add_argument('--quote', action='store', default='"', help='Specify \'\' to suppress quoting. Defaults to \'"\'.')
ap.add_argument('--forcequotes', action='store_true', default=False, help="Quote all field values. By default, only quote empty fields or values containing SEP, QUOTE, or newlines.")
ap.add_argument('--fields', action='store', nargs='+', default=['title', 'url'], choices=fields, metavar='FIELD', help='Controls format of output record. Acceptable fields are title, url, preview, date, added, viewed, uuid, synckey, and syncserverid. Defaults to title and url. (Date is date article was originally bookmarked. If defined, added is date  bookmark was synced via iCloud. If defined, viewed is date article was read.)')
ap.add_argument('--header', action='store_true', default=False, help='Output a header record containing field labels.')
ap.add_argument('--timestamp', action='store', default='%a %b %d %H:%M:%S %Y', metavar='FORMAT', help='Controls format of date, added, and viewed fields. Understands strftime directives. Defaults to \'%%a %%b %%d %%H:%%M:%%S %%Y\' (eg, \'' + datetime.datetime.now().strftime('%a %b %d %H:%M:%S %Y') + '\').')
ap.add_argument('--bookmarks', action='store_true', default=False, help='Output items in Netscape bookmarks file format. Overrides preceding tabular output options.')
ap.add_argument('--show', action='store', default='unread', choices=['unread', 'read', 'all'], metavar='FILTER', help='Control which items to output. Acceptable FILTER values are unread, read, or all. Defaults to unread.')
ap.add_argument('--sortfield', action='store', default='date', choices=fields, metavar='FIELD', help="Controls how output is sorted. Defaults to date.")
ap.add_argument('--sortorder', action='store', default='ascending', choices=['ascending', 'descending'], metavar='ORDER', help='May be ascending or descending. Defaults to ascending.')
ap.add_argument('--output', action='store', type=argparse.FileType('w'), default='-', help='Output file path. Defaults to stdout.')
ap.add_argument('--input', action='store', default=os.path.expanduser('~/Library/Safari/Bookmarks.plist'), help='Input file path. Assumed to be a Safari bookmarks file formatted as a binary property list. Defaults to ~/Library/Safari/Bookmarks.plist')
args = ap.parse_args()

# Reinterpretation of fiddly options
if 'tab' == args.separator:
	args.separator = '\t'

# Input
if not os.path.exists(args.input):
	raise SystemExit, "The input file does not exist: %s" % args.input
cmd = shlex.split('/usr/bin/plutil -convert xml1 -o - %s' % args.input)
input_pipe = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE).stdout
try:
	xml_plist = plistlib.readPlist(input_pipe)
except:
	raise SystemExit, "An error occured while attempting to parse the input. (%s)" % sys.exc_info()[1]
input_pipe.close()

# Locate reading list
rl_section = filter(lambda record: 'com.apple.ReadingList' == record.get('Title'), xml_plist['Children'])
reading_list = rl_section[0].get('Children')
if reading_list == None:
	reading_list = []

# assemble our own list of reading list items
bookmarks = []
for item in reading_list:
	
	# date added (via iCloud) and date viewed (read) may not be defined.
	# we use a long-ago time as undef placeholder to facilitate sorting, etc.
	added = item['ReadingList'].get('DateAdded')
	if None == added:
		added = datetime.datetime.min
	viewed = item['ReadingList'].get('DateLastViewed')
	if None == viewed:
		viewed = datetime.datetime.min

	bookmarks.append({
			'title': item['URIDictionary']['title'],
			'url': item['URLString'],
			'preview': item['ReadingList']['PreviewText'],
			'date': item['ReadingList']['DateLastFetched'],
			'added': added,
			'viewed': viewed,
			'uuid': item['WebBookmarkUUID'],
			'synckey': item['Sync'].get('Key'),
			'syncserverid': item['Sync'].get('ServerID')})

# Apply filtration (test LastViewedDate to determine unread status).
if 'unread' == args.show:
	bookmarks = filter(lambda record: datetime.datetime.min == record['viewed'], bookmarks)
elif 'read' == args.show:
	bookmarks = filter(lambda record: datetime.datetime.min != record['viewed'], bookmarks)

# Apply sortation
bookmarks = sorted(bookmarks, key=lambda record: record[args.sortfield])
if 'descending' == args.sortorder:
	bookmarks.reverse()

if args.bookmarks:

	# Netscape Bookmarks File formatted output
	# eg http://msdn.microsoft.com/en-us/library/ie/aa753582(v=vs.85).aspx
	
	print >> args.output, '<!DOCTYPE NETSCAPE-Bookmark-file-1>\n<HTML>\n<META HTTP-EQUIV="CONTENT-TYPE" CONTENT="text/html; charset=UTF-8">\n<Title>Bookmarks</Title>\n<H1>Bookmarks</H1>\n<DT><H3 FOLDED>Reading List Bookmarks</H3>\n<DL>'
	for bookmark in bookmarks:
		print >> args.output, '	<DT><A HREF="%s">%s</A>' % (bookmark['url'].encode('utf-8'), bookmark['title'].encode('utf-8'))
	print >> args.output, '</DL>\n</HTML>'

else:
	
	# CSV or custom tabular formatted output
	
	# Accepts a value. Tests if it should be quoted and, if so, returns quoted
	# value with any quote characters escaped via duplication.
	# Quoting rules derived from:
	# https://tools.ietf.org/html/rfc4180
	# http://www.creativyst.com/Doc/Articles/CSV/CSV01.htm
	def quotify(value):
		if (args.forcequotes or '' == value or -1 != value.find(args.separator) or -1 != value.find(args.quote) or -1 != value.find('\n')) and '' != args.quote:
			return '%s%s%s' % (args.quote, value.replace(args.quote, '%s%s' % (args.quote, args.quote)), args.quote)
		else:
			return value
	
	# Accepts a list of values. Prints record with separators and, if required, quotes.
	def output_record(values):
		print >> args.output, args.separator.join(map(quotify, values))
	
	# Header record
	if True == args.header:
		output_record(args.fields)
	
	for bookmark in bookmarks:
		field_values = []
		
		for field in args.fields:
			field_value = bookmark[field]
			
			# Convert timestamps, if defined, to printable strings.
			if 'date' == field or 'added' == field or 'viewed' == field:
				if datetime.datetime.min == field_value:
					field_value = ''
				else:
					field_value = field_value.strftime(args.timestamp)
			
			field_values.append(field_value.encode('utf-8'))
					
		output_record(field_values)
	
