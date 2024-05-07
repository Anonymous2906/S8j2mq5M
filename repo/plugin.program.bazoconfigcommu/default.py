# Module: default
# Author: Bazo, Osmoze06
# Created on: 19.01.2022
# Edited on: 17.03.2024

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
import urllib.request
import subprocess

artworkPath = xbmcvfs.translatePath('special://home/addons/plugin.program.bazoconfigcommu/resources/media/')
fanart = artworkPath + "fanart.jpg"

def notice(content):
    log(content, xbmc.LOGINFO)

def log(msg, level=xbmc.LOGINFO):
    addon = xbmcaddon.Addon()
    addonID = addon.getAddonInfo('id')
    xbmc.log('%s: %s' % (addonID, msg), level)

def showErrorNotification(message):
    xbmcgui.Dialog().notification("BAZOLAND", message,
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

############################################## LISTE DES MENUS ###############################################
def main_menu():
    xbmcplugin.setPluginCategory(__handle__, "Choix bazo")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("Installation - Modifier les options", 'modif_option', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)
    
###############################################
def modif_option():
    #Menu Principal
    xbmcplugin.setPluginCategory(__handle__, "MENU PRINCIPAL")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1. Entrer code unique[/B]", 'pbazo', artworkPath +'Logo Codes.png')
    add_dir("[B]2. Import/Gestion  codes secondaires[/B]", 'cuu', artworkPath +'Logo Codes.png')
    add_dir("[B]3. Référenciels :[/B] Installation des Depôts nécessaires", 'repo', artworkPath + 'Logo Dépot.png')
    add_dir("[B]4. U2Pplay :[/B] Installation / Paramétrage", 'men_ext', artworkPath + 'Logo Installer.png')
    add_dir("[B]5. VStream :[/B] Installation / Paramétrage", 'vodt', artworkPath + 'Logo Installer.png')
    add_dir("[B]6. TV & Replay :[/B] Installation / Paramétrage", 'men_pvr', artworkPath + 'Logo TV.png')
    add_dir("[B]7. Menu IPTV :[/B] Mode Stalker & Xtream", 'men_iptv', artworkPath + 'Logo IPTV.png')
    add_dir("[B]8. Menu Skins :[/B] Base de données de Skin", 'men_skin', artworkPath + 'Logo Skin.png')
    add_dir("[B] Activer le stop avec retour[/B]", 'sr', artworkPath + 'Logo Installer.png')
    add_dir("[COLOR red]Nettoyer KODI[/COLOR]", 'vider_cache', artworkPath + 'Logo Supprimer.png')
    add_dir("Vider cache vst ", 'cache_vst', artworkPath + 'Logo Supprimer.png')
    add_dir ("Gestion backup", 'gb', artworkPath + 'Logo Gérer.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

###############################################
def gb():
    #Menu Profil & Sous-Menus
    add_dir("Profil bazoland", 'cpb', artworkPath + 'Logo Créer.png')
    add_dir("Gestion favoris", "fav", artworkPath + 'Logo Gérer.png')
    add_dir("Gestion config", "gconf", artworkPath + 'Logo Gérer.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)
    
def gconf():
    add_dir("Sauvegarder config", 'sav_serv', artworkPath + 'Logo Sauver.png')
    add_dir("Restaurer config", 'res_serv', artworkPath + 'Logo Restaurer.png')
    add_dir("Suprimer addon data avant restauration backup", 'sad', artworkPath + 'Logo Supprimer.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)
    
def fav():
    add_dir("Sauvgarder fav vst", "fav_sync", artworkPath + 'Logo Sauver.png')
    add_dir("Restaurer fav vst", "sfav", artworkPath + 'Logo Restaurer.png')
    add_dir("Sauvegarder fav catchup", "fav_cat", artworkPath + 'Logo Sauver.png')
    add_dir("restaurer fav catchup", "r_fav_cat", artworkPath + 'Logo Restaurer.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

###############################################
def men_ext():
    #Menu U2Pplay
    xbmcplugin.setPluginCategory(__handle__, "MENU U2PPLAY")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]0.[/B] J ai kodi 21 donc je clique ici", 'kodi21', artworkPath + 'icone.png')
    add_dir("[B]1.[/B] Installation de U2Pplay", 'addons', artworkPath + 'Logo Installer.png')
    add_dir("[B]2.[/B] Import du Paramétrage", 'alloptions', artworkPath + 'Logo Importer.png')
    add_dir("[B]3.[/B] Installer ou Mettre à jour le Backup DB", 'back_db', artworkPath +'Logo Importer.png')
    add_dir("[B]4.[/B] Construire ou Mettre à jour la DB", 'const_db', artworkPath +'Logo Importer.png')
    add_dir("[B]5.[/B] Installer le Service de Mise à Jour Automatique", 'serv_maj', artworkPath + 'Logo Installer.png')
    add_dir("[B]6.[/B] Installer UPNext (Enchaînement auto. des épisodes)", 'upnext', artworkPath + 'Logo installer.png')
    add_dir("Ouvrir les Paramètres de U2Pplay", 'ref_import', artworkPath + 'Logo Parametres.png')
    add_dir("[COLOR red]Effacer la DB[/COLOR]", 'del_db', artworkPath +'Logo Suppression.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

###############################################
def vodt():
    #Menu VStream
    xbmcplugin.setPluginCategory(__handle__, "MENU VSTREAM")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1.[/B] Installation de VStream", 'addons2', artworkPath + 'Logo Installer.png')
    add_dir("[B]2.[/B] Télécharger le Paramétrage",'mv', artworkPath + 'Logo Importer.png')
    add_dir("[B]3.[/B] Importer le Paramétrage", 'mv1', artworkPath + 'Logo Importer.png')
    add_dir("[B]4.[/B] Installer la DB Torrent", 'dbt', artworkPath + 'Logo Importer.png')
    add_dir("Ouvrir les Paramètres de VStream", 'pv', artworkPath + 'Logo Parametres.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

###############################################
def men_pvr():
    #Menu TV PVR
    xbmcplugin.setPluginCategory(__handle__, "MENU TV PVR & REPLAY TV")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1.[/B] Installation du PVR Simple Client", 'pvr', artworkPath + 'Logo Installer.png')
    add_dir("[B]2.[/B] Installation de VAVOOTO",'vavooto', artworkPath + 'Logo Installer.png')
    add_dir("[B]3.[/B] Liste TV M3U de VAVOOTO",'vavoopvr', artworkPath + 'Logo Importer.png')
    add_dir("[B]4.[/B] Liste TV M3U de FOXX",'foxxpvr', artworkPath + 'Logo Importer.png')    
    add_dir("[B]5.[/B] Installation de Catchup TV & More",'catchuptv', artworkPath + 'Logo Installer.png') 
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

###############################################
def men_skin():
    #Menu Skins
    xbmcplugin.setPluginCategory(__handle__, "menu pour les skins")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]Skin bazoluc[/B] - skin hk3 avec iptv ou juste iptv", 'men_skin_bazoluc', artworkPath + 'Logo Bazo-Luc.png')
    add_dir("[B]Skin bazoland[/B] - HK3 + vst + iptv", 'men_skin_bazoland', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)


def men_skin_bazoluc():
      #Menu Skins
    xbmcplugin.setPluginCategory(__handle__, "menu pour les skins")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("Mettre à jour les icônes", 'au_maj', artworkPath + 'Logo Importer.png')
    add_dir("[B]AutoWidget :[/B] Installer l'addon", 'autowidget', artworkPath + 'Logo Installer.png')
    add_dir("[B]Estuary v2[/B] - IPTV - by Bazo & Luc", 'dl_skin', artworkPath + 'Logo Estuary V2.png')
    add_dir("[B]Estuary v2[/B] - HK3 - by Bazo & Luc", 'dl_skin2', artworkPath + 'Logo Estuary V2.png')
    add_dir("[B]Estuary v2[/B] - HK3 Light - by Bazo & Luc", 'dl_skin3', artworkPath + 'Logo Estuary V2.png')
    add_dir("[B]Arctic Horizon 2[/B] - IPTV - by Bazo & Luc", 'dl_skin6', artworkPath + 'Logo AH 2.png')
    add_dir("[B]Arctic Horizon 2[/B] - HK3 - by Bazo & Luc", 'dl_skin5', artworkPath + 'Logo AH 2.png')
    add_dir("[B]Arctic Horizon 2[/B] - HK3 Light - by Bazo & Luc", 'dl_skin4', artworkPath + 'Logo AH 2.png')
    add_dir("[B]Detruire les icons et autowidget pour une mise a jour[/B]", 'del_icon_aw', artworkPath + 'Logo Supprimer.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

def men_skin_bazoland():
      #Menu Skins
    xbmcplugin.setPluginCategory(__handle__, "menu pour les skins")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("Mettre à jour les icônes", 'au_maj', artworkPath + 'Logo Importer.png')
    add_dir("[B]AutoWidget :[/B] Installer l'addon", 'autowidget', artworkPath + 'Logo Installer.png')
    add_dir("[B]Arctic Horizon 2[/B] - BazoLand", 'dl_skin7', artworkPath + 'Logo AH 2.png')
    add_dir("[B]Estuary v2 [/B] - Bazoland", 'dl_skin8', artworkPath + 'Logo Estuary V2.png')
    add_dir("[B]Detruire les icons et autowidget pour une mise a jour[/B]", 'del_icon_aw', artworkPath + 'Logo Supprimer.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)
###############################################

def men_iptv():
     #Menu
    xbmcplugin.setPluginCategory(__handle__, "MENU IPTV")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1.[/B] Mode [B]STALKER[/B]", 'men_iptv_stalker', artworkPath + 'Logo Stalker.png')
    add_dir("[B]2.[/B] Mode [B]XTREAM[/B]", 'men_iptv_xtream', artworkPath + 'Logo Xtream.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

###############################################

def men_iptv_stalker():
     #Menu
    xbmcplugin.setPluginCategory(__handle__, "MENU IPTV STALKER")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1.[/B] Ajouter un Compte unique ou une Bank", 'iptv_tobal', artworkPath + 'Logo Importer.png')
    add_dir("[B]2.[/B] Sélectionner une Adresse MAC", 'iptv_tobal2', artworkPath + 'Logo Importer.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

################################################

def men_iptv_xtream():
     #Menu
    xbmcplugin.setPluginCategory(__handle__, "MENU IPTV XTREAM")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1.[/B]Ajouter le compte - Fournisseur 1", 'iptv_xt1', artworkPath + 'Logo Importer.png')
    add_dir("[B]2.[/B]Ajouter le compte - Fournisseur 2", 'iptv_xt2', artworkPath + 'Logo Importer.png')
    add_dir("[B]3.[/B]Ajouter le compte - Fournisseur 3", 'iptv_xt3', artworkPath + 'logo Importer.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

############################################## FIN LISTE DES MENUS ###############################################
def fav_auto_sav():
    import sav_auto_fav
    sav_auto_fav.sav_auto()
def sfav():
    import rfav
def cpfav():
    import cree_pfav
def fav_cat():
    import fav_catchup
def r_fav_cat():
    import r_fav_catchup
def fav_sync():
    import fav
def sad():
    import sup_addon_data
def res_serv():
    import test_r
def sav_serv():

    import test
def cpb():
    import crea_compte
def sr():
    settings_download2 = 'http://tobal.duckdns.org:805/api/public/dl/qoDhshil/kodi/bazoconfig/stopretour/keyboard.xml'
    settings_loc2 = xbmcvfs.translatePath('special://home/userdata/keymaps/keyboard.xml')
    urllib.request.urlretrieve(settings_download2, settings_loc2)
    xbmc.executebuiltin("Notification(INSTALLATION, Téléchargements terminés)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('Quit')

def cache_vst():
    xbmc.executebuiltin('RunScript(plugin.video.vstream, addon, ?site=globalRun&amp;function=addon)')

def pbazo():
    addon_id = "plugin.program.bazoconfigcommu"
    addons = xbmcaddon.Addon(addon_id)
    xbmcaddon.Addon(addon_id).openSettings()

def kodi21():
    import kodi21

def repo():
    #Installation de tous les référentiels nécéssaires
    import install_repositories

##############################################

def addons():
    #Installation de l'addon U2Pplay (Script Externe)
    import install_u2p

##############################################

def addons2():
    #Installation de l'addon VStream (Script Externe)
    import install_vstream

##############################################    

def pvr():
    #Installation de l'addon PVR Simple Client (Script Externe)
    import install_pvr

##############################################  

def vavooto():
    #Installation de l'addon Vavooto (Script Externe)
    import install_vavoo

##############################################  

def vavoopvr():
    #Installation de la liste m3u Vavooto (Script Externe)
    import vavoopvr
    vavoopvr.dl()
    
##############################################  

def foxxpvr():
    #Installation de la liste m3u FOXX (Script Externe)
    import foxxpvr
    foxxpvr.dl()
    
##############################################  

def catchuptv():
    #Installation de l'addon Catchup TV & More beta (Script Externe)
    import install_catchuptv

##############################################    

def upnext():
    #Installation de l'addon UPNext (Script Externe)
    import install_upnext

##############################################

def autowidget():
    #Installation de l'addon AutoWidget (Script Externe)
    import install_autowidget

##############################################

import xbmcaddon
import requests
import re

def cuu():
    import codeunique

    # Appeler la fonction code() de codeunique.py
    codeunique.code()


def au_maj():
    #Installation des Icônes
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
    xbmc.executebuiltin("Notification(EXTRACTION OK, icons installés)")
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
    import estuary_iptv

##############################################
    
def dl_skin2():
    import estuary_hk3

##############################################

def dl_skin3():
    import estuary_hk3_light

##############################################

def dl_skin4():
    import ah2_hk3_light
##############################################

def dl_skin5():
    import ah2_hk3

##############################################

def dl_skin6():
   import ah2_foxx

##############################################

def dl_skin7():
   import bazoland


def dl_skin8():
    import bazoland2

##############################################

def dbt():
    import dbt
    dbt.code()
def dbt2():
    import dbbazoland
    dbbazoland.code()
##############################################

def pv():
    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.vstream/?function=opensetting&sFav=opensetting&site=cHome&siteUrl=http%3a%2f%2fvenom&title=Ouvrir%20les%20param%c3%a8tres)')

##############################################

def mv():
    import config_vst
    # Appeler la fonction code() de config_hk3.py
    config_vst.dl()
def mv1():
    import config_vst2
    config_vst2.code()


##############################################

def back_db():
    # installer le skin cosmic bazoluc iptv
    # telechargement et extraction du zip
    #xbmc.sleep(5000)
    #zipurl = 'http://tobal.duckdns.org:805/api/public/dl/bDj_Ruq9/kodi/bazoconfig/backup_db/mediasNewSauve.bd.zip'
    #xbmc.sleep(5000)
    #with urlopen(zipurl) as zipresp:
        #with ZipFile(BytesIO(zipresp.read())) as zfile:
            #zfile.extractall(xbmcvfs.translatePath('special://home/userdata/addon_data/plugin.video.sendtokodiU2P'))
    #xbmc.executebuiltin( 'RunPlugin(plugin://plugin.video.sendtokodiU2P/?action=gestiondb)')
    #showInfoNotification("db telechargé cliquez sur restauration")
    import back_db
    
###############################################

def serv_maj():
    #import install_servicemaj
    xbmc.sleep(1000)
    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.sendtokodiU2P/?action=mepautostart2)')
    showInfoNotification("maj auto activé")

###############################################

def const_db ():
    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.sendtokodiU2P/?action=loadhk3v)')

###############################################

def del_db():
    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.sendtokodiU2P/?action=resetBDhkNew)')
    
################################################
def iptv_tobal():
       xbmc.sleep(2000)
       addon = xbmcaddon.Addon("plugin.video.sendtokodiU2P")
       iptv = "true"
       addon.setSetting(id="iptv", value=iptv)
       xbmc.sleep(2000)
       xbmc.executebuiltin('RunPlugin(plugin://plugin.video.sendtokodiU2P/?action=ajoutIPTV&reload=$INFO[Window(Home).Property(widgetreload)]$INFO[Window(Home).Property(widgetreload2')

###############################################

def iptv_tobal2():
       xbmc.sleep(2000)
       xbmc.executebuiltin('RunPlugin(plugin://plugin.video.sendtokodiU2P/?action=IPTVbank&reload=$INFO[Window(Home).Property(widgetreload)]$INFO[Window(Home).Property(widgetreload2)')

###############################################

def alloptions():
    import config_hk3

    # Appeler la fonction code() de config_hk3.py
    config_hk3.code()

###############################################

def iptv_xt1():
    import iptvx1
    iptvx1.code()

###############################################

def iptv_xt2():
   import iptvx2
   iptvx2.code()

###############################################

def iptv_xt3():
    import iptvx3
    iptvx3.code()

###############################################

def anote():
    numAnotepad0 = __addon__.getSetting("numAnotepad0")
    url = f"https://anotepad.com/note/read/{numAnotepad0.strip()}"

    try:
        rec = requests.get(url, verify=False)
        match = re.search(r'<\s*div\s*class\s*=\s*"\s*plaintext\s*"\s*>(?P<txAnote>.+?)</div>', rec.text, re.MULTILINE | re.DOTALL)
        if match:
            key_alldebrid = match.group("txAnote").strip()
            return key_alldebrid
        else:
            showInfoNotification("Échec de la correspondance du motif pour le contenu Anotepad")
            return None
    except Exception as e:
        showInfoNotification("Erreur lors de l'extraction du contenu Anotepad : " + str(e))
        return None

###############################################


###############################################

###############################################

def ref_import():
    # refaire l'immport
    # reset database
    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.sendtokodiU2P/?action=setting)')

###############################################

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

def del_icon_aw():
    # Nettoyer tout
    xbmc.executebuiltin("Notification(ICON, Effacement en cours...)")

    # Suppression du dossier temporaire
    dirPath = xbmcvfs.translatePath('special://home/userdata/addon_data/iconvod')
    try:
        shutil.rmtree(dirPath)
    except Exception as e:
        print('Erreur lors de la suppression du répertoire :', e)

    xbmc.sleep(1000)
    xbmc.executebuiltin('RunPlugin(plugin://plugin.program.autowidget/?mode=wipe&refresh=&reload)')
    xbmc.sleep(1000)
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
        'dl_skin4':(dl_skin4, ""),
        'dl_skin5':(dl_skin5, ""),
        'dl_skin6':(dl_skin6, ""),
        'repo': (repo, ""),
        'addons': (addons, ""),
        'addons2': (addons2, ""),
        'men_iptv': (men_iptv, ""),
        'men_pvr': (men_pvr, ""),        
        'pvr': (pvr, ""),
        'vavooto': (vavooto, ""),
        'vavoopvr': (vavoopvr, ""),
        'foxxpvr': (foxxpvr, ""),        
        'catchuptv': (catchuptv, ""),
        'upnext': (upnext, ""),        
        'autowidget': (autowidget, ""), 
        'iptv_tobal': (iptv_tobal, ""),
        'iptv_tobal2': (iptv_tobal2, ""),
        'back_db': (back_db, ""),
        'serv_maj': (serv_maj, ""),
        'anote': (anote, ""),
        'const_db': (const_db,""),
        'del_db': (del_db, ""),
        'men_iptv_stalker': (men_iptv_stalker, ""),
        'men_iptv_xtream': (men_iptv_xtream,""),
        'iptv_xt1': (iptv_xt1, ""),
        #'iptvx1': (iptvx1, ""),
       # 'iptvx2': (iptvx2, ""),
        'iptv_xt2': (iptv_xt2, ""),
        'iptv_xt3': (iptv_xt3, ""),
        'vodt': (vodt, ""),
        'pv': (pv, ""),
        'mv': (mv,""),
       # 'vm': (vm, ""),
        'dbt': (dbt, ""),
        #'dbtd': (dbtd, ""),
        'dl_skin7': (dl_skin7, ""),
        'cuu': (cuu, ""),
        #'cuuu': (cuuu,""),
        'pbazo': (pbazo,""),
        'dl_skin8': (dl_skin8, ""),
        'sr': (sr, ""),
        'del_icon_aw': (del_icon_aw, ""),
        'cache_vst': (cache_vst, ""),
        'mv1': (mv1,""),
        'men_skin_bazoluc': (men_skin_bazoluc, ""),
        'men_skin_bazoland': (men_skin_bazoland, ""),
        'kodi21': (kodi21, ""),
        'sav_serv': (sav_serv, ""),
        'res_serv': (res_serv, ""),
        'cpb': (cpb, ""),
        'sad': (sad, ""),
        'gb': (gb, ""),
        'fav_sync': (fav_sync, ""),
        'cpfav': (cpfav, ""),
        'sfav': (sfav, ""),
        'fav': (fav, ""),
        'gconf': (gconf, ""),
        'dbt2': (dbt2, ""),
        'fav_auto_sav': (fav_auto_sav, ""),
        'fav_cat': (fav_cat, ""),
        'r_fav_cat': (r_fav_cat, ""),
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
