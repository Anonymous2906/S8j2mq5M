# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import xbmc
import xbmcaddon
import requests

from resources.lib.comaddon import dialog, addon, isMatrix
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.gui.gui import cGui
from resources.lib.util import UnquotePlus

SITE_IDENTIFIER = 'cViewing'
SITE_NAME = 'Viewing'


class cViewing:

    def __init__(self):
        self.addon = xbmcaddon.Addon("plugin.program.bazoconfigcommu")
        self.pseudo = self.addon.getSetting("pseudo")
        self.server = self.addon.getSetting("server")
        self.BASE_URL = f'{self.server}/profils/{self.pseudo}/requete.php'
        self.DIALOG = dialog()
        self.ADDON = addon()

    def _send_request(self, action, params=None, data=None):
        params = params or {}
        params['action'] = action
        try:
            if data:
                response = requests.post(self.BASE_URL, params=params, json=data)
            else:
                response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            xbmc.log(f"Request to {self.BASE_URL} failed: {e}", xbmc.LOGERROR)
            self.DIALOG.VSinfo('Error', str(e))
            return None

    def delViewing(self):
        oInputParameterHandler = cInputParameterHandler()
        sTitleWatched = oInputParameterHandler.getValue('sTitleWatched')
        sCat = oInputParameterHandler.getValue('sCat')

        if not sTitleWatched:  # confirmation if delete ALL
            if not self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                return False

        params = {'titleWatched': sTitleWatched, 'cat': sCat}
        if self._send_request('delViewing', params=params):
            self.DIALOG.VSinfo(addon().VSlang(30072))
            cGui().updateDirectory()
            return True
        return False

    def delViewingMenu(self):
        sTitle = xbmc.getInfoLabel('ListItem.OriginalTitle')
        if not sTitle:  # confirmation if delete ALL
            if not self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                return False
        sCat = xbmc.getInfoLabel('ListItem.Property(sCat)')
        params = {'titleWatched': sTitle, 'cat': sCat}
        if self._send_request('delViewing', params=params):
            self.DIALOG.VSinfo(addon().VSlang(30072))
            cGui().updateDirectory()
            return True
        return False

    def showMenu(self):
        oGui = cGui()
        addons = addon()

        oOutputParameterHandler = cOutputParameterHandler()
        oGui.addDir(SITE_IDENTIFIER, 'getViewing', addons.VSlang(30126), 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '1')  # films
        oGui.addDir(SITE_IDENTIFIER, 'getViewing', addons.VSlang(30120), 'films.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '4')  # saisons
        oGui.addDir(SITE_IDENTIFIER, 'getViewing', '%s/%s' % (self.ADDON.VSlang(30121), self.ADDON.VSlang(30122)), 'series.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '5')  # Divers
        oGui.addDir(SITE_IDENTIFIER, 'getViewing', self.ADDON.VSlang(30410), 'buzz.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def getViewing(self):
        oGui = cGui()

        oInputParameterHandler = cInputParameterHandler()
        catFilter = oInputParameterHandler.getValue('sCat')

        row = self._send_request('getViewing')
        if not row:
            oGui.setEndOfDirectory()
            return

        for data in row:
            try:
                title = data.get('title', '')
                if not title:
                    continue

                siteurl = data.get('siteurl', '')
                if isMatrix():
                    siteurl = UnquotePlus(siteurl)
                else:
                    siteurl = UnquotePlus(siteurl)

                sTitleWatched = data.get('title_id', '')
                site = data.get('site', '')
                function = data.get('fav', '')
                cat = data.get('cat', '')
                sSeason = data.get('season', '')
                sTmdbId = data.get('tmdb_id', '')

                if catFilter and cat != catFilter:
                    continue

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteurl)
                oOutputParameterHandler.addParameter('sMovieTitle', title)
                oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
                oOutputParameterHandler.addParameter('sTitleWatched', sTitleWatched)
                oOutputParameterHandler.addParameter('sSeason', sSeason)
                oOutputParameterHandler.addParameter('sCat', cat)
                oOutputParameterHandler.addParameter('isViewing', True)

                # pourcentage de lecture
                meta = {'titleWatched': sTitleWatched}
                resume_data = self._send_request('getResume', params=meta)
                if resume_data:
                    resumetime, totaltime = resume_data.get('point', 0), resume_data.get('total', 0)
                    oOutputParameterHandler.addParameter('ResumeTime', resumetime)
                    oOutputParameterHandler.addParameter('TotalTime', totaltime)
                else:
                    oOutputParameterHandler.addParameter('ResumeTime', 0)
                    oOutputParameterHandler.addParameter('TotalTime', 0)

                if cat == '1':
                    oListItem = oGui.addMovie(site, function, title, 'films.png', '', title, oOutputParameterHandler)
                elif cat == '4':
                    oListItem = oGui.addSeason(site, function, title, 'series.png', '', title, oOutputParameterHandler)
                elif cat == '5':
                    oListItem = oGui.addMisc(site, function, title, 'buzz.png', '', title, oOutputParameterHandler)
                else:
                    oListItem = oGui.addTV(site, function, title, 'series.png', '', title, oOutputParameterHandler)

                oOutputParameterHandler.addParameter('sTitleWatched', sTitleWatched)
                oOutputParameterHandler.addParameter('sCat', cat)
                oListItem.addMenu(SITE_IDENTIFIER, 'delViewing', self.ADDON.VSlang(30412), oOutputParameterHandler)

            except Exception as e:
                oGui.addText(SITE_IDENTIFIER, 'Error: ' + str(e))

        # Vider toute la catégorie n'est pas accessible lors de l'utilisation en Widget
        if not xbmc.getCondVisibility('Window.IsActive(home)'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sCat', catFilter)
            oGui.addDir(SITE_IDENTIFIER, 'delViewing', self.ADDON.VSlang(30211), 'trash.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()
