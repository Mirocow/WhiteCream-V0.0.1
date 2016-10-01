'''
    Ultimate Whitecream
    Copyright (C) 2015 mortael
    Copyright (C) 2015 Fr33m1nd

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

from resources.lib import utils

# from resources.lib import compat

progress = utils.progress


def init(route):
    route.add(1, '[COLOR hotpink]Pornkino[/COLOR]', 'http://pornkino.to/', 330, 'pornkino.png', '')
    route.add(330, '[COLOR hotpink]Search[/COLOR]', 'http://pornkino.to/?s=', 333, '', '')
    route.add(330, '[COLOR hotpink]Categories[/COLOR]', 'http://pornkino.to/', 334, '', '')
    route.add(330, '', '', {'plugin': 'xtasie', 'call': 'Main'})
    route.add(331, '', '', {'plugin': 'xtasie', 'call': 'List', 'params': ['url']})
    route.add(332, '', '', {'plugin': 'xtasie', 'call': 'Playvid', 'params': ['url', 'name', 'download']})
    route.add(334, '', '', {'plugin': 'xtasie', 'call': 'Cat', 'params': ['url']})
    route.add(333, '', '', {'plugin': 'xtasie', 'call': 'Search', 'params': ['route', 'url', 'keyword']})


def Main():
    List('http://pornkino.to/')
    return False


def List(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<article id=.*?class="cover" src="([^"]+)".*?alt="([^"]+)".*?href="([^"]+)"',
                       re.DOTALL | re.IGNORECASE).findall(listhtml)
    for img, name, videopage in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 332, img, '')
    try:
        nextp = re.compile('<a class="next page-numbers" href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
        nextp = nextp[0].replace("&#038;", "&")
        utils.addDir('Next Page', nextp, 331, '')
    except:
        pass
    return False


def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 333)
    else:
        title = keyword.replace(' ', '+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)


def Cat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile("Kategorien</span>.*?<ul>(.*?)</ul>", re.DOTALL | re.IGNORECASE).findall(cathtml)
    match1 = re.compile(r'href="([^"]+)"[^>]+>([^<]+)</a> \((\d+)', re.DOTALL | re.IGNORECASE).findall(match[0])
    for catpage, name, videos in match1:
        name = name + ' [COLOR deeppink](%s)[/COLOR]' % videos
        utils.addDir(name, catpage, 331, '')
    return False


def Playvid(url, name, download=None):
    utils.playVideoByUrl(url, name, download)
