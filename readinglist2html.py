#!/usr/bin/python

from readinglistlib import ReadingListReader

rlr = ReadingListReader()
bookmarks = rlr.read(ascending=False)

print '<!DOCTYPE html><html><head><title>Reading List</title></head><body><h1>Reading List</h1><ul>'

for bookmark in bookmarks:
	print '<li><p><a href="%(url)s">%(title)s</a><br />%(url)s</p><blockquote>%(preview)s</blockquote></li>' % {'url': bookmark['url'].encode('utf-8'), 'title': bookmark['title'].encode('utf-8'), 'preview': bookmark['preview'].encode('utf-8')}

print '</ul></body></html>'
