# Module: default
# Author: bazo
# Created on: 19.01.2022
import xbmcplugin
from urllib.parse import quote_plus, unquote_plus, parse_qsl
import xbmc
import xbmcvfs
import xbmcaddon
import xbmcgui
import xbmcplugin
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import os
import shutil
import requests
import random
import re

artworkPath = xbmcvfs.translatePath('special://home/addons/plugin.program.bazoconfigcommu/resources/media/')
fanart = artworkPath + "fanart.jpg"

def notice(content):
    log(content, xbmc.LOGINFO)

def log(msg, level=xbmc.LOGINFO):
    addon = xbmcaddon.Addon()
    addonID = addon.getAddonInfo('id')
    xbmc.log('%s: %s' % (addonID, msg), level)

def showErrorNotification(message):
    xbmcgui.Dialog().notification("bazo skin", message,
                                  xbmcgui.NOTIFICATION_ERROR, 5000)
def showInfoNotification(message):
    xbmcgui.Dialog().notification("bazo skin", message, xbmcgui.NOTIFICATION_INFO, 15000)

def add_dir(name, mode, thumb):
    u = sys.argv[0] + "?" + "action=" + str(mode)
    liz = xbmcgui.ListItem(name)
    liz.setArt({'icon': thumb})
    liz.setProperty("fanart_image", fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

##############################################

# MENU PRINCIPAL
def main_menu():
    xbmcplugin.setPluginCategory(__handle__, "Choix bazo")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("Installation - Modifier les options", 'modif_option', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)
##############################################

def repo():
    # mise a jour icone aura
    # telechargement et extraction du zip
    zipurl = 'http://tobal.duckdns.org:805/api/public/dl/zNsnbCN5/kodi/bazoconfig/repo/repo.zip'
    xbmc.sleep(5000)
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmcvfs.translatePath('special://home/temp/temp/repo'))
    # copie des fichiers extraie
    source_dir = xbmcvfs.translatePath('special://home/temp/temp/repo')
    destination_dir = xbmcvfs.translatePath('special://home/addons')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(EXTRACTION OK, repos instalé)")
    xbmc.sleep(5000)
    xbmc.executebuiltin("Notification(FICHIER TEMP,Effacement en cours...)")
    # suppression dossier temporaire
    dirPath = xbmcvfs.translatePath('special://home/temp/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Notification(TERMINE , ...)")
    xbmc.executebuiltin("Notification(ATTENTION KODI VA SE FERMER , retour au menu principal et relancez kodi)")
    xbmc.sleep(2000)
   # xbmc.executebuiltin('ReloadSkin')
    xbmc.sleep(2000)
    xbmc.executebuiltin('Quit')

def repo2():
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.autowidget", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repo.S8j2mq5M", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.kodinerds", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "service.upnext", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "script.skinhelper", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "plugin.program.super.favourites", "enabled": true }}')
    xbmc.sleep(5000)
    xbmc.executebuiltin("Notification(ADDON , activer)")
    
##############################################

##############################################

##############################################

# INSTALLER LES ICONES
def au_maj():
    # mise a jour icone aura
    # telechargement et extraction du zip
    xbmc.sleep(5000)
    zipurl = 'http://tobal.duckdns.org:805/api/public/dl/42iiVP9Z/kodi/bazoconfig/icon/icon.zip'
    xbmc.sleep(5000)
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmcvfs.translatePath('special://home/temp/temp/addon_data/iconvod'))
 # copie des fichiers extraie
    source_dir = xbmcvfs.translatePath('special://home/temp/temp/addon_data/iconvod')
    destination_dir = xbmcvfs.translatePath('special://home/userdata/addon_data/')
    #source_dir2 = xbmcvfs.translatePath('special://home/temp/temp/addons')
    #destination_dir2 = xbmcvfs.translatePath('special://home/addons')
    #source_dir3 = xbmcvfs.translatePath('special://home/temp/temp/keymaps')
    #destination_dir3 = xbmcvfs.translatePath('special://masterprofile/keymaps')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    #shutil.copytree(source_dir2, destination_dir2, dirs_exist_ok=True)
    #shuexecutebuiltintil.copytree(source_dir3, destination_dir3, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(EXTRACTION OK, icons instalé)")
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(FICHIER TEMP,Effacement en cours...)")
    # suppression dossier temporaire
    dirPath = xbmcvfs.translatePath('special://home/temp/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Notification(TERMINE , ...)")

##############################################

# INSTALLER LE SKIN estuarry v2 bazoluc
def dl_skin():
    # installer le skin cosmic bazoluc iptv
    # telechargement et extraction du zip
    xbmc.sleep(5000)
    zipurl = 'http://tobal.duckdns.org:805/api/public/dl/sfv-6Eg6/kodi/bazoconfig/add/add.zip'
    xbmc.sleep(5000)
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmcvfs.translatePath('special://home/userdata/addon_data'))
 # copie des fichiers extraie
    #source_dir = xbmcvfs.translatePath('special://home/temp/temp/addon_data')
    #destination_dir = xbmcvfs.translatePath('special://home/userdata/addon_data')
    #source_dir2 = xbmcvfs.translatePath('special://home/temp/temp/addons')
    #destination_dir2 = xbmcvfs.translatePath('special://home/addons')
    #source_dir3 = xbmcvfs.translatePath('special://home/temp/temp/keymaps')
    #destination_dir3 = xbmcvfs.translatePath('special://masterprofile/keymaps')
    #shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    #shutil.copytree(source_dir2, destination_dir2, dirs_exist_ok=True)
    #shutil.copytree(source_dir3, destination_dir3, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(EXTRACTION OK, skin instalé)")
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(FICHIER TEMP,Effacement en cours...)")
    # suppression dossier temporaire
    dirPath = xbmcvfs.translatePath('special://home/temp/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Notification(TERMINE , ...)")
    
def dl_skin2():
    # installer le skin estuary v2 bazoluc
    # telechargement et extraction du zip
    zipurl = 'http://tobal.duckdns.org:805/api/public/dl/AWs5w6HT/kodi/bazoconfig/add/hk3-estuary.zip'
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmcvfs.translatePath('special://home/userdata/addon_data'))
 # copie des fichiers extraie
    #source_dir = xbmcvfs.translatePath('special://home/temp/temp/addon_data')
    #destination_dir = xbmcvfs.translatePath('special://home/userdata/addon_data')
    #source_dir2 = xbmcvfs.translatePath('special://home/temp/temp/addons')
    #destination_dir2 = xbmcvfs.translatePath('special://home/addons')
    #source_dir3 = xbmcvfs.translatePath('special://home/temp/temp/keymaps')
    #destination_dir3 = xbmcvfs.translatePath('special://masterprofile/keymaps')
    #shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    #shutil.copytree(source_dir2, destination_dir2, dirs_exist_ok=True)
    #shutil.copytree(source_dir3, destination_dir3, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(EXTRACTION OK, skin instalé)")
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(FICHIER TEMP,Effacement en cours...)")
    # suppression dossier temporaire
    dirPath = xbmcvfs.translatePath('special://home/temp/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Notification(TERMINE , ...)")


def dl_skin3():
    # installer le skin estuary v2 bazoluc
    # telechargement et extraction du zip
    zipurl = 'http://tobal.duckdns.org:805/api/public/dl/ykHRZ8Y1/kodi/bazoconfig/add/hk3-cosmic.zip'
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmcvfs.translatePath('special://home/userdata/addon_data'))
 # copie des fichiers extraie
    #source_dir = xbmcvfs.translatePath('special://home/temp/temp/addon_data')
    #destination_dir = xbmcvfs.translatePath('special://home/userdata/addon_data')
    #source_dir2 = xbmcvfs.translatePath('special://home/temp/temp/addons')
    #destination_dir2 = xbmcvfs.translatePath('special://home/addons')
    #source_dir3 = xbmcvfs.translatePath('special://home/temp/temp/keymaps')
    #destination_dir3 = xbmcvfs.translatePath('special://masterprofile/keymaps')
    #shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    #shutil.copytree(source_dir2, destination_dir2, dirs_exist_ok=True)
    #shutil.copytree(source_dir3, destination_dir3, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(EXTRACTION OK, skin instalé)")
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(FICHIER TEMP,Effacement en cours...)")
    # suppression dossier temporaire
    dirPath = xbmcvfs.translatePath('special://home/temp/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Notification(TERMINE , ...)")
##############################################
# MODIFIER LES OPTIONS
def modif_option():
    #Menu
    xbmcplugin.setPluginCategory(__handle__, "Modifier les options")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("1- extensions", 'men_ext', artworkPath + 'icone.png')
    add_dir("2- skins", 'men_skin', artworkPath + 'icone.png')
    add_dir("3- installer iptv", 'men_iptv', artworkPath + 'icone.png')
    add_dir("Ajouter Compte CatchupTv", 'ajout_cpt_ctv', artworkPath + 'icone.png')
    add_dir("Nettoyer Kodi", 'vider_cache', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

###############################################
def men_ext():
    #Menu
    xbmcplugin.setPluginCategory(__handle__, "menu pour les extensions")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("installer les depôts nécessaires", 'repo', artworkPath + 'icone.png')
    add_dir("activer les depôts", 'repo2', artworkPath + 'icone.png')
    add_dir("modifier options u2pplay", 'alloptions', artworkPath + 'icone.png')
    add_dir("installer/mise a jour backup db", 'back_db', artworkPath +'icone.png')
    add_dir("paramètres", 'ref_import', artworkPath + 'icone.png')
    add_dir("activer service maj", 'serv_maj', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)
###############################################
def men_skin():
    #Menu
    xbmcplugin.setPluginCategory(__handle__, "menu pour les skins")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("Mettre a jour les icones", 'au_maj', artworkPath + 'icone.png')
    add_dir("installer le skin bazo luc cosmic iptv (il faut installer depuis le repo de notre ami osmoze)", 'dl_skin', artworkPath + 'icone.png')
    add_dir("installer le skin bazo luc estuarry v2 hk3 (il faut installer depuis depot kodinerds)", 'dl_skin2', artworkPath + 'icone.png')
    add_dir("installer le skin bazo luc cosmic hk3 (il faut installer depuis le depot de notre ami osmomze)", 'dl_skin3', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)
###############################################
def back_db():
    # installer le skin cosmic bazoluc iptv
    # telechargement et extraction du zip
    xbmc.sleep(5000)
    zipurl = 'http://tobal.duckdns.org:805/api/public/dl/bDj_Ruq9/kodi/bazoconfig/backup_db/mediasNewSauve.bd.zip'
    xbmc.sleep(5000)
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmcvfs.translatePath('special://home/userdata/addon_data/plugin.video.sendtokodiU2P'))
    showInfoNotification("db telechargé pensez a restaurer dans parametres")
###############################################
def serv_maj():
    xbmc.sleep(1000)
    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.sendtokodiU2P/?action=mepautostart2)')
    showInfoNotification("maj auto activé")
###############################################
def men_iptv():
     #Menu
    xbmcplugin.setPluginCategory(__handle__, "menu pour les iptv")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("iptv etape 1", 'iptv_tobal', artworkPath + 'icone.png')
    add_dir("iptv etape 2", 'iptv_tobal2', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

def iptv_tobal():
       xbmc.sleep(2000)
       addon = xbmcaddon.Addon("plugin.video.sendtokodiU2P")
       iptv = "true"
       addon.setSetting(id="iptv", value=iptv)
       xbmc.sleep(2000)
       xbmc.executebuiltin('RunPlugin(plugin://plugin.video.sendtokodiU2P/?action=ajoutIPTV&reload=$INFO[Window(Home).Property(widgetreload)]$INFO[Window(Home).Property(widgetreload2')
def iptv_tobal2():
       xbmc.sleep(2000)
       xbmc.executebuiltin('RunPlugin(plugin://plugin.video.sendtokodiU2P/?action=IPTVbank&reload=$INFO[Window(Home).Property(widgetreload)]$INFO[Window(Home).Property(widgetreload2)')
def alloptions():
    addon = xbmcaddon.Addon("plugin.video.sendtokodiU2P")
    nb_items = "50"
    addon.setSetting(id="nb_items", value=nb_items)
    thumbnails = "3000"
    addon.setSetting(id="thumbnails", value=thumbnails)
    actifnewpaste = "true"
    addon.setSetting(id="actifnewpaste", value=actifnewpaste)
    heberg = "Rentry"
    addon.setSetting(id="heberg", value=heberg)
    numHeberg = "4vbug"
    addon.setSetting(id="numHeberg", value=numHeberg)
    intmaj = "15"
    addon.setSetting(id="intmaj", value=intmaj)
    delaimaj = "0"
    addon.setSetting(id="delaimaj", value=delaimaj)
    iptv = "true"
    addon.setSetting(id="iptv", value=iptv)
    showInfoNotification("Toutes les options activé")

def ref_import():
    # refaire l'immport
    # reset database
    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.sendtokodiU2P/?action=setting)')

# AJOUTER COMPTES CATCHUP TV
def ajout_cpt_ctv():
    addon = xbmcaddon.Addon("plugin.video.catchuptvandmore")
    mail = "rayflix@gmx.fr"
    mot2passe = "Mot2passe"
    addon.setSetting(id="nrj.login", value=mail)
    addon.setSetting(id="mytf1.login", value=mail)
    addon.setSetting(id="6play.login", value=mail)
    addon.setSetting(id="rmcbfmplay.login", value=mail)
    addon.setSetting(id="nrj.password", value=mot2passe)
    addon.setSetting(id="mytf1.password", value=mot2passe)
    addon.setSetting(id="6play.password", value=mot2passe)
    addon.setSetting(id="rmcbfmplay.password", value=mot2passe)

    showInfoNotification("Config Comptes ok")

##############################################

##############################################


##############################################

##############################################


    
def actuskin():
    # actualiser 
    xbmc.executebuiltin("Notification(actualisation OK,Faites retour !)")
    xbmc.sleep(1000)
    xbmc.executebuiltin('ReloadSkin')

##############################################

# MENU NETTOYAGE
def nettoye():
    xbm
    #menu nettoyage
    xbmcplugin.setPluginCadminategory(__handle__, "NETTOYER KODI")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR red]NETTOYER TadminOUT D'UN COUP : [/COLOR]clic ici", 'vider_cache', artworkPath + 'icone.png')
    add_dir("[COLOR deepskyblue]Vider Cache uniquement[/COLOR]", 'cache_seul', artworkPath + 'icone.png')
    add_dir("[COLOR deepskyblue]Vider Tmp uniquement[/COLOR]", 'tmp_seul', artworkPath + 'icone.png')
    add_dir("[COLOR deepskyblue]Vider Packages uniquement[/COLOR]", 'package_seul', artworkPath + 'icone.png')
    add_dir("[COLOR deepskyblue]Vider Thumbnails uniquement[/COLOR]", 'thumb_seul', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)  

##############################################

def vider_cache():
    #nettoyer tout
    xbmc.executebuiltin("Notification(FICHIER TEMP,Effacement en cours...)")
    # suppression dossier temporaire
    dirPath = xbmcvfs.translatePath('special://home/temp/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Notification(DOSSIER PACKAGES,Effacement en cours...)")
    # suppression dossier packages
    dirPath = xbmcvfs.translatePath('special://home/addons/packages/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Notification(DOSSIER THUMBNAILS,Effacement en cours...)")
    # suppression dossier thumbnails
    dirPath = xbmcvfs.translatePath('special://masterprofile/Thumbnails/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Notification(CACHE TEMP,Effacement en cours...)")
    # suppression dossier cache
    dirPath = xbmcvfs.translatePath('special://home/cache/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    # actualisation du skin
    xbmc.executebuiltin("Notification(ATTENTION KODI VA SE FERMER , Relancez le...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')
    xbmc.sleep(2000)
    xbmc.executebuiltin('Quit')
###########################

##############################################

# VIDER CACHE
def cache_seul():
    #nettoyaer cache uniquement
    xbmc.executebuiltin("Notification(CACHE TEMP,Effacement en cours...)")
    # suppression dossier cache
    dirPath = xbmcvfs.translatePath('special://home/cache/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    # actualisation du skin
    xbmc.executebuiltin("Notification(TERMINE , ...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')

#####################admin#############admin############

# VIDER TMP
def tmp_seul():
    #nettoyaer tmp uniquement
    xbmc.executebuiltin("Notification(FICHIER TEMP,Effacement en cours...)")
    # suppression dossier temporaire
    dirPath = xbmcvfs.translatePath('special://home/temp/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Notification(TERMINE , ...)")
    # actualisation du skin
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')

##############################################

# VIDER PACKAGES    
def package_seul():
    #nettoyaer packages uniquement
    xbmc.executebuiltin("Notification(DOSSIER PACKAGES,Effacement en cours...)")
    # suppression dosadminsier packages
    dirPath = xbmcvfs.translatePath('speciadminal://home/addons/packages/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    # actualisation du skin
    xbmc.executebuiltin("Notification(TERMINE , ...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')

##############################################

# VIDER THUMBNAILS
def thumb_seul():
    #nettoyaer thumbnails uniquement
    xbmc.executebuiltin("Notification(DOSSIER THUMBNAILS,Effacement en cours...)")
    # suppression dossier thumbnails
    dirPath = xbmcvfs.translatePath('special://masterprofile/Thumbnails/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    # actualisation du skin
    xbmc.executebuiltin("Notification(ATTENTION KODI VA SE FERMER , Relancez le...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')
    xbmc.sleep(2000)
    xbmc.executebuiltin('Quit')

##############################################

def router(paramstring):
    params = dict(parse_qsl(paramstring))    
    dictActions = {
        #key uptobox
        #'menuKey':(menuKey, ""),
        #menu option
        'men_ext':(men_ext, ""),
        'men_skin':(men_skin,""),
        'modif_option':(modif_option, ""),
        'alloptions':(alloptions, ""),
        'ajout_cpt_ctv': (ajout_cpt_ctv, ""),
        'ref_import': (ref_import, ""),
        #maj hk2
        "actuskin": (actuskin, ""),
        #nettoyage
        'vider_cache': (vider_cache, ""),
        'cache_seul': (cache_seul, ""),
        'tmp_seul': (tmp_seul, ""),
        'package_seul': (package_seul, ""),
        'thumb_seul': (thumb_seul, ""),
        'nettoye': (nettoye, ""),
        #autres
        #'ad_maj2': (ad_maj2, ""),
        'au_maj': (au_maj, ""),
        'dl_skin': (dl_skin, ""),
        'dl_skin2':(dl_skin2, ""),
        'dl_skin3':(dl_skin3, ""),
        'repo': (repo, ""),
        'repo2': (repo2, ""),
        'men_iptv': (men_iptv, ""),
        'iptv_tobal': (iptv_tobal, ""),
        'iptv_tobal2': (iptv_tobal2, ""),
        'back_db': (back_db, ""),
        'serv_maj': (serv_maj, ""),
        }
    if params:
        fn = params['action']
        if fn in dictActions.keys():
            argv = dictActions[fn][1]
            if argv:
                dictActions[fn][0](argv)
            else:
                dictActions[fn][0]()
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
         main_menu()

if __name__ == '__main__':
    __addon__ = xbmcaddon.Addon("plugin.program.bazoconfigcommu")
    __handle__ = int(sys.argv[1])
    router(sys.argv[2][1:])
