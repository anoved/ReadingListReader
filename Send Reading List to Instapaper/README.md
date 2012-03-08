# Send Reading List to Instapaper

This is a tool for Mac OS X 10.7 Lion to send your unread Reading List articles to [Instapaper](http://instapaper.com/). [Download the applet here.](https://github.com/anoved/ReadingListReader/raw/master/Send%20Reading%20List%20to%20Instapaper/Send%20Reading%20List%20to%20Instapaper.app.zip) (Alternatively, [download the script ](https://github.com/anoved/ReadingListReader/raw/master/Send%20Reading%20List%20to%20Instapaper/Send%20Reading%20List%20to%20Instapaper.scptd.zip), put it in `~/Library/Scripts`, and [run it](http://anoved.net/2007/09/script-runners/) however you prefer to run AppleScripts.)

When you first run it, you'll be prompted to enter your Instapaper email address or username:

![Setup username](https://github.com/anoved/ReadingListReader/raw/master/Send%20Reading%20List%20to%20Instapaper/Screenshots/setup_username.png)

Then you'll be prompted to enter your Instapaper password, if you have one; if not, leave it blank:

![Setup password](https://github.com/anoved/ReadingListReader/raw/master/Send%20Reading%20List%20to%20Instapaper/Screenshots/setup_password.png)

Your unread Reading List articles will be sent to Instapaper. They will not be marked as read or removed from your Reading List.

Next time you run the script, it will remember your Instapaper account and simply check whether you want to proceed.

![Send to Instapaper confirmation dialog](https://github.com/anoved/ReadingListReader/raw/master/Send%20Reading%20List%20to%20Instapaper/Screenshots/setup_confirm.png)

Click *Change Account* to enter a new or updated username and password.

---

This tool uses [readinglistlib](https://github.com/anoved/ReadingListReader) and [instapaperlib](https://github.com/mrtazz/InstapaperLibrary).
