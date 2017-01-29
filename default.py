#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import urllib

import xbmcgui
import xbmcplugin
import xbmcaddon

import libtv3 as tv3

settings = xbmcaddon.Addon(id='plugin.video.tv3.lt')

def getParameters(parameterString):
  commands = {}
  splitCommands = parameterString[parameterString.find('?') + 1:].split('&')
  for command in splitCommands:
    if (len(command) > 0):
      splitCommand = command.split('=')
      key = splitCommand[0]
      value = splitCommand[1]
      commands[key] = value
  return commands

def build_main_directory(): 
  
  listitem = xbmcgui.ListItem("Aktualu")
  listitem.setProperty('IsPlayable', 'false')
  xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + '?mode=1&page=1', listitem = listitem, isFolder = True, totalItems = 0)
  
  listitem = xbmcgui.ListItem("Naujausi")
  listitem.setProperty('IsPlayable', 'false')
  xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + '?mode=2&page=1', listitem = listitem, isFolder = True, totalItems = 0)
  
  listitem = xbmcgui.ListItem("Žiūrimiausi")
  listitem.setProperty('IsPlayable', 'false')
  xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + '?mode=3&page=1', listitem = listitem, isFolder = True, totalItems = 0)
  
  listitem = xbmcgui.ListItem("Rinkiniai")
  listitem.setProperty('IsPlayable', 'false')
  xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + '?mode=4&page=1', listitem = listitem, isFolder = True, totalItems = 0)
  
  listitem = xbmcgui.ListItem("Naujausi klipai")
  listitem.setProperty('IsPlayable', 'false')
  xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + '?mode=5&page=1', listitem = listitem, isFolder = True, totalItems = 0)
  
  listitem = xbmcgui.ListItem("Laidos")
  listitem.setProperty('IsPlayable', 'false')
  xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + '?mode=6', listitem = listitem, isFolder = True, totalItems = 0)
    
  listitem = xbmcgui.ListItem("Paieška")
  listitem.setProperty('IsPlayable', 'false')
  xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + '?mode=7', listitem = listitem, isFolder = True, totalItems = 0)
  
  xbmcplugin.setContent(int( sys.argv[1] ), 'tvshows')
  xbmc.executebuiltin('Container.SetViewMode(515)')
  xbmcplugin.endOfDirectory(int(sys.argv[1]))

def addVideo(video):
  listitem = xbmcgui.ListItem(video['title'])
  listitem.setProperty('IsPlayable', 'true')
    
  info = {}
  info['title'] = video['title']
  info['plot'] = video['description']
    
  try:
    info['aired'] = video['broadcasts'][0]['air_at'][0:10]
  except:
    info['aired'] = video['publish_at'][0:10]
    
  try:
    info['genre'] = video['format_categories'][0]['name']
  except:
    pass
    
  position = video['format_position']
  if position['is_episodic']:
    info['season'] = position['season']
    info['episode'] = position['episode']
      
  if hasattr(listitem, 'addStreamInfo'):
    listitem.addStreamInfo('video', { 'duration': video['duration'] })
  else:
    info['duration'] = video['duration']
    
  listitem.setInfo(type = 'video', infoLabels = info )
    
  url = ''
  img = None
  if '_links' in video:
    links = video['_links']
      
    if 'image' in links and links['image']['href']:	
      img = links['image']['href'].replace('{size}', '1280x720')
      listitem.setProperty('Fanart_Image', img)
      listitem.setThumbnailImage(img)
	
    if 'stream' in links:
      url = links['stream']['href']
    
  u = {}
  if video['publishing_status']['type'] == 'live_countdown':
    u['mode'] = 15
    time = video['publishing_status']['until']
    u['time'] = time[0:10]+' '+time[11:16]
  else:
    u['mode'] = 10
    u['url'] = url
    u['title'] = video['title']
    if img:
      u['img'] = img
  xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + '?' + urllib.urlencode(u), listitem = listitem, isFolder = False, totalItems = 0)
  

def listSections(data):
  
  try:    
    data = data['_embedded']['sections']
  except:
    return
  
  for section in data:
    listVideos(section)

def listVideos(data):

  page = data['count']['page']
  total_pages = data['count']['total_pages']
  
  try:
    data = data['_embedded']['videos']
  except:
    return
  
  titles = {}
  
  for video in data:
    if video['title'] in titles:
      titles[video['title']] = titles[video['title']] + 1
    else:
      titles[video['title']] = 1
  
  for video in data:
    if titles[video['title']] > 1:
      video['title'] = video['title'] + ' ' + video['publish_at'][0:10]
    addVideo(video)
  
  if page < total_pages:
    listitem = xbmcgui.ListItem('[Daugiau...] (%d/%d)' % (page, total_pages))
    listitem.setProperty('IsPlayable', 'false')
    
    u = {}
    u['mode'] = mode
    u['page'] = page + 1
    
    if 'url' in params:
      u['url'] = urllib.unquote_plus(params['url'])
    
    xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + '?' + urllib.urlencode(u), listitem = listitem, isFolder = True, totalItems = 0)
  
  xbmcplugin.setContent(int( sys.argv[1] ), 'tvshows')
  xbmc.executebuiltin('Container.SetViewMode(503)')
  xbmcplugin.endOfDirectory(int(sys.argv[1]))
  

def featured(page):
  
  data = tv3.getFeatured(page)
  listSections(data)
  
def latest(page):
  
  data = tv3.getLatest(page)
  listSections(data)
  
def popular(page):
  
  data = tv3.getPopular(page)
  listSections(data)
  
def colections():
  
  data = tv3.getCollections()
  
  try:    
    data = data['_embedded']['sections'][0]
  except:
    return
  
  page = data['count']['page']
  total_pages = data['count']['total_pages']
  
  try:
    data = data['_embedded']['collections']
  except:
    return
  
  for collection in data:
    listitem = xbmcgui.ListItem(collection['title'])
    listitem.setProperty('IsPlayable', 'false')
    
    info = {}
    info['title'] = collection['title']
    info['plot'] = collection['description']
    info['plotoutline'] = collection['subtitle']
    info['aired'] = collection['publish_at'][0:10]
    listitem.setInfo(type = 'video', infoLabels = info )
    
    img = collection['_links']['image']['href'].replace('{size}', '1280x720')
    listitem.setProperty('Fanart_Image', img)
    listitem.setThumbnailImage(img)
    
    u = {}
    u['mode'] = 11
    u['url'] = collection['_links']['self']['href']
    
    xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + '?' + urllib.urlencode(u), listitem = listitem, isFolder = True, totalItems = 0)
    
  xbmcplugin.setContent(int( sys.argv[1] ), 'tvshows')
  xbmc.executebuiltin('Container.SetViewMode(515)')
  xbmcplugin.endOfDirectory(int(sys.argv[1]))

def addFolder(item):
  
  listitem = xbmcgui.ListItem(item['title'])
  listitem.setProperty('IsPlayable', 'false')
  
  info = {}
  info['title'] = item['title']
  listitem.setInfo(type = 'video', infoLabels = info )
  
  img = None
  if 'image' in item:
    img = item['image']
  else:  
    img = item['_links']['image']['href'].replace('{size}', '1280x720')
  
  if img:
    listitem.setProperty('Fanart_Image', img)
    listitem.setThumbnailImage(img)
  
  u = {}
  u['mode'] = 12
  u['url'] = item['_links']['videos']['href']
  
  xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + '?' + urllib.urlencode(u), listitem = listitem, isFolder = True, totalItems = 0)
  

def videoListFromUrl(params):
  
  url = urllib.unquote_plus(params['url'])
  data = tv3.getJSON(url)
  
  try:    
    data = data['_embedded']['items']
  except:
    return
  
  for item in data:
    if item['_meta']['type'] == 'video':
      addVideo(item)
    elif item['_meta']['type'] == 'format':
      addFolder(item)
  
  xbmcplugin.setContent(int( sys.argv[1] ), 'tvshows')
  xbmc.executebuiltin('Container.SetViewMode(503)')
  xbmcplugin.endOfDirectory(int(sys.argv[1]))

def videos(params):
  
  url = urllib.unquote_plus(params['url'])
  
  page = ''
  if 'page' in params:
    page = '&page=' + params['page']
  
  data = tv3.getJSON(url + '&limit=100&order=-visible_from' + page)
  listVideos(data)

def latestClips(page):
  
  data = tv3.getLatestClips(page)
  listSections(data)
  
def liveMSG(params):
  
  time = urllib.unquote_plus(params['time'])
  
  dialog = xbmcgui.Dialog()
  dialog.ok( "Anonsas" , 'Transliacija prasidės: ' + time )

def playVideo(params):
  
  title = urllib.unquote_plus(params['title'])
  url = urllib.unquote_plus(params['url'])
  if 'img' in params:
    img = urllib.unquote_plus(params['img'])
  else:
    img = None
  
  data = tv3.getJSON(url)
  
  streamURL = ''
  streams = data['streams']
  if streams['hls']:
    streamURL = streams['hls']
  elif streams['high']:
    streamURL = streams['high']
  elif streams['medium']:
    streamURL = streams['medium']
  
  listitem = xbmcgui.ListItem(label = title)
  listitem.setPath(streamURL)
  if img:
    listitem.setThumbnailImage(img)
  xbmcplugin.setResolvedUrl(handle = int(sys.argv[1]), succeeded = True, listitem = listitem)	
  
def channels():
  
  data = tv3.getChannels()
  
  try:
    data = data['_embedded']['formats']
  except:
    pass
  
  for channel in data:
    addFolder(channel)
    
  xbmcplugin.setContent(int( sys.argv[1] ), 'tvshows')
  xbmc.executebuiltin('Container.SetViewMode(515)')
  xbmcplugin.endOfDirectory(int(sys.argv[1]))
  
def startSearch():
  
  dialog = xbmcgui.Dialog()
  searchKey = dialog.input('Muzikos paieška', type=xbmcgui.INPUT_ALPHANUM)
  search({'searchKey': urllib.quote_plus(searchKey), 'page': 1})
  

def search(parameters):
  
  searchKey = urllib.unquote_plus(parameters['searchKey'])
  page = int(parameters['page'])
  
  data = tv3.search(searchKey, page)
  try:
    data = data['_embedded']['formats']
    
    for channel in data:
      addFolder(channel)
    
  except:
    pass 
    
  xbmcplugin.setContent(int( sys.argv[1] ), 'tvshows')
  xbmc.executebuiltin('Container.SetViewMode(515)')
  xbmcplugin.endOfDirectory(int(sys.argv[1]))
  
# **************** main ****************

path = sys.argv[0]
params = getParameters(sys.argv[2])

mode = None
page = None

try:
  mode = int(params['mode'])
except:
  pass

try:
  page = int(params['page'])
except:
  pass

if mode == 1:
  featured(page)
elif mode == 2:
  latest(page)
elif mode == 3:
  popular(page)
elif mode == 4:
  colections()
elif mode == 5:
  latestClips(page)
elif mode == 6:
  channels()
elif mode == 7:
  startSearch()
elif mode == 10:
  playVideo(params)
elif mode == 11:
  videoListFromUrl(params)
elif mode == 12:
  videos(params)
elif mode == 15:
  liveMSG(params)
else:  
  build_main_directory()