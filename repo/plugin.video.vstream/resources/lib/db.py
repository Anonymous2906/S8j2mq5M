# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import xbmc
import xbmcaddon
import requests
from resources.lib.comaddon import dialog, addon, VSlog, VSProfil
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.util import QuotePlus, Unquote

SITE_IDENTIFIER = 'cDb'
SITE_NAME = 'DB'

class cDb(object):
    def __init__(self):
        self.addon = xbmcaddon.Addon("plugin.program.bazoconfigcommu")
        self.pseudo = self.addon.getSetting("pseudo")
        self.server = self.addon.getSetting("server")
        self.BASE_URL = f'{self.server}/profils/{self.pseudo}/requete.php'
        self.DIALOG = dialog()
        self.ADDON = addon()
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def _send_request(self, action, params=None, data=None):
        params = params or {}
        params['action'] = action
        if data:
            response = requests.post(self.BASE_URL, params=params, json=data)
        else:
            response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()

    # ***********************************
    #   History fonctions
    # ***********************************

    def insert_history(self, meta):
        data = {
            'title': Unquote(meta['title']),
            'disp': meta['disp'],
            'icone': 'icon.png'
        }
        try:
            self._send_request('insertHistory', data=data)
            VSlog('SQL INSERT history Successfully')
        except Exception as e:
            VSlog(f'SQL ERROR INSERT, title = {data["title"]}, {e}')

    def get_history(self):
        try:
            return self._send_request('getHistory')
        except Exception as e:
            VSlog(f'SQL ERROR EXECUTE, {e}')
            return None

    def del_history(self):
        oInputParameterHandler = cInputParameterHandler()
        params = {}
        if oInputParameterHandler.exist('searchtext'):
            params['searchtext'] = oInputParameterHandler.getValue('searchtext')
        try:
            self._send_request('delHistory', params=params)
            dialog().VSinfo(addon().VSlang(30041))
            return False, False
        except Exception as e:
            VSlog(f'SQL ERROR DELETE : {e}')
            return False, False

    # ***********************************
    #   Watched fonctions
    # ***********************************

    def insert_watched(self, meta):
        data = {
            'tmdb_id': meta.get('tmdbId', ''),
            'title_id': meta['titleWatched'],
            'title': meta['title'],
            'siteurl': QuotePlus(meta['siteurl']),
            'site': meta['site'],
            'cat': meta.get('cat', '1'),
            'fav': meta['fav'],
            'season': meta.get('season', '')
        }
        try:
            self._send_request('insertWatched', data=data)
            VSlog('SQL INSERT watched Successfully')
        except Exception as e:
            VSlog(f'SQL ERROR INSERT watched : title = {e}')

    def get_watched(self, meta):
        params = {'titleWatched': meta['titleWatched']}
        try:
            result = self._send_request('getWatched', params=params)
            return result if result else False
        except Exception as e:
            VSlog(f'SQL ERROR {e}')
            return False

    def get_allwatched(self):
        try:
            return self._send_request('getAllWatched')
        except Exception as e:
            VSlog(f'SQL ERROR : {e}')
            return None

    def del_watched(self, meta):
        params = {'titleWatched': meta['titleWatched']}
        try:
            self._send_request('delWatched', params=params)
            return False, False
        except Exception as e:
            VSlog(f'SQL ERROR {e}')
            return False, False

    # ***********************************
    #   Resume fonctions
    # ***********************************

    def insert_resume(self, meta):
        data = {
            'title': meta['titleWatched'],
            'hoster': QuotePlus(meta['site']),
            'point': meta['point'],
            'total': meta['total']
        }
        try:
            self._send_request('insertResume', data=data)
        except Exception as e:
            VSlog(f'SQL ERROR INSERT : {e}')

    def get_resume(self, meta):
        params = {'titleWatched': meta['titleWatched']}
        try:
            result = self._send_request('getResume', params=params)
            return float(result['point']), float(result['total'])
        except Exception as e:
            VSlog(f'SQL ERROR : {e}')
            return False, False

    def del_resume(self, meta):
        params = {'titleWatched': meta['titleWatched']}
        try:
            self._send_request('delResume', params=params)
            return False, False
        except Exception as e:
            VSlog(f'SQL ERROR {e}')
            return False, False

    # ***********************************
    #   Bookmark fonctions
    # ***********************************

    def insert_bookmark(self, meta):
        data = {
            'title': meta['title'],
            'siteurl': QuotePlus(meta['siteurl']),
            'site': meta['site'],
            'fav': meta['fav'],
            'cat': meta['cat'],
            'icon': meta['icon'],
            'fanart': meta['fanart']
        }
        try:
            self._send_request('insertBookmark', data=data)
            dialog().VSinfo(addon().VSlang(30042), meta['title'], 4)
            VSlog(f'SQL INSERT favorite Successfully - {meta["title"]}')
        except Exception as e:
            VSlog(f'SQL ERROR INSERT : {e}')

    def get_bookmark(self):
        try:
            return self._send_request('getBookmarks')
        except Exception as e:
            VSlog(f'SQL ERROR EXECUTE : {e}')
            return None

    def del_bookmark(self, sSiteUrl='', sMovieTitle='', sCat='', sAll=False):
        params = {
            'siteurl': sSiteUrl,
            'title': sMovieTitle,
            'cat': sCat,
            'all': sAll
        }
        try:
            self._send_request('delBookmark', params=params)
            dialog().VSinfo(addon().VSlang(30044))
            return True
        except Exception as e:
            VSlog(f'SQL ERROR {e}')
            return False

    # ***********************************
    #   InProgress fonctions
    # ***********************************

    def insert_viewing(self, meta):
        data = {
            'tmdb_id': meta.get('sTmdbId', ''),
            'title_id': meta['titleWatched'],
            'title': meta['title'],
            'siteurl': QuotePlus(meta['siteurl']),
            'site': meta['site'],
            'fav': meta['fav'],
            'cat': meta['cat'],
            'season': meta.get('season', '')
        }
        try:
            self._send_request('insertViewing', data=data)
            VSlog('SQL INSERT viewing Successfully')
        except Exception as e:
            VSlog(f'SQL ERROR INSERT : {e}')

    def get_viewing(self):
        try:
            return self._send_request('getViewing')
        except Exception as e:
            VSlog(f'SQL ERROR : {e}')
            return None

    def del_viewing(self, meta):
        params = {
            'titleWatched': meta.get('titleWatched'),
            'cat': meta.get('cat')
        }
        try:
            self._send_request('delViewing', params=params)
            return True
        except Exception as e:
            VSlog(f'SQL ERROR {e}')
            return False

    # ***********************************
    #   Download fonctions
    # ***********************************

    def insert_download(self, meta):
        data = {
            'title': meta['title'],
            'url': QuotePlus(meta['url']),
            'path': meta['path'],
            'cat': meta['cat'],
            'icon': meta['icon'],
            'size': '',
            'totalsize': '',
            'status': 0
        }
        try:
            self._send_request('insertDownload', data=data)
            VSlog('SQL INSERT download Successfully')
        except Exception as e:
            VSlog(f'SQL ERROR INSERT : {e}')

    def get_download(self, meta=''):
        params = {}
        if meta:
            params['url'] = QuotePlus(meta['url'])
        try:
            return self._send_request('getDownload', params=params)
        except Exception as e:
            VSlog(f'SQL ERROR : {e}')
            return None

    def clean_download(self):
        try:
            self._send_request('cleanDownload')
            return False, False
        except Exception as e:
            VSlog(f'SQL ERROR : {e}')
            return False, False

    def reset_download(self, meta):
        params = {'url': QuotePlus(meta['url'])}
        try:
            self._send_request('resetDownload', params=params)
            return False, False
        except Exception as e:
            VSlog(f'SQL ERROR : {e}')
            return False, False

    def del_download(self, meta):
        params = {
            'url': QuotePlus(meta.get('url', '')),
            'path': meta.get('path', '')
        }
        try:
            self._send_request('delDownload', params=params)
            return False, False
        except Exception as e:
            VSlog(f'SQL ERROR : {e}')
            return False, False

    def cancel_download(self):
        try:
            self._send_request('cancelDownload')
            return False, False
        except Exception as e:
            VSlog(f'SQL ERROR : {e}')
            return False, False

    def update_download(self, meta):
        data = {
            'path': meta['path'],
            'size': meta['size'],
            'totalsize': meta['totalsize'],
            'status': meta['status']
        }
        try:
            self._send_request('updateDownload', data=data)
            return False, False
        except Exception as e:
            VSlog(f'SQL ERROR : {e}')
            return False, False
