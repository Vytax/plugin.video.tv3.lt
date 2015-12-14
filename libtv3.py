#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib
import urllib2
import sys
import operator

import simplejson as json

from StringIO import StringIO
import gzip

reload(sys) 
sys.setdefaultencoding('utf8')

SECTIONS_URL = 'http://staging.playapi.mtgx.tv/v3/sections?channel=3000,6501,6502,6503,6504&sections=%s&device=mobile&premium=open&page=%d'
CHANNELS_URL = 'http://staging.playapi.mtgx.tv/v3/formats?limit=500&channel=3000,6501,6502,6503,6504&device=mobile&premium=open'
SEARCH_URL = 'http://staging.playapi.mtgx.tv/v3/search?term=%s&country=lt&device=mobile&premium=open&page=%d'
FORMATVIDEOS_URL = 'http://staging.playapi.mtgx.tv/v3/videos?format=%s'

def getURL(url):
  
  request = urllib2.Request(url)
  request.add_header('Accept-encoding', 'gzip')
  response = urllib2.urlopen(request)
  if response.info().get('Content-Encoding') == 'gzip':
    buf = StringIO(response.read())
    f = gzip.GzipFile(fileobj=buf)
    return f.read()  
  
  return response.read()

def getJSON(url):

  data = getURL(url)  
  return json.loads(data)  

def getSection(section, page):

  return getJSON(SECTIONS_URL % (section, page))

def getFeatured(page=1):
  
  return getSection('videos.featured', page)

def getLatest(page=1):
  
  return getSection('videos.latest', page)

def getPopular(page=1):
  
  return getSection('videos.popular', page)

def getLatestClips(page=1):
  
  return getSection('videos.latest_clips', page)

def getCollections(page=1):
  
  return getSection('collections.featured', page)

def getChannels():
  
  data = getJSON(CHANNELS_URL)
  
  try:
    data['_embedded']['formats'].sort(key=operator.itemgetter('slug'))
  except:
    pass
  
  return data

def search(key, page=1):
  
  data = getJSON(SEARCH_URL % (urllib.quote_plus(key.strip()), page))
  
  if '_embedded' not in data:
    return data
  
  for f in data['_embedded']['formats']:
    f['_links']['videos'] = {'href': (FORMATVIDEOS_URL % f['id'])}    
  
  return data;
