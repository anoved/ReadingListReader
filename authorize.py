#!/usr/bin/env python

import httplib2
import ConfigParser
import webbrowser

consumer_key = '16577-c5e0b5443c4c6bd5a873a2b9'

request_token_url = 'https://getpocket.com/v3/oauth/request'
authorize_url = 'https://getpocket.com/auth/authorize'
redirect_url = 'localhost'
access_token_url = 'https://getpocket.com/v3/oauth/authorize'

# Obtain request token
body = "consumer_key=%s&redirect_uri=%s" % (consumer_key, redirect_url)
h = httplib2.Http()
headers = {}
headers['Content-Type'] = 'application/x-www-form-urlencoded'
resp, content = h.request(request_token_url, method="POST", body=body, headers=headers)
if resp['status'] != '200':
    print resp.reason
request_token = content.split("=")

# Redirect to provider
print "Go to the following link in your browser:"
print "%s?request_token=%s&redirect_uri=%s" % (authorize_url, request_token[1], redirect_url)
print
webbrowser.open("%s?request_token=%s&redirect_uri=%s" % (authorize_url, request_token[1], redirect_url))

accepted = 'n'
while accepted.lower() == 'n':
    accepted = raw_input('Have you authorized me? (y/n) ')

# Obtain access token
body = "consumer_key=%s&code=%s" % (consumer_key, request_token[1])
h = httplib2.Http()
headers = {}
headers['Content-Type'] = 'application/x-www-form-urlencoded'
resp, content = h.request(access_token_url, method="POST", body=body, headers=headers)
if resp['status'] != '200':
    raise Exception('Bad request. Are you sure you authorized?')
content_final = content.split("&")
access_token = content_final[0].split("=")
username = content_final[1].split("=")
print "You've been authorized successfully."
print "Username: %s" % username[1]
print "You should copy this access token and then add it to config.py"
print "Your access token: %s" % access_token[1]

config = ConfigParser.ConfigParser()
config.add_section('POCKET_API')
config.set('POCKET_API', 'username', username[1])
config.set('POCKET_API', 'access_token', access_token[1])
with open('config.ini', 'w') as configfile:
    config.write(configfile)
