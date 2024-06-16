# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
import xbmc
import xbmcaddon
import requests
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import dialog, addon, isMatrix
from resources.lib.util import UnquotePlus

SITE_IDENTIFIER = 'cFav'
SITE_NAME = 'Fav'


class cFav:

    def __init__(self):
        self.addon = xbmcaddon.Addon("plugin.program.bazoconfigcommu")
        self.pseudo = self.addon.getSetting("pseudo")
        self.server = self.addon.getSetting("server")
        self.BASE_URL = f'{self.server}/profils/{self.pseudo}/requete.php'
        self.DIALOG = dialog()
        self.ADDON = addon()

    # Suppression d'un bookmark, d'une catégorie, ou tous les bookmarks
    def delBookmark(self):
        oInputParameterHandler = cInputParameterHandler()
        if not self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
            return False

        params = {
            'action': 'delBookmark',
            'siteurl': oInputParameterHandler.getValue('siteUrl'),
            'title': oInputParameterHandler.getValue('sCleanTitle'),
            'cat': oInputParameterHandler.getValue('sCat'),
            'all': oInputParameterHandler.exist('sAll')
        }
        response = requests.get(self.BASE_URL, params=params)
        return response.status_code == 200

    # Suppression d'un bookmark depuis un Widget
    def delBookmarkMenu(self):
        if not self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
            return False

        params = {
            'action': 'delBookmark',
            'siteurl': xbmc.getInfoLabel('ListItem.Property(siteUrl)'),
            'title': xbmc.getInfoLabel('ListItem.Property(sCleanTitle)')
        }
        response = requests.get(self.BASE_URL, params=params)
        return response.status_code == 200

    def getBookmarks(self):
        oGui = cGui()

        response = requests.get(self.BASE_URL, params={'action': 'getBookmarks'})
        if response.status_code != 200:
            oGui.setEndOfDirectory()
            return

        row = response.json()
        compt = [0] * 10
        for i in row:
            compt[int(i['cat'])] += 1

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '1')
        total = compt[1] + compt[7]
        oGui.addDir(SITE_IDENTIFIER, 'getFav', ('%s (%s)') % (self.ADDON.VSlang(30120), str(total)), 'mark.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '2')
        total = compt[2] + compt[3] + compt[4] + compt[8] + compt[9]
        oGui.addDir(SITE_IDENTIFIER, 'getFav', ('%s/%s (%s)') % (self.ADDON.VSlang(30121), self.ADDON.VSlang(30122), str(total)), 'mark.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '5')
        total = compt[5]
        oGui.addDir(SITE_IDENTIFIER, 'getFav', ('%s (%s)') % (self.ADDON.VSlang(30410), str(total)), 'mark.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '6')
        total = compt[6]
        oGui.addDir(SITE_IDENTIFIER, 'getFav', ('%s (%s)') % (self.ADDON.VSlang(30332), str(total)), 'mark.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sAll', 'true')
        oGui.addDir(SITE_IDENTIFIER, 'delBookmark', self.ADDON.VSlang(30209), 'trash.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def getFav(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        response = requests.get(self.BASE_URL, params={'action': 'getBookmarks'})
        if response.status_code != 200:
            oGui.setEndOfDirectory()
            return

        row = response.json()
        if oInputParameterHandler.exist('sCat'):
            sCat = oInputParameterHandler.getValue('sCat')

            catList = ('2', '3', '4', '8', '9')
            if sCat in catList:
                sCat = '2'
                cGui.CONTENT = 'tvshows'
            else:
                catList = ('1', '7')
                cGui.CONTENT = 'movies'
                if sCat in catList:
                    sCat = '1'
                else:
                    catList = sCat
                    cGui.CONTENT = 'videos'
            gen = (x for x in row if x['cat'] in catList)
        else:
            oGui.setEndOfDirectory()
            return

        for data in gen:
            try:
                title = data['title']
                thumbnail = data['icon']

                siteurl = data['siteurl']
                if isMatrix():
                    siteurl = UnquotePlus(siteurl)
                    title = str(title)

                site = data['site']
                function = data['fav']
                cat = data['cat']
                fanart = data['fanart']

                if thumbnail == '':
                    thumbnail = 'False'

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteurl)
                oOutputParameterHandler.addParameter('sMovieTitle', title)
                oOutputParameterHandler.addParameter('searchtext', title)
                oOutputParameterHandler.addParameter('sThumbnail', thumbnail)
                oOutputParameterHandler.addParameter('sThumb', thumbnail)

                if function == 'play':
                    oHoster = cHosterGui().checkHoster(siteurl)
                    oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
                    oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
                    oOutputParameterHandler.addParameter('sMediaUrl', siteurl)

                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(site)
                oGuiElement.setFunction(function)
                oGuiElement.setTitle(title)
                oGuiElement.setFileName(title)
                oGuiElement.setIcon("mark.png")
                if cat == '1':
                    oGuiElement.setMeta(1)
                    oGuiElement.setCat(1)
                elif cat == '2':
                    oGuiElement.setMeta(2)
                    oGuiElement.setCat(2)
                elif cat == '3':
                    oGuiElement.setMeta(4)
                    oGuiElement.setCat(3)
                elif cat == '4':
                    oGuiElement.setMeta(5)
                    oGuiElement.setCat(4)
                elif cat == '5':
                    oGuiElement.setMeta(0)
                    oGuiElement.setCat(5)
                elif cat == '6':
                    oGuiElement.setMeta(0)
                    oGuiElement.setCat(6)
                elif cat == '7':
                    oGuiElement.setMeta(3)
                    oGuiElement.setCat(7)
                elif cat == '8':
                    oGuiElement.setMeta(6)
                    oGuiElement.setCat(8)
                elif cat == '9':
                    oGuiElement.setMeta(2)
                    oGuiElement.setCat(9)
                else:
                    oGuiElement.setMeta(0)
                    oGuiElement.setCat(cat)
                oGuiElement.setThumbnail(thumbnail)
                oGuiElement.setFanart(fanart)
                oGuiElement.addItemProperties('isBookmark', True)

                oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cFav', 'cFav', 'delBookmark', self.ADDON.VSlang(30412))

                if function == 'play':
                    oGui.addHost(oGuiElement, oOutputParameterHandler)
                else:
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)

            except:
                oOutputParameterHandler = cOutputParameterHandler()
                oGui.addDir(SITE_IDENTIFIER, 'DoNothing', '[COLOR red]ERROR[/COLOR]', 'films.png', oOutputParameterHandler)

        if not xbmc.getCondVisibility('Window.IsActive(home)'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sCat', sCat)
            oGui.addDir(SITE_IDENTIFIER, 'delBookmark', self.ADDON.VSlang(30211), 'trash.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def setBookmark(self):
        oInputParameterHandler = cInputParameterHandler()

        sCat = oInputParameterHandler.getValue('sCat') if oInputParameterHandler.exist('sCat') else xbmc.getInfoLabel('ListItem.Property(sCat)')
        iCat = 0
        if sCat:
            iCat = int(sCat)
        if iCat < 1 or iCat > 9:
            self.DIALOG.VSinfo('Error', self.ADDON.VSlang(30038))
            return

        meta = {}

        sSiteUrl = oInputParameterHandler.getValue('siteUrl') if oInputParameterHandler.exist('siteUrl') else xbmc.getInfoLabel('ListItem.Property(siteUrl)')
        sTitle = oInputParameterHandler.getValue('sMovieTitle') if oInputParameterHandler.exist('sMovieTitle') else xbmc.getInfoLabel('ListItem.Property(sCleanTitle)')
        sSite = oInputParameterHandler.getValue('sId') if oInputParameterHandler.exist('sId') else xbmc.getInfoLabel('ListItem.Property(sId)')
        sFav = oInputParameterHandler.getValue('sFav') if oInputParameterHandler.exist('sFav') else xbmc.getInfoLabel('ListItem.Property(sFav)')

        if sTitle == '':
            self.DIALOG.VSinfo('Error', 'Probleme sur le titre')
            return

        meta['siteurl'] = sSiteUrl
        meta['title'] = sTitle
        meta['site'] = sSite
        meta['fav'] = sFav
        meta['cat'] = sCat
        meta['icon'] = xbmc.getInfoLabel('ListItem.Art(thumb)')
        meta['fanart'] = xbmc.getInfoLabel('ListItem.Art(fanart)')

        response = requests.post(self.BASE_URL, params={'action': 'insertBookmark'}, json=meta)
        if response.status_code == 200:
            self.DIALOG.VSinfo(self.ADDON.VSlang(30042), meta['title'], 4)
        else:
            self.DIALOG.VSinfo('Error', 'Insertion failed')