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

import socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon
import route, utils

socket.setdefaulttimeout(60)

xbmcplugin.setContent(utils.addon_handle, 'movies')
addon = xbmcaddon.Addon(id=utils.__scriptid__)
progress = utils.progress
imgDir = utils.imgDir
rootDir = utils.rootDir
dialog = utils.dialog

if not addon.getSetting('uwcage') == 'true':
    age = dialog.yesno('WARNING :This addon contains adult material.','You may enter only if you are at least 18 years of age.', nolabel='Exit', yeslabel='Enter')
    if age:
        addon.setSetting('uwcage','true')
else:
    age = True

if age:
    route = route.Route()

    # Index
    route.add(None, '[COLOR hotpink]Whitecream[/COLOR] [COLOR white]Scenes[/COLOR]','',1,'icon.png','')
    route.add(None, '[COLOR hotpink]Whitecream[/COLOR] [COLOR white]Movies[/COLOR]','',2,'icon.png','')
    route.add(None, '[COLOR hotpink]Whitecream[/COLOR] [COLOR white]Favorites[/COLOR]','',901,'icon.png','')

    # Add plugins (Plugin must has merhod init())
    plugins = [
        'favorites',
        'search',
        'watchxxxfree', 'xxxsorg', 'beeg',
        'xtheatre',
    ]
    for plugin in plugins:
        plugin = route.load_plugin(plugin)
        getattr(plugin, 'init')(route)

    route.run()
