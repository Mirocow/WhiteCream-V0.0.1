# -*- coding: utf-8 -*-

'''
    Ultimate Whitecream
    Copyright (C) 2015 mortael, mirocow

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

import re

import search
from resources.lib import utils

# from resources.lib import compat

addon = utils.addon

sortlistwxf = [addon.getLocalizedString(30012), addon.getLocalizedString(30013), addon.getLocalizedString(30014)]


def init(route):
    route.add(1, '[COLOR hotpink]WatchXXXFree[/COLOR]', 'http://www.watchxxxfree.com/page/1/', 10, 'wxf.png')
    route.add(10, '[COLOR hotpink]Categories[/COLOR]', 'http://www.watchxxxfree.com/categories/', 12, '', '')
    route.add(10, '[COLOR hotpink]Search[/COLOR]', 'http://www.watchxxxfree.com/page/1/?s=', 14, '', '')
    route.add(10, '[COLOR hotpink]Top Pornstars[/COLOR]', 'http://www.watchxxxfree.com/top-pornstars/', 15, '', '')
    route.add(10, '[COLOR hotpink]Current sort:[/COLOR] ' + sortlistwxf[int(addon.getSetting("sortwxf"))], '', 16, '',
              '')
    route.add(10, '', '', {'plugin': 'watchxxxfree', 'call': 'Main'})
    route.add(11, '', '', {'plugin': 'watchxxxfree', 'call': 'List', 'params': ['url', 'page']})
    route.add(12, '', '', {'plugin': 'watchxxxfree', 'call': 'Cat', 'params': ['url']})
    route.add(13, '', '', {'plugin': 'watchxxxfree', 'call': 'Video', 'params': ['url', 'name', 'download']})
    route.add(14, '', '', {'plugin': 'watchxxxfree', 'call': 'Search', 'params': ['route', 'url', 'keyword']})
    route.add(15, '', '', {'plugin': 'watchxxxfree', 'call': 'PS', 'params': ['url']})
    route.add(16, '', '', {'plugin': 'watchxxxfree', 'call': 'Settings', 'params': ['route']})


def Settings(route):
    addon.openSettings()
    Main(route)


def Main():
    return List('http://watchxxxfree.com/page/1/', 1)


def Cat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('data-lazy-src="([^"]+)".*?<a href="([^"]+)"[^<]+<span>([^<]+)</s.*?">([^<]+)',
                       re.DOTALL | re.IGNORECASE).findall(cathtml)
    for img, catpage, name, videos in match:
        catpage = catpage + 'page/1/'
        name = name + ' [COLOR deeppink]' + videos + '[/COLOR]'
        utils.addDir(name, catpage, 11, img, 1)
    return False


def PS(url):
    tpshtml = utils.getHtml(url, '')
    match = re.compile("<li><a href='([^']+)[^>]+>([^<]+)", re.DOTALL | re.IGNORECASE).findall(tpshtml)
    for tpsurl, name in match:
        tpsurl = tpsurl + 'page/1/'
        utils.addDir(name, tpsurl, 11, '', 1)
    return False


def Search(route, url, keyword=None):
    searchUrl = url
    if not keyword:
        return search.searchDir(route, url, 14)
    else:
        title = keyword.replace(' ', '+')
        searchUrl = searchUrl + title
        return List(searchUrl, 1)


def List(url, page=1, onelist=None):
    if onelist:
        url = url.replace('/page/1/', '/page/' + str(page) + '/')

    sort = getSortMethod()

    if re.search('\?', url, re.DOTALL | re.IGNORECASE):
        url = url + '&filtre=' + sort + '&display=extract'
    else:
        url = url + '?filtre=' + sort + '&display=extract'
    try:
        listhtml = utils.getHtml(url, '')
    except:
        utils.notify('Oh oh', 'It looks like this website is down.')
        return None
    match = re.compile('data-lazy-src="([^"]+)".*?<a href="([^"]+)" title="([^"]+)".*?<p>([^<]+)</p>',
                       re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, videopage, name, desc in match:
        name = utils.cleantext(name)
        desc = utils.cleantext(desc)
        utils.addDownLink(name, videopage, 13, img, desc)

    if not onelist:
        if re.search('<link rel="next"', listhtml, re.DOTALL | re.IGNORECASE):
            npage = page + 1
            url = url.replace('/page/' + str(page) + '/', '/page/' + str(npage) + '/')
            utils.addDir('Next Page (' + str(npage) + ')', url, 11, '', npage)
        return False


def Video(url, name, download):
    utils.playVideoByUrl(url, name, download=None)
    return True


def getSortMethod():
    sortoptions = {0: 'date',
                   1: 'rate',
                   2: 'views'}
    sortvalue = addon.getSetting("sortwxf")
    return sortoptions[int(sortvalue)]
