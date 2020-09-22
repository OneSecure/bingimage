#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import webapp2

from google.appengine.ext import ndb
from google.appengine.api import mail
from datetime import datetime

from bingimage import postBingImageToWeibo
from bingimage import postBingImageToTwitter
from settings import *


class PostImageToSinaWeibo(webapp2.RequestHandler):
    def get(self):
        prefix = u"#Bing# #Wallpaper# #Photo#."
        userUrl = BING_GLOBAL
        postBingImageToWeibo(prefix, userUrl)

        import time
        time.sleep(5)

        prefix = u'每日 #必应美图# #壁纸#。'
        userUrl = BING_CHINA
        postBingImageToWeibo(prefix, userUrl)

class PostImageToTwitter(webapp2.RequestHandler):
    def get(self):
        prefix = u"#Bing #Wallpaper #Photo."
        userUrl = BING_GLOBAL
        postBingImageToTwitter(prefix, userUrl)

        import time
        time.sleep(60)

        prefix = u'每日 #必应美图 #壁纸。'
        userUrl = BING_CHINA
        postBingImageToTwitter(prefix, userUrl)



APP = webapp2.WSGIApplication(
        [
            ('/postimagetosinaweibo', PostImageToSinaWeibo),
            ('/postimagetotwitter', PostImageToTwitter)
        ])
