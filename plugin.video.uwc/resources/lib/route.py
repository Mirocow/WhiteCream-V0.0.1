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

import copy
import os
import sys
import urllib
import utils

import xbmcplugin

progress = utils.progress
imgDir = utils.imgDir
rootDir = utils.rootDir
dialog = utils.dialog

class Route(object):
    _index = None
    _items = {}

    def add(self, route, name, url, mode, iconimage=None, page=None, channel=None, section=None, keyword='', folder=True):
        if not route in self._items.keys():
            self._items[route] = []

        self._items[route].append({
            'name': name,
            'url': url,
            'mode': mode,
            'iconimage': iconimage,
            'page': page,
            'channel': channel,
            'section': section,
            'keyword': keyword,
            'Folder': folder
        })

    def getParams(self):
        param = []
        paramstring = sys.argv[2]
        if len(paramstring) >= 2:
            params = sys.argv[2]
            cleanedparams = params.replace('?', '')
            if params[len(params) - 1] == '/':
                params = params[0:len(params) - 2]
            pairsofparams = cleanedparams.split('&')
            param = {}
            for i in range(len(pairsofparams)):
                splitparams = {}
                splitparams = pairsofparams[i].split('=')
                if (len(splitparams)) == 2:
                    param[splitparams[0]] = splitparams[1]

        return param


    def run(self):
        self.params = self.getParams()
        self.mode = None
        self.plugins = {}

        try:
            self.mode = int(self.params["mode"])
        except:
            pass

        if self.mode in self._items:
            items = copy.deepcopy(self._items[self.mode])
            for item in items:
                if not isinstance(item['mode'], dict):

                    image = ''
                    if item['iconimage']:
                        image = os.path.join(imgDir, item['iconimage'])

                    utils.addDir(
                        item['name'],
                        item['url'],
                        item['mode'],
                        image,
                        item['page'],
                        item['channel'],
                        item['section'],
                        item['keyword'],
                        item['Folder']
                    )

                    self._items[self.mode].remove(item)

            try:
                items = self._items[self.mode]
            except:
                pass

            if items:
                if isinstance(items[0]['mode'], dict):
                    mode = items[0]['mode']
                    plugin = self.loadPlugin(mode['plugin'])
                    params = []
                    if 'params' in mode:
                        for param in mode['params']:
                            for case in utils.switch(param):

                                if case('route'):
                                    params.append(self)
                                    break
                                if case('url'):
                                    try:
                                        params.append(urllib.unquote_plus(self.params["url"]))
                                    except:
                                        params.append(None)
                                    break
                                if case('name'):
                                    try:
                                        params.append(urllib.unquote_plus(self.params["name"]))
                                    except:
                                        params.append(None)
                                    break
                                if case('mode'):
                                    try:
                                        params.append(int(self.params["mode"]))
                                    except:
                                        params.append(None)
                                    break
                                if case('page'):
                                    try:
                                        params.append(int(self.params["page"]))
                                    except:
                                        params.append(1)
                                    break
                                if case('img'):
                                    try:
                                        params.append(urllib.unquote_plus(self.params["img"]))
                                    except:
                                        params.append(None)
                                    break
                                if case('download'):
                                    try:
                                        params.append(int(self.params["download"]))
                                    except:
                                        params.append(None)
                                    break
                                if case('fav'):
                                    try:
                                        params.append(self.params["fav"])
                                    except:
                                        params.append(None)
                                    break
                                if case('favmode'):
                                    try:
                                        params.append(int(self.params["favmode"]))
                                    except:
                                        params.append(None)
                                    break
                                if case('channel'):
                                    try:
                                        params.append(int(self.params["channel"]))
                                    except:
                                        params.append(None)
                                    break
                                if case('section'):
                                    try:
                                        params.append(int(self.params["section"]))
                                    except:
                                        params.append(None)
                                    break
                                if case('keyword'):
                                    try:
                                        params.append(urllib.unquote_plus(self.params["keyword"]))
                                    except:
                                        params.append(None)
                                    break

                    self._items = {}

                    if getattr(plugin, mode['call'])(*params) == True:
                        return

                    if self.mode in self._items:
                        for item in self._items[self.mode]:
                            if not isinstance(item['mode'], dict):

                                image = ''
                                if item['iconimage']:
                                    image = os.path.join(imgDir, item['iconimage'])

                                utils.addDir(
                                    item['name'],
                                    item['url'],
                                    item['mode'],
                                    image,
                                    item['page'],
                                    item['channel'],
                                    item['section'],
                                    item['keyword'],
                                    item['Folder']
                                )

        xbmcplugin.endOfDirectory(utils.addon_handle, cacheToDisc=False)

    def loadPlugin(self, plugin):
        plugin = plugin.replace(".py", "")
        #dialog.ok("Debug", "Load plugin: " + plugin)
        sys.path = [utils.pluginsDir] + sys.path
        return __import__(plugin, None, None, [''])
