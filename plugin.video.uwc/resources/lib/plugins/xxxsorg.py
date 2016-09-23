'''
    Ultimate Whitecream
    Copyright (C) 2016 mortael
    Copyright (C) 2016 anton40
 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
 
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
 
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon
import search
from resources.lib import utils

progress = utils.progress

def init(route):
    route.add(1, '[COLOR hotpink]XXX Streams (org)[/COLOR]','http://xxxstreams.org/',420,'xxxsorg.png','')

    route.add(420, '[COLOR hotpink]Categories[/COLOR]','http://xxxstreams.org/',423,'','')
    route.add(420, '[COLOR hotpink]Search[/COLOR]','http://xxxstreams.org/?s=',424,'','')
    route.add(420, '', '', {'plugin': 'xxxsorg', 'call': 'Main'})

    route.add(421, '', '', {'plugin': 'xxxsorg', 'call': 'List', 'params': ['url']})
    route.add(422, '', '', {'plugin': 'xxxsorg', 'call': 'Playvid', 'params': ['url', 'name', 'download']})
    route.add(423, '', '', {'plugin': 'xxxsorg', 'call': 'Categories', 'params': ['url']})
    route.add(424, '', '', {'plugin': 'xxxsorg', 'call': 'Search', 'params': ['route', 'url', 'keyword']})
    route.add(425, '', '', {'plugin': 'xxxsorg', 'call': 'ListSearch', 'params': ['url']})
 
def Main():
    return List('http://xxxstreams.org/page/1')

 
def List(url):
    html = utils.getHtml(url, '')
    match = re.compile('<div class="entry-content">.*?<img src="([^"]+)".*?<a href="([^"]+)" class="more-link">.+?<span class="screen-reader-text">([^"]+)</span>', re.DOTALL | re.IGNORECASE).findall(html)
    for img, videopage, name in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 422, img, '')
    try:
        nextp = re.compile('<a class="next.*?href="(.+?)">', re.DOTALL | re.IGNORECASE).findall(html)
        utils.addDir('Next Page', nextp[0], 421,'')
    except: pass

    return False

def ListSearch(url):
    html = utils.getHtml(url, '').replace('\n','')
    match = re.compile('bookmark">([^<]+)</a></h1>.*?<img src="([^"]+)".*?href="([^"]+)"').findall(html)
    for name, img, videopage in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 422, img, '')
    try:
        nextp = re.compile('<link rel="next" href="(.+?)" />', re.DOTALL | re.IGNORECASE).findall(html)
        utils.addDir('Next Page', nextp[0], 425,'')
    except: pass
    return False

def Playvid(url, name, download):
    progress.create('Play video', 'Searching videofile.')
    progress.update( 10, "", "Loading video page", "" )
    url = url.split('#')[0]
    videopage = utils.getHtml(url, '')
    entrycontent = re.compile('entry-content">(.*?)entry-content', re.DOTALL | re.IGNORECASE).findall(videopage)[0]
    links = re.compile('href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(entrycontent)
    videourls = " "
    for link in links:
        if 'securely' in link:
            link = utils.getVideoLink(link, url)
        videourls = videourls + " " + link
    utils.playVideoBySource(videourls, name, download, url)
 
 
def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<li.+?class=".+?menu-item-object-post_tag.+?"><a href="(.+?)">(.+?)</a></li>').findall(cathtml)
    for catpage, name in match:
        utils.addDir(name, catpage, 421, '')    
    return False
 
def Search(route, url, keyword=None):
    searchUrl = url
    if not keyword:
        return search.searchDir(route, url, 424)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        return ListSearch(searchUrl)