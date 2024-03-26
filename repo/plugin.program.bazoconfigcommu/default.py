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

def modif_option():
    #Menu Principal
    xbmcplugin.setPluginCategory(__handle__, "MENU PRINCIPAL")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1. Entrer code unique[/B]", 'pbazo', artworkPath +'icone.png')
    add_dir("[B]2. Import/Gestion  codes secondaires[/B]", 'cuu', artworkPath +'icone.png')
    add_dir("[B]3. Référenciels :[/B] Installation des Depôts nécéssaires", 'repo', artworkPath + 'icone.png')
    add_dir("[B]4. U2Pplay :[/B] Installation / Paramétrage", 'men_ext', artworkPath + 'icone.png')
    add_dir("[B]5. VStream :[/B] Installation / Paramétrage", 'vodt', artworkPath + 'icone.png')
    add_dir("[B]6. TV & Replay :[/B] Installation / Paramétrage", 'men_pvr', artworkPath + 'icone.png')
    add_dir("[B]7. Menu IPTV :[/B] Mode Stalker & Xtream", 'men_iptv', artworkPath + 'icone.png')
    add_dir("[B]8. Menu Skins :[/B] Base de données de Skin", 'men_skin', artworkPath + 'icone.png')
    add_dir("[B] Activer le stop avec retour[/B]", 'sr', artworkPath + 'icone.png')
    add_dir("[COLOR red]Nettoyer KODI[/COLOR]", 'vider_cache', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

###############################################
def men_ext():
    #Menu U2Pplay
    xbmcplugin.setPluginCategory(__handle__, "MENU U2PPLAY")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1.[/B] Installation de U2Pplay", 'addons', artworkPath + 'icone.png')
    add_dir("[B]2.[/B] Import du Paramétrage", 'alloptions', artworkPath + 'icone.png')
    add_dir("[B]3.[/B] Installer ou Mettre à jour le Backup DB", 'back_db', artworkPath +'icone.png')
    add_dir("[B]4.[/B] Construire ou Mettre à jour la DB", 'const_db', artworkPath +'icone.png')
    add_dir("[B]5.[/B] Installer le Service de Mise à Jour Automatique", 'serv_maj', artworkPath + 'icone.png')
    add_dir("[B]6.[/B] Installer UPNext (Enchaînement auto. des épisodes)", 'upnext', artworkPath + 'icone.png')
    add_dir("Ouvrir les Paramètres de U2Pplay", 'ref_import', artworkPath + 'icone.png')
    add_dir("[COLOR red]Effacer la DB[/COLOR]", 'del_db', artworkPath +'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

###############################################
def vodt():
    #Menu VStream
    xbmcplugin.setPluginCategory(__handle__, "MENU VSTREAM")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1.[/B] Installation de VStream", 'addons2', artworkPath + 'icone.png')    
    add_dir("[B]2.[/B] Importer le Paramétrage",'mv', artworkPath + 'icone.png')
    add_dir("[B]3.[/B] Installer la DB Torrent", 'dbt', artworkPath + 'icone.png')
    add_dir("Ouvrir les Paramètres de VStream", 'pv', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

###############################################
def men_pvr():
    #Menu TV PVR
    xbmcplugin.setPluginCategory(__handle__, "MENU TV PVR & REPLAY TV")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1.[/B] Installation du PVR Simple Client", 'pvr', artworkPath + 'icone.png')    
    add_dir("[B]2.[/B] Installation de VAVOOTO",'vavooto', artworkPath + 'icone.png')
    #add_dir("[B]3.[/B] Import du Paramétrage PVR + VAVOOTO", 'dbt', artworkPath + 'icone.png')
    add_dir("[B]3.[/B] Installation de Catchup TV & More",'catchuptv', artworkPath + 'icone.png')
    #add_dir("[B]5.[/B] Ajouter les Comptes Catchup TV & More", 'ajout_cpt_ctv', artworkPath + 'icone.png')    
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

###############################################
def men_skin():
    #Menu Skins
    xbmcplugin.setPluginCategory(__handle__, "menu pour les skins")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("Mettre à jour les icônes", 'au_maj', artworkPath + 'icone.png')
    add_dir("[B]AutoWidget :[/B] Installer l'addon", 'autowidget', artworkPath + 'icone.png')
    add_dir("[B]Estuary v2[/B] - IPTV - by Bazo & Luc", 'dl_skin', artworkPath + 'icone.png')
    add_dir("[B]Estuary v2[/B] - HK3 - by Bazo & Luc", 'dl_skin2', artworkPath + 'icone.png')
    add_dir("[B]Estuary v2[/B] - HK3 Light - by Bazo & Luc", 'dl_skin3', artworkPath + 'icone.png')
    add_dir("[B]Arctic Horizon 2[/B] - IPTV - by Bazo & Luc", 'dl_skin6', artworkPath + 'icone.png')
    add_dir("[B]Arctic Horizon 2[/B] - HK3 - by Bazo & Luc", 'dl_skin5', artworkPath + 'icone.png')
    add_dir("[B]Arctic Horizon 2[/B] - HK3 Light - by Bazo & Luc", 'dl_skin4', artworkPath + 'icone.png')
    add_dir("[B]Arctic Horizon 2[/B] - BazoLand", 'dl_skin7', artworkPath + 'icone.png')
    add_dir("[B]Estuary v2 [/B] - Bazoland", 'dl_skin8', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

###############################################

def men_iptv():
     #Menu
    xbmcplugin.setPluginCategory(__handle__, "MENU IPTV")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1.[/B] Mode [B]STALKER[/B]", 'men_iptv_stalker', artworkPath + 'icone.png')
    add_dir("[B]2.[/B] Mode [B]XTREAM[/B]", 'men_iptv_xtream', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

###############################################

def men_iptv_stalker():
     #Menu
    xbmcplugin.setPluginCategory(__handle__, "MENU IPTV STALKER")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1.[/B] Ajouter un Compte unique ou une Bank", 'iptv_tobal', artworkPath + 'icone.png')
    add_dir("[B]2.[/B] Sélectionner une Adresse MAC", 'iptv_tobal2', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

################################################

def men_iptv_xtream():
     #Menu
    xbmcplugin.setPluginCategory(__handle__, "MENU IPTV XTREAM")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1.[/B]Ajouter le compte - Fournisseur 1", 'iptv_xt1', artworkPath + 'icone.png')
    add_dir("[B]2.[/B]Ajouter le compte - Fournisseur 2", 'iptv_xt2', artworkPath + 'icone.png')
    add_dir("[B]3.[/B]Ajouter le compte - Fournisseur 3", 'iptv_xt3', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

############################################## FIN LISTE DES MENUS ###############################################

def sr():
    settings_download2 = 'http://tobal.duckdns.org:805/api/public/dl/qoDhshil/kodi/bazoconfig/stopretour/keyboard.xml'
    settings_loc2 = xbmcvfs.translatePath('special://home/userdata/keymaps/keyboard.xml')
    urllib.request.urlretrieve(settings_download2, settings_loc2)
    xbmc.executebuiltin("Notification(INSTALLATION, Téléchargements terminés)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('Quit')



def pbazo():
    addon_id = "plugin.program.bazoconfigcommu"
    addons = xbmcaddon.Addon(addon_id)
    xbmcaddon.Addon(addon_id).openSettings()


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

def cuu():
    settings_to_update = {
        'code_hk3': 'numAnotepad0',
        'code_config_vt': 'vm',
        'code_db_torrent': 'dbtd',
        'code_iptvx1': 'iptvx1',
        'code_iptvx2': 'iptvx2',
        'code_iptvx3': 'iptvx3',

    }

    key_alldebrid = cuuu()

    if key_alldebrid:
        key_values = key_alldebrid.split('\n')
        for key_value in key_values:
            key, value = key_value.split('=')
            key = key.strip().lower()
            value = value.strip()

            if key in settings_to_update:
                try:
                    addon = xbmcaddon.Addon("plugin.program.bazoconfigcommu")
                    addon.setSetting(id=settings_to_update[key], value=value)
                    showInfoNotification(f"{key.capitalize()} ajouté(e)")
                except Exception as e:
                    notice("Erreur HK: " + str(e))
            else:
                showInfoNotification(f"Clé inconnue : {key}")
    else:
        showInfoNotification("Aucune clé Anotepad trouvée")

def cuuu():
    numAnotepad0 = __addon__.getSetting("cu")
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

##############################################
    
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

##############################################

def dl_skin3():
    # installer le skin ???? v2 bazoluc
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

def dl_skin4():
    # installer le skin estuary v2 bazoluc
    # telechargement et extraction du zip
    zipurl = 'http://tobal.duckdns.org:805/api/public/dl/1aceP-y6/kodi/bazoconfig/add/hk3-ah2-light.zip'
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

def dl_skin5():
    # installer le skin estuary v2 bazoluc
    # telechargement et extraction du zip
    zipurl = 'http://tobal.duckdns.org:805/api/public/dl/5L6AgCaD/kodi/bazoconfig/add/hk3-ah2.zip'
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

def dl_skin6():
    # installer le skin estuary v2 bazoluc
    # telechargement et extraction du zip
    zipurl = 'http://tobal.duckdns.org:805/api/public/dl/xZ1i0UZB/kodi/bazoconfig/add/ah2-foxx.zip'
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

def dl_skin7():
    # installer le skin estuary v2 bazoluc
    # telechargement et extraction du zip
    zipurl = 'http://tobal.duckdns.org:805/api/public/dl/F5DZg7Ne/kodi/bazoconfig/add/bazoland.zip'
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


def dl_skin8():
    # installer le skin cosmic bazoluc iptv
    # telechargement et extraction du zip
    xbmc.sleep(5000)
    zipurl = 'http://tobal.duckdns.org:805/api/public/dl/Rf_0qxq-/kodi/bazoconfig/add/bazoland2.zip'
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

##############################################

def dbt():
    settings_to_update = {
        'dossier1': 'pastebin_label_1',
        'past1': 'pastebin_id_1',
        'dossier2': 'pastebin_label_2',
        'past2': 'pastebin_id_2',
        'dossier3': 'pastebin_label_3',
        'past3': 'pastebin_id_3',
        'dossier4': 'pastebin_label_4',
        'past4': 'pastebin_id_4',
        'dossier5': 'pastebin_label_5',
        'past5': 'pastebin_id_5',
        'dossier6': 'pastebin_label_6',
        'past6': 'pastebin_id_6',
        'dossier7': 'pastebin_label_7',
        'past7': 'pastebin_id_7',
    }

    key_alldebrid = dbtd()

    if key_alldebrid:
        key_values = key_alldebrid.split('\n')
        for key_value in key_values:
            key, value = key_value.split('=')
            key = key.strip().lower()
            value = value.strip()

            if key in settings_to_update:
                try:
                    addon = xbmcaddon.Addon("plugin.video.vstream")
                    addon.setSetting(id=settings_to_update[key], value=value)
                    showInfoNotification(f"{key.capitalize()} ajouté(e)")
                except Exception as e:
                    notice("Erreur : " + str(e))
            else:
                showInfoNotification(f"Clé inconnue : {key}")
    else:
        showInfoNotification("Aucune clé Anotepad trouvée")

def dbtd():
    dbtd = __addon__.getSetting("dbtd")
    url = f"https://anotepad.com/note/read/{dbtd.strip()}"

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

##############################################

def pv():
    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.vstream/?function=opensetting&sFav=opensetting&site=cHome&siteUrl=http%3a%2f%2fvenom&title=Ouvrir%20les%20param%c3%a8tres)')

##############################################

def mv():
    zipurl = 'http://tobal.duckdns.org:805/api/public/dl/Gj0ArcN9/kodi/bazoconfig/config_vstream/sites.zip'
    xbmc.sleep(5000)
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmcvfs.translatePath('special://home/temp/temp/repo'))
    # copie des fichiers extraie
    source_dir = xbmcvfs.translatePath('special://home/temp/temp/repo')
    destination_dir = xbmcvfs.translatePath('special://home/userdata/addon_data/plugin.video.vstream')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(EXTRACTION OK, source configurer)")
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
    xbmc.sleep(2000)
   # xbmc.executebuiltin('ReloadSkin')
    xbmc.sleep(2000)
    settings_to_update = {
        'hpast': 'pastebin_url',
        'aalldeb': 'hoster_alldebrid_premium',
        'talldeb': 'hoster_alldebrid_token',
    }

    key_alldebrid = vm()

    if key_alldebrid:
        key_values = key_alldebrid.split('\n')
        for key_value in key_values:
            key, value = key_value.split('=')
            key = key.strip().lower()
            value = value.strip()

            if key in settings_to_update:
                try:
                    addon = xbmcaddon.Addon("plugin.video.vstream")
                    addon.setSetting(id=settings_to_update[key], value=value)
                    showInfoNotification(f"{key.capitalize()} ajouté(e)")
                except Exception as e:
                    notice("Erreur HK: " + str(e))
            else:
                showInfoNotification(f"Clé inconnue : {key}")
    else:
        showInfoNotification("Aucune clé Anotepad trouvée")
    xbmc.executebuiltin("Notification(TERMINE , ...)")

def vm():
    vm = __addon__.getSetting("vm")
    url = f"https://anotepad.com/note/read/{vm.strip()}"

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
    settings_to_update = {
        'activer-hk3': 'actifnewpaste',
        'cle-alldeb': 'keyalldebrid',
        'dbrentry': 'numHeberg',
        'linkdatabase': 'numdatabase',
        'maj-hk': 'intmaj',
        'delai-majhk': 'delaimaj',
        'activer-bookmark': 'bookonline',
        'bookmark-online': 'bookonline_name',
        'activer-trakt': 'traktperso',
        'compte-trakt' : 'usertrakt',
        'bookmark-trakt': 'profiltrakt',
        'delai-maj': 'delaimaj'
    }

    key_alldebrid = anote()

    if key_alldebrid:
        key_values = key_alldebrid.split('\n')
        for key_value in key_values:
            key, value = key_value.split('=')
            key = key.strip().lower()
            value = value.strip()

            if key in settings_to_update:
                try:
                    addon = xbmcaddon.Addon("plugin.video.sendtokodiU2P")
                    addon.setSetting(id=settings_to_update[key], value=value)
                    showInfoNotification(f"{key.capitalize()} ajouté(e)")
                except Exception as e:
                    notice("Erreur HK: " + str(e))
            else:
                showInfoNotification(f"Clé inconnue : {key}")
    else:
        showInfoNotification("Aucune clé Anotepad trouvée")

###############################################

def iptv_xt1():
    settings_to_update = {
        'iptv': 'iptv',
        'adr_xt1': 'serverx1',
        'u_xt1': 'userx1',
        'p_xt1': 'passx1',
        'n_xt1': 'nomx1',
    }

    key_alldebrid = iptvx1()

    if key_alldebrid:
        key_values = key_alldebrid.split('\n')
        for key_value in key_values:
            key, value = key_value.split('=')
            key = key.strip().lower()
            value = value.strip()

            if key in settings_to_update:
                try:
                    addon = xbmcaddon.Addon("plugin.video.sendtokodiU2P")
                    addon.setSetting(id=settings_to_update[key], value=value)
                    showInfoNotification(f"{key.capitalize()} ajouté(e)")
                except Exception as e:
                    notice("Erreur HK: " + str(e))
            else:
                showInfoNotification(f"Clé inconnue : {key}")
    else:
        showInfoNotification("Aucune clé Anotepad trouvée")

###############################################

def iptv_xt2():
    settings_to_update = {
        'iptv': 'iptv',
        'adr_xt2': 'serverx1',
        'u_xt2': 'userx1',
        'p_xt2': 'passx1',
        'n_xt2': 'nomx1',
    }

    key_alldebrid = iptvx2()

    if key_alldebrid:
        key_values = key_alldebrid.split('\n')
        for key_value in key_values:
            key, value = key_value.split('=')
            key = key.strip().lower()
            value = value.strip()

            if key in settings_to_update:
                try:
                    addon = xbmcaddon.Addon("plugin.video.sendtokodiU2P")
                    addon.setSetting(id=settings_to_update[key], value=value)
                    showInfoNotification(f"{key.capitalize()} ajouté(e)")
                except Exception as e:
                    notice("Erreur HK: " + str(e))
            else:
                showInfoNotification(f"Clé inconnue : {key}")
    else:
        showInfoNotification("Aucune clé Anotepad trouvée")

###############################################

def iptv_xt3():
    settings_to_update = {
        'iptv': 'iptv',
        'adr_xt3': 'serverx1',
        'u_xt3': 'userx1',
        'p_xt3': 'passx1',
        'n_xt3': 'nomx1',
    }

    key_alldebrid = iptvx3()

    if key_alldebrid:
        key_values = key_alldebrid.split('\n')
        for key_value in key_values:
            key, value = key_value.split('=')
            key = key.strip().lower()
            value = value.strip()

            if key in settings_to_update:
                try:
                    addon = xbmcaddon.Addon("plugin.video.sendtokodiU2P")
                    addon.setSetting(id=settings_to_update[key], value=value)
                    showInfoNotification(f"{key.capitalize()} ajouté(e)")
                except Exception as e:
                    notice("Erreur HK: " + str(e))
            else:
                showInfoNotification(f"Clé inconnue : {key}")
    else:
        showInfoNotification("Aucune clé Anotepad trouvée")

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
def iptvx1():
    iptvx1 = __addon__.getSetting("iptvx1")
    url = f"https://anotepad.com/note/read/{iptvx1.strip()}"

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

def iptvx2():
    iptvx2 = __addon__.getSetting("iptvx2")
    url = f"https://anotepad.com/note/read/{iptvx2.strip()}"

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

def iptvx3():
    iptvx3 = __addon__.getSetting("iptvx3")
    url = f"https://anotepad.com/note/read/{iptvx3.strip()}"

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
        'pvr': (pvr, ""),
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
        'iptvx1': (iptvx1, ""),
        'iptvx2': (iptvx2, ""),
        'iptvx3': (iptvx3, ""),
        'iptv_xt2': (iptv_xt2, ""),
        'iptv_xt3': (iptv_xt3, ""),
        'vodt': (vodt, ""),
        'pv': (pv, ""),
        'mv': (mv,""),
        'vm': (vm, ""),
        'dbt': (dbt, ""),
        'dbtd': (dbtd, ""),
        'dl_skin7': (dl_skin7, ""),
        'cuu': (cuu, ""),
        'cuuu': (cuuu,""),
        'pbazo': (pbazo,""),
        'dl_skin8': (dl_skin8, ""),
        'sr': (sr, ""),

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
