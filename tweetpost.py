#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
_ver = sys.version_info
py3_or_upper = (_ver[0] > 2)


from settings import *

def postTweet(text, image):
    if py3_or_upper:
        postTweet_py3(text, image)
    else:
        postTweet_py2(text, image)

def postTweet_py3(text, image):
    from twython import Twython, TwythonError

    twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)

    try:
        if image:
            twitter.update_status_with_media(status=text, media=image)
        else :
            twitter.update_status(status=text)
    except TwythonError as e:
        print(e)


def postTweet_py2(text, image):
	import tweetpony
	api = tweetpony.API(consumer_key = consumer_key, consumer_secret = consumer_secret, access_token = access_token, access_token_secret = access_token_secret)
	user = api.user
	try:
		if image:
			api.update_status_with_single_media(status = text, media=image)
		else :
			api.update_status(status = text)
	except tweetpony.APIError as err:
		print("Oops, something went wrong! Twitter returned error #%i and said: %s" % (err.code, err.description))
	else:
		pass #print "Yay! Your tweet has been sent!"
