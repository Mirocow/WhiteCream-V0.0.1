#-*- coding: utf-8 -*-

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

import sqlite3, utils, urllib
import xbmc

favoritesdb = utils.favoritesdb


def init(route):
    route.add(902, '', '', {'plugin': 'search', 'call': 'newSearch', 'params': ['url', 'channel']})
    route.add(903, '', '', {'plugin': 'search', 'call': 'clearSearch'})


def searchDir(route, url, mode, page=None):
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM keywords")
        for (keyword,) in c.fetchall():
            name = '[COLOR deeppink]' + urllib.unquote_plus(keyword) + '[/COLOR]'
            utils.addDir(name, url, mode, '', page=page, keyword=keyword)

    except: pass
    route.add(mode, '[COLOR hotpink]Add Keyword[/COLOR]', url, 902, '', '', mode, folder=False)
    route.add(mode, '[COLOR hotpink]Clear list[/COLOR]', '', 903, '', folder=False)
    return False


def newSearch(url, channel):
    vq = utils._get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    addKeyword(title)
    xbmc.executebuiltin('Container.Refresh')


def clearSearch():
    delKeyword()
    xbmc.executebuiltin('Container.Refresh')


def addKeyword(keyword):
    xbmc.log(keyword)
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    c.execute("INSERT INTO keywords VALUES (?)", (keyword,))
    conn.commit()
    conn.close()


def delKeyword():
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    c.execute("DELETE FROM keywords;")
    conn.commit()
    conn.close()