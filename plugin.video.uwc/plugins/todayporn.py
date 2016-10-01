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


def init(route):
    route.add(1, '[COLOR hotpink]TodayPorn[/COLOR]', 'http://www.todayporn.com/page1.html', 90, 'tp.png', '')
    route.add(90, '[COLOR hotpink]Categories[/COLOR]', 'http://www.todayporn.com/channels/', 93, '', '')
    route.add(90, '[COLOR hotpink]Pornstars[/COLOR]', 'http://www.todayporn.com/pornstars/page1.html', 95, '', '')
    route.add(90, '[COLOR hotpink]Top Rated[/COLOR]', 'http://www.todayporn.com/top-rated/a/page1.html', 91, '', '')
    route.add(90, '[COLOR hotpink]Most Viewed[/COLOR]', 'http://www.todayporn.com/most-viewed/a/page1.html', 91, '', '')
    route.add(90, '[COLOR hotpink]Search[/COLOR]', 'http://www.todayporn.com/search/page1.html?q=', 94, '', '')
    route.add(90, '', '', {'plugin': 'todayporn', 'call': 'Main'})
    route.add(91, '', '', {'plugin': 'todayporn', 'call': 'List', 'params': ['url']})
    route.add(92, '', '', {'plugin': 'todayporn', 'call': 'Playvid', 'params': ['url', 'name', 'download']})
    route.add(93, '', '', {'plugin': 'todayporn', 'call': 'Cat', 'params': ['url']})
    route.add(94, '', '', {'plugin': 'todayporn', 'call': 'Search', 'params': ['route', 'url', 'keyword']})
    route.add(95, '', '', {'plugin': 'todayporn', 'call': 'Pornstars', 'params': ['url']})


def Main():
    List('http://www.todayporn.com/page1.html', 1)
    return False


def List(url, page):
    listhtml = utils.getHtml(url, '')
    match = re.compile('prefix="([^"]+)[^<]+[^"]+"([^"]+)">([^<]+)<[^"]+[^>]+>([^\s]+)\s',
                       re.DOTALL | re.IGNORECASE).findall(listhtml)
    for thumb, videourl, name, duration in match:
        name = utils.cleantext(name)
        videourl = "http://www.todayporn.com" + videourl
        thumb = thumb + "1.jpg"
        name = name + " [COLOR deeppink]" + duration + "[/COLOR]"
        utils.addDownLink(name, videourl, 92, thumb, '')
    if re.search('Next &raquo;</a>', listhtml, re.DOTALL | re.IGNORECASE):
        npage = page + 1
        url = url.replace('page' + str(page), 'page' + str(npage))
        utils.addDir('Next Page (' + str(npage) + ')', url, 91, '', npage)
    return False


def layvid(url, name, download=None):
    videopage = utils.getHtml(url, '')
    match = re.compile(r"url: '([^']+)',\s+f", re.DOTALL | re.IGNORECASE).findall(videopage)
    if match:
        videourl = match[0]
        if download == 1:
            utils.downloadVideo(videourl, name)
        else:
            iconimage = xbmc.getInfoImage("ListItem.Thumb")
            listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
            listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
            xbmc.Player().play(videourl, listitem)


def Cat(url):
    caturl = utils.getHtml(url, '')
    match = re.compile('<img src="([^"]+)"[^<]+<[^"]+"([^"]+)">([^<]+)<', re.DOTALL | re.IGNORECASE).findall(caturl)
    for thumb, caturl, cat in match:
        caturl = "http://www.todayporn.com" + caturl + "page1.html"
        utils.addDir(cat, caturl, 91, thumb, 1)
    return False


def Pornstars(url, page):
    pshtml = utils.getHtml(url, '')
    pornstars = re.compile("""img" src='([^']+)'[^<]+<[^"]+"([^"]+)"[^>]+>([^<]+)<.*?total[^>]+>([^<]+)<""",
                           re.DOTALL | re.IGNORECASE).findall(pshtml)
    for img, psurl, title, videos in pornstars:
        psurl = "http://www.todayporn.com" + psurl + "page1.html"
        title = title + " [COLOR deeppink]" + videos + "[/COLOR]"
        utils.addDir(title, psurl, 91, img, 1)
    if re.search('Next &raquo;</a>', pshtml, re.DOTALL | re.IGNORECASE):
        npage = page + 1
        url = url.replace('page' + str(page), 'page' + str(npage))
        utils.addDir('Next Page (' + str(npage) + ')', url, 95, '', npage)
    return False


def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 94)
    else:
        title = keyword.replace(' ', '+')
        searchUrl = searchUrl + title + "&s=new"
        print "Searching URL: " + searchUrl
        List(searchUrl, 1)
