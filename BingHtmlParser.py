try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

class BingHtmlParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.info_found = False 
        self.info = ""
        self.copyright_found = False
        self.copyright = ""
        self.image_url = ""
    
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for name, value in attrs:
                if name == 'class' and value == 'copyright':
                    self.copyright_found = True
        if tag == 'a':
            for name, value in attrs:
                if name == 'class' and value == 'title':
                    self.info_found = True

                if name == 'download' and value == 'BingWallpaper.jpg':
                    for name2, href in attrs:
                        if name2 == 'href':
                            self.image_url = href

    def handle_endtag(self, tag):
        if self.info_found:
            self.info_found = False
        if self.copyright_found:
            self.copyright_found = False

    def handle_data(self, data):
        if self.info_found:
            self.info = data
        if self.copyright_found:
            self.copyright = data


if __name__ == "__main__":
    # f = urlopen('https://www.bing.com/?mkt=zh-cn')
    f = urlopen('https://www.bing.com/?mkt=en-us')
    html = f.read()
  
    p = BingHtmlParser()
    p.feed(str(html))
    print(p.image_url)
    print(p.info)
    print(p.copyright)
    p.close()
