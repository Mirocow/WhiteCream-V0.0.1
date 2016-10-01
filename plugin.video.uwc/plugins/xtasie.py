'''
    Ultimate Whitecream
    Copyright (C) 2015 mortael

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
    route.add(1, '[COLOR hotpink]Xtasie[/COLOR]', 'http://xtasie.com/porn-video-list/page/1/', 200, 'xtasie.png', '')
    route.add(200, '[COLOR hotpink]Categories[/COLOR]', 'http://xtasie.com/video-porn-categories/', 203, '', '')
    route.add(200, '[COLOR hotpink]Top Rated[/COLOR]', 'http://xtasie.com/top-rated-porn-videos/page/1/', 201, '', '')
    route.add(200, '[COLOR hotpink]Most Rated[/COLOR]', 'http://xtasie.com/most-viewed-porn-videos/page/1/', 201, '',
              '')
    route.add(200, '[COLOR hotpink]Search[/COLOR]', 'http://xtasie.com/?s=', 204, '', '')
    route.add(200, '', '', {'plugin': 'xtasie', 'call': 'Main'})
    route.add(201, '', '', {'plugin': 'xtasie', 'call': 'List', 'params': ['url']})
    route.add(202, '', '', {'plugin': 'xtasie', 'call': 'Playvid', 'params': ['url', 'name', 'download']})
    route.add(203, '', '', {'plugin': 'xtasie', 'call': 'Cat', 'params': ['url']})
    route.add(204, '', '', {'plugin': 'xtasie', 'call': 'Search', 'params': ['route', 'url', 'keyword']})


def Main():
    return List('http://xtasie.com/porn-video-list/page/1/')


def List(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile(
        r'<div class="image-holder">\s+<a href="([^"]+)".*?><img.*?data-original="([^"]+)" alt="([^"]+)"',
        re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 202, img, '')
    try:
        nextp = re.compile('<a class="next page-numbers" href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
        next = nextp[0]
        utils.addDir('Next Page', next, 201, '')
    except:
        pass
    return False


def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 204)
    else:
        title = keyword.replace(' ', '+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        return List(searchUrl)


def Cat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<p><a href="([^"]+)".*?<img src="([^"]+)".*?<h2>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(
        cathtml)
    for catpage, img, name in match:
        utils.addDir(name, catpage, 201, img)
    return False


def Playvid(url, name, download=None):
    utils.playVideoByUrl(url, name, download)
