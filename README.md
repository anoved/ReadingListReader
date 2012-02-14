Reading List Reader
===================

Safari Reading List "lets you save web pages to read or browse later." This script reads your Reading List and lists the articles bookmarked therein. It is offered as a proof of concept rather than a finished tool.  Safari's bookmarks file format is undocumented so reading it directly is totally unsupported and quite likely to fail in a variety of cases. That said, this script **does not** edit or modify your Safari bookmarks file in any way. No changes are made to the status of your Reading List.

This script is derived from [Safari-Reading-List-Recipe](https://github.com/anoved/Safari-Reading-List-Recipe). It's intended to facilitate experimental integration of Reading List with services like Instapaper or Pinboard. For example, you can [import](https://pinboard.in/settings/import/) the output of `readinglistreader.py --netscape` to add your unread articles to Pinboard.

Usage
-----

	usage: readinglistreader.py [-h] [--separator SEP] [--quote QUOTE]
								[--forcequotes] [--fields FIELD [FIELD ...]]
								[--header] [--timestamp FORMAT] [--netscape]
								[--show FILTER] [--sortfield FIELD]
								[--sortorder ORDER] [--output OUTPUT]
								[--input INPUT]
	
	This script outputs the contents of your Safari Reading List, a queue of
	temporary bookmarks representing articles you intend to read. By default, it
	prints the title and url of unread articles in chronological order, beginning
	with the oldest bookmark. Default output is compliant with CSV conventions.
	
	optional arguments:
	  -h, --help            show this help message and exit
	  --separator SEP       Separates field values. Specify 'tab' to use an actual
							tab character. Defaults to ','.
	  --quote QUOTE         Specify '' to suppress quoting. Defaults to '"'.
	  --forcequotes         Quote all field values. By default, only quote empty
							fields or values containing SEP, QUOTE, or newlines.
	  --fields FIELD [FIELD ...]
							Controls format of output record. Acceptable fields
							are title, url, preview, date, added, viewed, uuid,
							synckey, and syncserverid. Defaults to title and url.
							(Date is date article was originally bookmarked. If
							defined, added is date bookmark was synced via iCloud.
							If defined, viewed is date article was read.)
	  --header              Output a header record containing field labels.
	  --timestamp FORMAT    Controls format of date, added, and viewed fields.
							Understands strftime directives. Defaults to '%a %b %d
							%H:%M:%S %Y' (eg, 'Mon Feb 13 22:50:40 2012').
	  --netscape            Output items in Netscape bookmarks file format.
							Overrides preceding tabular output options.
	  --show FILTER         Control which items to output. Acceptable FILTER
							values are unread, read, or all. Defaults to unread.
	  --sortfield FIELD     Controls how output is sorted. Defaults to date.
	  --sortorder ORDER     May be ascending or descending. Defaults to ascending.
	  --output OUTPUT       Output file path. Defaults to stdout.
	  --input INPUT         Input file path. Assumed to be a Safari bookmarks file
							formatted as a binary property list. Defaults to
							~/Library/Safari/Bookmarks.plist
