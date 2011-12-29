#!/usr/bin/python

import sys
import urllib
import urlparse

import BeautifulSoup


def Get(url):
    f = urllib.urlopen(url)
    return f.getcode(), f.read()

def GetLinks(url, data):
    try:
        soup = BeautifulSoup.BeautifulSoup(data)
        for tag in soup.findAll('a'):
            href = tag.get('href')
            if href:
                yield urlparse.urljoin(url, href)
    except:
        pass

def GetLinksWithPrefix(prefix, url, data):
    for link in GetLinks(url, data):
        if link.startswith(prefix):
            link, _ = urlparse.urldefrag(link)
            yield link

def Scan(baseurl):
    toScan = [('', baseurl)]
    seen = set(baseurl)
    errors = {}
    
    while toScan:
        fromURL, url = toScan.pop()
        code, data = Get(url)
        print code, url
        if code != 200:
            errors[url] = (code, fromURL)
        for link in GetLinksWithPrefix(url, url, data):
            if link not in seen:
                seen.add(link)
                toScan.append((url, link))
    
    for url in errors.keys():
        code, fromURL = errors[url]
        print url, code, 'linked from', fromURL


if len(sys.argv) != 2:
    print >> sys.stderr, 'usage: %s <url>' % sys.argv[0]
    sys.exit(1)

url = sys.argv[1]
if not url.startswith('http://') and not url.startswith('https://'):
    url = 'http://' + url

Scan(url)

