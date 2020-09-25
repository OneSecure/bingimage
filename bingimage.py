#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
_ver = sys.version_info
py3_or_upper = (_ver[0] > 2)

#---------------------------------import---------------------------------------
if py3_or_upper:
    from urllib.parse import urlencode, quote_plus, parse_qsl, urlsplit, urlparse
    from urllib.request import Request, urlopen
    str = str
    basestring = (str, bytes)
    numeric_types = (int, float)
else:
    from urllib import urlencode, quote_plus
    from urlparse import parse_qsl, urlsplit, urlparse
    from urllib2 import Request, urlopen
    str = unicode
    basestring = basestring
    numeric_types = (int, long, float)

import re
import os
from io import BytesIO
from settings import *


#------------------------------------------------------------------------------
def postBingImageToWeibo(prefix, userUrl):
    _postBingImageToWebsite(prefix, userUrl, 'Weibo')

def _postBingImageToWebsite(prefix, userUrl, weibo):
    respHtml = getWebContents(userUrl)
    respHtml = str(respHtml, "utf-8")
    #print respHtml

    title = extractTitle(respHtml)
    if title == None:
        title = extractTitle2(respHtml)
    #print(u"title : %s" % title)

    imageUrl = extractImageUrl(respHtml)
    #print(u"imageUrl : %s" % imageUrl)

    imgData = None
    if imageUrl:
        parseResult = urlparse(imageUrl)
        if len(parseResult.netloc) == 0:
            parseResult = urlparse(userUrl)
            slash = u'/'
            if imageUrl[0] == u'/':
                slash = u''
            imageUrl = parseResult.scheme + '://' + parseResult.netloc + slash + imageUrl
        imgData = downloadImage(imageUrl)

    if imgData and title:
        # 给定图片存放名称
        #save_path = '/path/path'
        #fileName = save_path + "/ddd.jpg"
        #writeDataToFile(imgData, fileName)

        picFile = BytesIO(imgData)

        info = title + "\n" + prefix

        if weibo:
            from weibo_tiny import Client
            client = Client(APP_KEY, APP_SECRET, REDIRECT_URL, username=USERNAME, password=PASSWORD)
            client.post('statuses/upload', status=info, pic=picFile)
        else:
            maxTweetLen = 110
            if len(info) > maxTweetLen:
                info = info[0 : maxTweetLen]

            from tweetpost import postTweet
            postTweet(info, picFile)

def postBingImageToTwitter(prefix, userUrl):
    _postBingImageToWebsite(prefix, userUrl, None)

def getWebContents(targetUrl):
    req = Request(targetUrl)
    resp = urlopen(req)
    respHtml = resp.read()
    return respHtml

# id="sh_cp" class="sc_light" title="卡尔斯岛上的Kallur灯塔，法罗群岛 (© Janne Kahila/500px)"
def extractTitle(respHtml):
    titlePat = 'class="text" id="headline">'
    # http://www.regexlab.com/wild2regex
    # https://en.wikipedia.org/wiki/List_of_Unicode_characters
    # http://www.runoob.com/regexp/regexp-tutorial.html
    titlePatternEx = r'class\="text"\s+id\="headline">[^<]+<'
    result = re.search(titlePatternEx, respHtml)
    if result == None:
        titlePat = '<a id="sh_cp" class="sc_light" title="'
        titlePatternEx = r'<a\s+id\="sh_cp"\s+class\="sc_light"\s+title\="[^"]+"'
        result = re.search(titlePatternEx, respHtml)
    if result:
        result = result.group()
        result = result[ len(titlePat) : (len(result)-1) ]
    return result

# "copyright":"Kuha Karuhas pavilion in Phraya Nakhon Cave, Thailand (© Bule Sky Studio/Shutterstock)"
def extractTitle2(respHtml):
    titlePat = '"copyright":"'
    titlePatternEx = r'"copyright":"[^\"]+"'
    result = re.search(titlePatternEx, respHtml)
    if result:
        result = result.group()
        result = result[ len(titlePat) : (len(result)-1) ]
    return result

def extractImageUrl(respHtml):
    imageRE = r'<div\s+class\="img_cont"\s+style\="background\-image\:\s+url\([^\)]+\)'
    result = re.search(imageRE, respHtml)
    if result:
        result = result.group()

        flag = r'('
        begin = result.find(flag)

        if begin >= 0:
            flag2 = r')'
            end = result.find(flag2, begin+1)
            result = result[ (begin+1) : end ]
        else:
            result = ''
    else:
        imageRE = r'id\="bgLink"\s+rel\="preload"\s+href\="[^"]+"'
        result = re.search(imageRE, respHtml)
        if result:
            result = result.group()
            pat = 'id="bgLink" rel="preload" href="'
            begin = len(pat)
            if begin >= 0:
                flag2 = r'"'
                end = result.find(flag2, begin+1)
                result = result[ (begin+1) : end ]
            else:
                result = ''
    return result

def downloadImage(imageUrl):
    try:
        imgData = urlopen(imageUrl).read()
    except:
        imgData = None
        pass
    return imgData

def writeDataToFile(binData, localFile):
    f = open(localFile, 'wb+')
    if f:
        f.write(binData)
        f.close()

def getBingImage(userUrl):
    respHtml = getWebContents(userUrl)
    respHtml = str(respHtml, "utf-8")

    imageUrl = extractImageUrl(respHtml)

    imgData = None
    if imageUrl:
        parseResult = urlparse(imageUrl)
        if len(parseResult.netloc) == 0:
            parseResult = urlparse(userUrl)
            slash = u'/'
            if imageUrl[0] == u'/':
                slash = u''
            imageUrl = parseResult.scheme + '://' + parseResult.netloc + slash + imageUrl
        imgData = downloadImage(imageUrl)
    return imgData

###############################################################################
if __name__=="__main__":
    prefix = u"Today's pretty #wallpaper # #photo # on #Bing #."
    userUrl = BING_GLOBAL
    postBingImageToTwitter(prefix, userUrl)

    import time
    time.sleep(5)

    prefix = u'每日 #必应美图 # #壁纸 #。'
    userUrl = BING_CHINA
    postBingImageToTwitter(prefix, userUrl)
