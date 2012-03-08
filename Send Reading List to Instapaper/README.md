# Send Reading List to Instapaper

This is a tool for Mac OS X 10.7 Lion to send your unread Reading List articles to [Instapaper](http://instapaper.com/). [Download the applet here.](https://github.com/anoved/ReadingListReader/raw/master/Send%20Reading%20List%20to%20Instapaper/Send%20Reading%20List%20to%20Instapaper.app.zip) (Alternatively, [download the script ](https://github.com/anoved/ReadingListReader/raw/master/Send%20Reading%20List%20to%20Instapaper/Send%20Reading%20List%20to%20Instapaper.scptd.zip), put it in `~/Library/Scripts`, and [run it](http://anoved.net/2007/09/script-runners/) however you prefer to run AppleScripts.)

When you first run it, you'll be prompted to enter your Instapaper email address or username:

![Setup username](https://github.com/anoved/ReadingListReader/raw/master/Send%20Reading%20List%20to%20Instapaper/Screenshots/setup_username.png)

Then you'll be prompted to enter your Instapaper password, if you have one; if not, leave it blank:

![Setup password](https://github.com/anoved/ReadingListReader/raw/master/Send%20Reading%20List%20to%20Instapaper/Screenshots/setup_password.png)

Your unread Reading List articles will be sent to Instapaper. Articles are not automatically marked as read or removed from your Reading List. (This may limit the utility of this script as a way to "sync" Instapaper and Reading List. It is perhaps more useful as an occasional way to transfer a large number of accumulated Reading List bookmarks to Instapaper.)

Next time you run the script, it will remember your Instapaper account and simply check whether you want to proceed.

![Send to Instapaper confirmation dialog](https://github.com/anoved/ReadingListReader/raw/master/Send%20Reading%20List%20to%20Instapaper/Screenshots/setup_confirm.png)

Click *Change Account* to enter a new or updated username and password.

---

This tool uses [readinglistlib](https://github.com/anoved/ReadingListReader) and [instapaperlib](https://github.com/mrtazz/InstapaperLibrary).

---

## An Alternative

So here you are, surfing GitHub and downloading scripts. You look like the roll-your-own type. Instead of sending your Reading List articles to Instapaper, why not send them straight to your Kindle (or other ereader) with [Calibre](http://www.calibre-ebook.com/) and [my ebook recipe for Reading List](https://github.com/anoved/Safari-Reading-List-Recipe)? [Here's a blog post with more details](http://anoved.net/2012/02/ebook-recipe-for-safari-reading-list/), including screenshots and a step-by-step setup guide.
