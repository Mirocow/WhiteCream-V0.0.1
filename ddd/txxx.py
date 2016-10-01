'''
    Ultimate Whitecream
    Copyright (C) 2016 mirocow

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

import urllib
import urllib2
import re
import cookielib
import os.path
import sys
import socket
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import search
import sqlite3
import base64
import json
import gzip
import urlparse
import hashlib
from resources.lib import utils
from resources.lib import route
from resources.lib import cloudflare
from resources.lib import compat
from resources.lib import jjdecode
from resources.lib import jsunpack
from StringIO import StringIO


def Main():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://www.txxx.com/categories/',906,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://www.txxx.com/search/?s=',908,'','')
    List('http://www.txxx.com/latest-updates/1/')
    return False


def List(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<a href="([^"]+)".*?src="([^"]+)".*?alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 907, img, '')
    try:
        nextp = re.compile('href="([^"]+)" title="Next Page"', re.DOTALL | re.IGNORECASE).findall(listhtml)
        utils.addDir('Next Page', nextp[0], 905,'')
    except: pass
    return False


def Playvid(url, name, download):
    utils.playVideoByUrl(url, name, download)


def Cat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<a class="link--pressed " href="([^"]+)">([^<]+)<span class="link__badge">').findall(cathtml)
    for catpage, name in match:
        utils.addDir(name, catpage, 905, '')
    return False


def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 908)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        List(searchUrl)

