CP = /bin/cp

SCRIPT             = Upload\ Reading\ List\ to\ Instapaper.scptd
SCRIPT_DIR         = $(SCRIPT)/Contents/Resources/Python

READINGLISTLIB_DIR = readinglistlib

# InstapaperLibrary is assumed to be installed in this directory.
# git clone git@github.com:mrtazz/InstapaperLibrary.git
INSTAPAPERLIB      = InstapaperLibrary
INSTAPAPERLIB_DIR  = $(INSTAPAPERLIB)/instapaperlib

.PHONY: script setup
	
# Copies current Python scripts and libraries into AppleScript bundle
script:
	$(CP) readinglist2instapaper.py $(SCRIPT_DIR)
	$(CP) -R $(READINGLISTLIB_DIR) $(SCRIPT_DIR)
	$(CP) -R $(INSTAPAPERLIB_DIR) $(SCRIPT_DIR)

# Grab a test copy of instapaperlib from the InstapaperLibrary repository
setup:
	$(CP) -R $(INSTAPAPERLIB_DIR) .
