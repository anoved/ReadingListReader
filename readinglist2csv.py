#!/usr/bin/env python
"""
Dumps the entire Safari Reading List into a CSV file for use in other ways. Kind of a master reset button."""

from readinglistlib import ReadingListReader
import csv


r = ReadingListReader()
articles = r.read()

with open('reading_list_dump.csv', 'wb') as csvfile:
    cwriter = csv.writer(csvfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL)
    fieldnames = ['title', 'url', 'added', 'viewed']
    hwriter = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
    hwriter.writeheader()
    for a in articles:
        try:
            w = {
                'title': a['title'],
                'url': a['url'],
                'added': a['added'],
                'viewed': a['viewed']
            }
            hwriter.writerow(w)
        except UnicodeEncodeError:
            print "Couldnt save %s" % a['url']
