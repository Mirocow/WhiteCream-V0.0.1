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

import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils


def Main():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://www.txxx.com/categories/',906,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://www.txxx.com/search/?s=',908,'','')
    List('http://www.txxx.com/latest-updates/1/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


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
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Playvid(url, name, download):
    utils.playVideoByUrl(url, name, download)


def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<a class="link--pressed " href="([^"]+)">([^<]+)<span class="link__badge">').findall(cathtml)
    for catpage, name in match:
        utils.addDir(name, catpage, 905, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 908)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        List(searchUrl)

