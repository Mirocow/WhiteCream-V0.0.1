'''
    Ultimate Whitecream
    Copyright (C) 2015 mortael
    Copyright (C) 2015 anton40

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
    route.add(2, '[COLOR hotpink]PornKinoX[/COLOR]', 'http://www.pornkinox.com', 470, 'pornkinox.png', '')
    route.add(470, '[COLOR hotpink]Search[/COLOR]', 'http://pornkinox.to/?s=', 473, '', '')
    route.add(470, '[COLOR hotpink]Categories[/COLOR]', 'http://pornkinox.to/', 474, '', '')
    route.add(470, '', '', {'plugin': 'pornkinox', 'call': 'Main'})
    route.add(471, '', '', {'plugin': 'pornkinox', 'call': 'List', 'params': ['url']})
    route.add(472, '', '', {'plugin': 'pornkinox', 'call': 'Playvid', 'params': ['url', 'name', 'download']})
    route.add(474, '', '', {'plugin': 'pornkinox', 'call': 'Cat', 'params': ['url']})
    route.add(473, '', '', {'plugin': 'pornkinox', 'call': 'Search', 'params': ['route', 'url', 'keyword']})


def Main():
    List('http://pornkinox.to/')
    return False


def List(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<article[^>]+>.+?<a href="([^"]+)" title="([^"]+)".*?src="([^"]+)"',
                       re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, name, img in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 472, img, '')
    try:
        nextp = re.compile('<a class="next page-numbers" href="(.+?)"><i class="fa fa-angle-right"',
                           re.DOTALL | re.IGNORECASE).findall(listhtml)
        nextp = nextp[0].replace("&#038;", "&")
        utils.addDir('Next Page', nextp, 471, '')
    except:
        pass
    return False


def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 473)
    else:
        title = keyword.replace(' ', '+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)


def Cat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<li class="cat-item.+?"><a href="(.+?)" title=".+?">(.+?)</a> \((.+?)\)',
                       re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name, videos in match:
        name = name + ' [COLOR deeppink](%s)[/COLOR]' % videos
        utils.addDir(name, catpage, 471, '')
    return False


def Playvid(url, name, download=None):
    utils.playVideoByUrl(url, name, download)
