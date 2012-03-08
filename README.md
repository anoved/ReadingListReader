# readinglistlib

This Python module provides a very simple interface to read the contents of your Safari Reading List. Here is a simple usage example:

	from readinglistlib import ReadingListReader
	rlr = ReadingListReader()
	rl = rlr.read()

The output of `rlr.read()` is a list of articles. Each article is a dictionary with the following keys: `title`, `url`, `preview`, `date` (creation date of bookmark), `added` (sync date; may be undefined), `viewed` (read date; undefined for unread articles), `uuid`, `synckey`, and `syncserverid`.

If you provide a path as an argument to the `ReadingListReader` constructor, an attempt will be made to load the Reading List from that file. By default, your Reading List is read from `~/Library/Safari/Bookmarks.plist`.

The `read()` method has a few optional arguments that can be used to control its output:

- `show` can be set to `'unread'` or `'read'` to return only unread or read items, respectively. Any other value (such as `None`) will cause all items to be returned. Defaults to `'unread'`. 
- `sortfield` can be set to any of the keys listed above. The default is `date`. 
- `ascending` controls sort order of the returned list. The default is `True`; set to `False` for descending sort.
- `dateformat` controls the formatting of the `date`, `added`, and `viewed` fields. Defaults to `None`, in which case datetime objects are returned instead of strings. Understands [strftime format directives](http://docs.python.org/library/datetime.html?highlight=strftime#strftime-strptime-behavior).

Your Reading List is read once by the `ReadingListReader` constructor. Subsequent calls to the `read()` method do not reload the Reading List, but can be called with different options to return different subsets of the same list.

---

# Send Reading List to Instapaper

This is a script that you can use to send your unread Reading List articles to [Instapaper](http://instapaper.com/). [Download the script](https://github.com/anoved/ReadingListReader/raw/master/Send%20Reading%20List%20to%20Instapaper/Send%20Reading%20List%20to%20Instapaper.scptd.zip), unzip it, and put it in your `~/Library/Scripts` folder so you can [run it](http://anoved.net/2007/09/script-runners/).

When you first run it, you'll be prompted to enter your Instapaper email address or username:

![Setup username](https://github.com/anoved/ReadingListReader/raw/master/Send%20Reading%20List%20to%20Instapaper/Screenshots/setup_username.png)

Then you'll be prompted to enter your Instapaper password, if you have one; if not, leave it blank:

![Setup password](https://github.com/anoved/ReadingListReader/raw/master/Send%20Reading%20List%20to%20Instapaper/Screenshots/setup_password.png)

Your unread Reading List articles will be sent to Instapaper. They will not be marked as read or removed from your Reading List.

Next time you run the script, it will remember your Instapaper account and simply check whether you want to proceed.

![Send to Instapaper confirmation dialog](https://github.com/anoved/ReadingListReader/raw/master/Send%20Reading%20List%20to%20Instapaper/Screenshots/setup_confirm.png)

Click *Change Account* to enter a new or updated username and password.

---

# Python Scripts

Two scripts based on `readinglistlib` are provided as examples. `readinglistreader.py` dumps your Reading List in tabular or "bookmarks" format. `readinglist2instapaper.py` adds your unread Reading List items to your Instapaper queue. Details below.

## readinglistreader.py

Safari Reading List "lets you save web pages to read or browse later." This script reads your Reading List and lists the articles bookmarked therein. It is offered as a proof of concept rather than a finished tool.  Safari's bookmarks file format is undocumented so reading it directly is totally unsupported and quite likely to fail in a variety of cases. That said, this script **does not** edit or modify your Safari bookmarks file in any way. No changes are made to the status of your Reading List.

This script is derived from [Safari-Reading-List-Recipe](https://github.com/anoved/Safari-Reading-List-Recipe). It's intended to facilitate experimental integration of Reading List with services like Instapaper or Pinboard. For example, you can [import](https://pinboard.in/settings/import/) the output of `readinglistreader.py --bookmarks` to add your unread articles to Pinboard.

### Requirements

This script is for Mac OS X 10.7 ("Lion"). It relies on libraries introduced with Python 2.7, which is not included with "Snow Leopard" or earlier versions of Mac OS X.

### Usage

	usage: readinglistreader.py [-h] [--separator SEP] [--quote QUOTE]
								[--forcequotes] [--fields FIELD [FIELD ...]]
								[--header] [--timestamp FORMAT] [--bookmarks]
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
	  --bookmarks           Output items in Netscape bookmarks file format.
							Overrides preceding tabular output options.
	  --show FILTER         Control which items to output. Acceptable FILTER
							values are unread, read, or all. Defaults to unread.
	  --sortfield FIELD     Controls how output is sorted. Defaults to date.
	  --sortorder ORDER     May be ascending or descending. Defaults to ascending.
	  --output OUTPUT       Output file path. Defaults to stdout.
	  --input INPUT         Input file path. Assumed to be a Safari bookmarks file
							formatted as a binary property list. Defaults to
							~/Library/Safari/Bookmarks.plist

### Installation

Make it executable with `chown +x readinglistreader.py` and put it in your `/usr/local/bin` if you want. Make sure you have installed `readinglistlib` somewhere in your [sys.path](http://docs.python.org/tutorial/modules.html#the-module-search-path).

### Examples

With no options, a list of your unread bookmarks is displayed in `title,url` format:

	readinglistreader.py

Use the `--fields` option to specify the "schema" of your output table:

	readinglistreader.py --fields title preview date url

By default, output is sorted by `date`, starting with the oldest bookmark. To sort alphabetically by article `title`:

	readinglistreader.py --sortfield title
	
As an alternative to outputting a table, you can save a [bookmarks file][netscape bookmarks spec]:

[netscape bookmarks spec]: http://msdn.microsoft.com/en-us/library/ie/aa753582(v=vs.85).aspx

	readinglistreader.py --bookmarks --output bookmarks.html

Note that `--bookmarks` mode ignores tabular output options such as `--fields`. However, your `--show`, `--sortfield`, and `--sortorder` settings are reflected in the bookmarks output.

## readinglist2instapaper.py

This script uses `readinglistreader.py` and Daniel Schauenberg's [InstapaperLibrary](https://github.com/mrtazz/InstapaperLibrary) to add your unread Reading List articles to your [Instapaper](http://www.instapaper.com/) account. Specify your Instapaper account with the `--username` and `--password` arguments, or create a file named `~/.instapaperrc` containing a line with your credentials formatted as `username:password`. Articles are not removed from your Reading List as they are added to Instapaper. This script is provided as example.

(InstapaperLibrary is not included with this script; install it via any of the methods advised at its GitHub page, or simply put the `instapaperlib` package folder in the same folder as `readinglist2instapaper.py`.)

---

# Wishlist

- Allow deletion and/or mark-as-read of Reading List items. Naïvely overwriting `~/Library/Safari/Bookmarks.plist` with a modified plist accomplishes this, albeit without propagating changes to synced browsers/devices. Alternatively, use GUI scripting to remove items auto-manually (more compatible, but likely more visually distracting).
