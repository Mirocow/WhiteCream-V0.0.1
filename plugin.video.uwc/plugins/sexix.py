'''
    Ultimate Whitecream
    Copyright (C) 2016 mortael

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


def init(route):
    route.add(1, '[COLOR hotpink]Sexix[/COLOR]', 'http://sexix.net/', 450, 'sexix.png', '')
    route.add(450, '[COLOR hotpink]Categories[/COLOR]', 'http://sexix.net/', 453, '', '')
    route.add(450, '[COLOR hotpink]Search[/COLOR]', 'http://sexix.net/?s=', 454, '', '')
    route.add(450, '', '', {'plugin': 'sexix', 'call': 'Main'})
    route.add(451, '', '', {'plugin': 'sexix', 'call': 'List', 'params': ['url', 'page']})
    route.add(453, '', '', {'plugin': 'sexix', 'call': 'Cat', 'params': ['url']})
    route.add(452, '', '', {'plugin': 'sexix', 'call': 'Playvid', 'params': ['url', 'name', 'download']})
    route.add(454, '', '', {'plugin': 'sexix', 'call': 'Search', 'params': ['route', 'url', 'keyword']})


def Main():
    List('http://sexix.net/page/1/?orderby=date')
    return False


def List(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<div id="main">(.*?)<div id="sidebar', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
    match1 = re.compile(r'data-id="\d+" title="([^"]+)" href="([^"]+)".*?src="([^"]+)"',
                        re.DOTALL | re.IGNORECASE).findall(match)
    for name, videopage, img in match1:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 452, img, '')
    try:
        nextp = re.compile('href="([^"]+)">Next', re.DOTALL | re.IGNORECASE).findall(match)
        utils.addDir('Next Page', nextp[0], 451, '')
    except:
        pass
    return False


def Playvid(url, name, download):
    videopage = utils.getHtml(url)
    plurl = re.compile('\?u=([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)[0]
    plurl = 'http://sexix.net/qaqqew/playlist.php?u=' + plurl
    plpage = utils.getHtml(plurl, url)
    videourl = re.compile('file="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(plpage)[0]
    if videourl:
        utils.playvid(videourl, name, download)
    else:
        utils.notify('Oh oh', 'Couldn\'t find a video')


def Cat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<a href="(http://sexix.net/videotag/[^"]+)"[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(
        cathtml)
    for catpage, name in match:
        utils.addDir(name, catpage, 451, '')
    return False


def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 454)
    else:
        title = keyword.replace(' ', '+')
        searchUrl = searchUrl + title
        List(searchUrl)
