# encoding: utf-8

from instapaperlib import Instapaper

__author__ = "Daniel Schauenberg"
__version__ = "0.4.0"
__license__ = "MIT"

def auth(user='', password=''):
    return Instapaper(user, password).auth()

def add_item(user='', password='', url=None,
             title=None, selection=None, jsonp=None,
             redirect=None, response_info=False):
    return Instapaper(user, password).add_item(url,title=title,
                                               selection=selection, jsonp=jsonp,
                                               redirect=redirect,
                                               response_info=response_info)
