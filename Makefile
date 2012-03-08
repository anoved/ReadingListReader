CP  = /bin/cp
ZIP = /usr/bin/zip

SCRIPT             = Send\ Reading\ List\ to\ Instapaper/Send\ Reading\ List\ to\ Instapaper.scptd
SCRIPT_DIR         = $(SCRIPT)/Contents/Resources/Python
SCRIPT_ZIP         = $(SCRIPT).zip
SCRIPT_APP         = Send\ Reading\ List\ to\ Instapaper/Send\ Reading\ List\ to\ Instapaper.app
SCRIPT_APP_DIR     = $(SCRIPT_APP)/Contents/Resources/Python
SCRIPT_APP_ZIP     = Send\ Reading\ List\ to\ Instapaper/Send\ Reading\ List\ to\ Instapaper.app.zip

READINGLISTLIB_DIR = readinglistlib

# InstapaperLibrary is assumed to be installed in this directory.
# git clone git@github.com:mrtazz/InstapaperLibrary.git
INSTAPAPERLIB      = InstapaperLibrary
INSTAPAPERLIB_DIR  = $(INSTAPAPERLIB)/instapaperlib

.PHONY: dist script script_app setup
	
# Make a distributable zip file of the AppleScript
dist: script script_app
	$(ZIP) -r $(SCRIPT_ZIP) $(SCRIPT)
	$(ZIP) -r $(SCRIPT_APP_ZIP) $(SCRIPT_APP)

# Copies current Python scripts and libraries into AppleScript bundle
script:
	$(CP) readinglist2instapaper.py $(SCRIPT_DIR)
	$(CP) -R $(READINGLISTLIB_DIR) $(SCRIPT_DIR)
	$(CP) -R $(INSTAPAPERLIB_DIR) $(SCRIPT_DIR)

# Copies current Python scripts and libraries into AppleScript app bundle;
# also copies the AppleScript from the script bundle into the app bundle.
script_app:
	$(CP) readinglist2instapaper.py $(SCRIPT_APP_DIR)
	$(CP) -R $(READINGLISTLIB_DIR) $(SCRIPT_APP_DIR)
	$(CP) -R $(INSTAPAPERLIB_DIR) $(SCRIPT_APP_DIR)
	$(CP) $(SCRIPT)/Contents/Resources/Scripts/main.scpt $(SCRIPT_APP)/Contents/Resources/Scripts

# Grab a test copy of instapaperlib from the InstapaperLibrary repository
setup:
	$(CP) -R $(INSTAPAPERLIB_DIR) .
