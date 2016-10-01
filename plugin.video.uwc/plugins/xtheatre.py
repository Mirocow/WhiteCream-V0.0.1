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

import plugins.search
from resources.lib import utils

# from resources.lib import compat

addon = utils.addon

sortlistxt = [addon.getLocalizedString(30022), addon.getLocalizedString(30023), addon.getLocalizedString(30024),
              addon.getLocalizedString(30025)]


def init(route):
    route.add(2, '[COLOR hotpink]Xtheatre[/COLOR]', 'http://xtheatre.net/page/1/', 20, 'xt.png', '')
    route.add(20, '[COLOR hotpink]Categories[/COLOR]', 'http://xtheatre.net/categories/', 22, '', '')
    route.add(20, '[COLOR hotpink]Search[/COLOR]', 'http://xtheatre.net/page/1/?s=', 24, '', '')
    route.add(20, '[COLOR hotpink]Current sort:[/COLOR] ' + sortlistxt[int(addon.getSetting("sortxt"))], '', 25, '', '')
    route.add(20, '', '', {'plugin': 'xtheatre', 'call': 'Main'})
    route.add(21, '', '', {'plugin': 'xtheatre', 'call': 'List', 'params': ['url', 'page']})
    route.add(22, '', '', {'plugin': 'xtheatre', 'call': 'Cat', 'params': ['url']})
    route.add(23, '', '', {'plugin': 'xtheatre', 'call': 'Video', 'params': ['url', 'name', 'download']})
    route.add(24, '', '', {'plugin': 'xtheatre', 'call': 'Search', 'params': ['route', 'url', 'keyword']})
    route.add(25, '', '', {'plugin': 'xtheatre', 'call': 'Settings', 'params': ['route']})


def Settings(route):
    addon.openSettings()
    Main(route)


def Main():
    return List('http://xtheatre.net/category/movies/page/1/', 1)


def Cat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('src="([^"]+)"[^<]+</noscript>.*?<a href="([^"]+)"[^<]+<span>([^<]+)</s.*?">([^<]+)',
                       re.DOTALL | re.IGNORECASE).findall(cathtml)
    for img, catpage, name, videos in match:
        catpage = catpage + 'page/1/'
        name = name + ' [COLOR deeppink]' + videos + '[/COLOR]'
        utils.addDir(name, catpage, 21, img, 1)
    return False


def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        return plugins.search.searchDir(url, 24)
    else:
        title = keyword.replace(' ', '+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        return List(searchUrl, 1)


def List(url, page):
    sort = SortMethod()
    if re.search('\?', url, re.DOTALL | re.IGNORECASE):
        url = url + '&filtre=' + sort + '&display=extract'
    else:
        url = url + '?filtre=' + sort + '&display=extract'
    print url
    listhtml = utils.getHtml(url, '')
    match = re.compile(
        'src="([^"]+?)" class="attachment.*?<a href="([^"]+)" title="([^"]+)".*?<div class="right">.<p>([^<]+)</p>',
        re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, videopage, name, desc in match:
        name = utils.cleantext(name)
        desc = utils.cleantext(desc)
        utils.addDownLink(name, videopage, 23, img, desc)

    if re.search('<link rel="next"', listhtml, re.DOTALL | re.IGNORECASE):
        npage = page + 1
        url = url.replace('/page/' + str(page) + '/', '/page/' + str(npage) + '/')
        utils.addDir('Next Page (' + str(npage) + ')', url, 21, '', npage)
        return False


def Video(url, name, download):
    utils.playVideoByUrl(url, name, download)
    return True


def SortMethod():
    sortoptions = {0: 'date',
                   1: 'title',
                   2: 'views',
                   3: 'likes'}
    sortvalue = addon.getSetting("sortxt")
    return sortoptions[int(sortvalue)]
