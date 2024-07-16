# Module: default
# Author: Bazo, Osmoze06
# Created on: 19.01.2022
# Edited on: 25.05.2024

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

############################################## BOOKMARK ONLINE ###############################################

# Initialiser les paramètres de l'add-on
addon = xbmcaddon.Addon()

def cree_profil_bookmark():
    # Création du dossier profil pour le bookmark online (Script Externe)
    try:
        # Assurez-vous que le script externe est importé correctement
        import cree_profil_bookmark
        xbmcgui.Dialog().notification('SYNCHRONISATION', 'Bookmark en ligne actif', xbmcgui.NOTIFICATION_INFO, 5000)
        xbmc.log('Script executed successfully', level=xbmc.LOGINFO)
    except Exception as e:
        xbmcgui.Dialog().notification('Bookmark Sync', f'Failed to execute script: {str(e)}', xbmcgui.NOTIFICATION_ERROR, 5000)
        xbmc.log(f'Failed to execute script: {str(e)}', level=xbmc.LOGERROR)

def execute_script():
    # Récupérer la valeur de 'server_status'
    server_status = addon.getSettingBool('server_status')
    
    # Vérifier l'état de 'server_status' et exécuter le script si activé
    if server_status:
        cree_profil_bookmark()

# Appeler la fonction d'exécution du script au démarrage de l'add-on
execute_script()

############################################## FIN ###############################################


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

def add_dir(name, mode, thumb, description):
    u = sys.argv[0] + "?" + "action=" + str(mode)
    liz = xbmcgui.ListItem(name)
    liz.setArt({'icon': thumb})
    liz.setProperty("fanart_image", fanart)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})  # Ajout de la description
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

############################################## LISTE DES MENUS ###############################################
def main_menu():
    xbmcplugin.setPluginCategory(__handle__, "Choix Bazo")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("Installations & Modifications", 'modif_option', artworkPath + 'Logo Bazoland v2.png', "Menu principal de l'addon Bazoland.")
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)
    
###############################################
def modif_option():
    #Menu Principal
    xbmcplugin.setPluginCategory(__handle__, "Menu principal")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1. 1er Démarrage[/B]", 'pbazo', artworkPath +'Logo Codes.png', "Menu pour renseigner votre Code Unique, vos Codes Secondaires et de régler votre Profil Bazoland (Delai au démarrage, Intervalle de sauvegarde et le Service de Favoris).")
    add_dir("[B]2. Profil Bazoland[/B]", 'cpb', artworkPath + 'Logo Profil.png', "Permet de créer un profil sur le serveur (Uniquement pour la première configuration).")
    add_dir("[B]3. Codes Secondaires[/B]", 'cuu', artworkPath +'Logo Codes.png', "Permet d'importer et de gérer les Codes Secondaires afin de poursuivre la configuration.")
    add_dir("[B]4. Référentiels :[/B] Installation des Dépôts nécessaires", 'men_repos', artworkPath + 'Logo Dépot.png', "Permet d'installer tous les dépôts en une fois, pour le bon fonctionnement du service Bazoland.")
    add_dir("[B]5. U2Pplay :[/B] Installation/Paramétrage", 'men_ext', artworkPath + 'Logo U2Pplay.png', "Menu de configuration pour U2Pplay.")
    add_dir("[B]6. vStream :[/B] Installation/Paramétrage", 'vodt', artworkPath + 'Logo Vstream.png', "Menu de configuration pour vStream.")
    add_dir("[B]7. TV & Replay :[/B] Installation/Paramétrage", 'men_pvr', artworkPath + 'Logo TV.png', "Menu de configuration pour la TV & Replay.")
    add_dir("[B]8. IPTV :[/B] Mode Stalker & Xtream", 'men_iptv', artworkPath + 'Logo IPTV.png', "Menu de configuration pour l'IPTV de U2pplay.")
    add_dir("[B]9. Skins :[/B] Base de données de Skins", 'men_skin', artworkPath + 'Logo Skin.png', "Menu de Téléchargement et de Gestion des Skins.")
    add_dir("[B] Activer le Stop avec retour[/B]", 'sr', artworkPath + 'Logo Installer.png', "Mise en place de l'arrêt des vidéos en avec la touche Retour de la télécommande.")
    add_dir("[B][COLOR red]Nettoyer KODI[/COLOR][/B]", 'nettoye', artworkPath + 'Logo Nettoyer.png', "Menu pour nettoyer tous les dossiers de Kodi, en une fois ou séparément (Cache, Temp, Packages et Thumbnails).")
    add_dir("Vider cache vStream ", 'cache_vst', artworkPath + 'Logo Vider.png', "Vider le cache de vStream.")
    add_dir ("Gestion Backup", 'gb', artworkPath + 'Logo Backup.png', "Menu de gestion des Backups pour les Favoris et les Config.")
    add_dir ("Signalement", 'send_signalements', artworkPath + 'Logo Signaler.png', "Envoyer un signalement de liens morts, de bugs ou autres.")
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

###############################################
def gb():
    #Menu Profil & Sous-Menus

    add_dir("Gestion Favoris", "fav", artworkPath + 'Logo Favoris.png', "Menu pour gérer les Backups des Favoris.")
    add_dir("Gestion Config", "gconf", artworkPath + 'Logo Config.png', "Menu pour gérer les Backups des Configurations.")
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)
    
def gconf():
    add_dir("Sauvegarder Config", 'sav_serv', artworkPath + 'Logo Sauvegarder.png', "Permet de sauvegarder une configuration (addon_data).")
    add_dir("Restaurer Config", 'res_serv', artworkPath + 'Logo Restaurer.png', "Permet de restaurer une configuration (addon_data) - l'installation préalable des extensions est requise.")
    add_dir("Vider Addon_data", 'sad', artworkPath + 'Logo Vider.png', "Permet de vider le dossier Addon_data avant de restaurer un Backup.")
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)
    
def fav():
    add_dir("Sauvegarder Fav vStream", "fav_txt", artworkPath + 'Logo Sauvegarder.png', "Permet de sauvegarder les Favoris vStream.")
    add_dir("Restaurer Fav vStream", "fav_txt_r", artworkPath + 'Logo Restaurer.png', "Permet de restaurer les Favoris vStream.")
    add_dir("Sauvegarder Fav Catchup", "fav_cat", artworkPath + 'Logo Sauvegarder.png', "Permet de sauvegarder les Favoris Catchup.")
    add_dir("Restaurer Fav Catchup", "r_fav_cat", artworkPath + 'Logo Restaurer.png', "Permet de restaurer les Favoris Catchup.")
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True,)

###############################################

def men_repos():
    #Menu Repositories
    xbmcplugin.setPluginCategory(__handle__, "Menu Référenciels")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B][COLOR green]Tout installer[/COLOR][/B]", 'repo', artworkPath + 'Logo Installer.png', "Permet d'installer tous les référentiels disponibles.")
    add_dir("[B]1.[/B] Jurialmunkey", 'rep_jurialmunkey', artworkPath + 'Logo Installer.png', "Installation du référenciel de Jurialmunkey")
    add_dir("[B]2.[/B] vStream", 'rep_vstream', artworkPath +'Logo Installer.png', "Installation du référenciel de vStream")
    add_dir("[B]3.[/B] Autowidget", 'rep_autowidget', artworkPath +'Logo Installer.png', "Installation du référenciel de Autowidget")
    add_dir("[B]4.[/B] Kodinerds", 'rep_kodinerds', artworkPath + 'Logo Installer.png', "Installation du référenciel de Kodinerds")
    add_dir("[B]5.[/B] Michaz", 'rep_michaz', artworkPath + 'Logo Installer.png', "Installation du référenciel de Michaz.")
    add_dir("[B]6.[/B] Catchup Tv & More", 'rep_catchuptv', artworkPath + 'Logo Installer.png', "Installation du référenciel béta de Catchup Tv & More.")
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

###############################################

def men_ext():
    #Menu U2Pplay
    xbmcplugin.setPluginCategory(__handle__, "Menu U2Pplay")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1.[/B] Installation de U2Pplay", 'addons', artworkPath + 'Logo Installer.png', "Permet d'installer U2Pplay.")
    add_dir("[B]2.[/B] Importer Paramètres", 'alloptions', artworkPath + 'Logo Importer.png', "Permet d'importer les paramètres de U2Pplay en un clic.")
    add_dir("[B]3.[/B] Importer/MaJ DB", 'back_db', artworkPath +'Logo Importer.png', "Permet d'importer ou de mettre à jour la Database de U2Pplay (afin de gagner du temps et ne pas avoir à tout reconstruire depuis le début).")
    add_dir("[B]4.[/B] Ajouter Contenu", 'const_db', artworkPath +'Logo Importer.png', "Permet d'ajouter ou de mettre à jour le Contenu de U2Pplay (Téléchargement des fichiers Pastes).")
    add_dir("[B]5.[/B] Installer le Service de MAJ Auto", 'serv_maj', artworkPath + 'Logo Installer.png', "Permet la mise en place du Service de mise à jour Automatique de U2Pplay (maj HK 0.3).")
    add_dir("[B]6.[/B] Installer UpNext", 'upnext', artworkPath + 'Logo installer.png', "Permet d'installer l'addon UpNext (enchaînement des épisodes pour les séries).")
    add_dir("Paramètres de U2Pplay", 'ref_import', artworkPath + 'Logo Parametres.png', "Permet d'ouvrir les paramètres de U2Pplay.")
    add_dir("[B][COLOR red]Supprimer DB & Contenu[/COLOR][/B]", 'del_db', artworkPath +'Logo Supprimer.png', "Permet de supprimer la Database ainsi que tout le contenu (pastes) de U2Pplay.")
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

###############################################
def vodt():
    #Menu VStream
    xbmcplugin.setPluginCategory(__handle__, "Menu vStream")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1.[/B] Installation de vStream", 'addons2', artworkPath + 'Logo Installer.png', "Permet d'installer vStream.")
    add_dir("[B]2.[/B] Importer Paramètres", 'mv1', artworkPath + 'Logo Importer.png', "Permet d'importer les paramètres de vStream en un clic.")
    #add_dir("[B]3.[/B] Importer DB Torrent", 'dbt', artworkPath + 'Logo Importer.png', "Permet d'importer la DB Torrent.")
    add_dir("[B]4.[/B]Insallation du Service", 'install_autoexec', artworkPath + 'Logo Installer.png', "Installation d'autoexec pour l'actualisation des paramètres au démarrage.")    
    add_dir("Paramètres de vStream", 'pv', artworkPath + 'Logo Parametres.png', "Permet d'ouvrir les paramètres de vStream.")
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

###############################################
def men_pvr():
    #Menu TV PVR
    xbmcplugin.setPluginCategory(__handle__, "Menu TV - PVR - Replay")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1.[/B] Installation de PVR Simple Client", 'pvr', artworkPath + 'Logo Installer.png', "Permet d'installer PVR Simple Client IPTV, pour regarder la TV en streaming, liste m3u, chaînes de radio et de l'EPG.")
    add_dir("[B]2.[/B] Installation de Vavoo",'vavooto', artworkPath + 'Logo Installer.png', "Permet d'installer l'addon Vavoo TV qui propose gratuitement des chaînes TV en français.")
    add_dir("[B]3.[/B] Importer liste TV m3u Vavoo",'vavoopvr', artworkPath + 'Logo Importer.png', "Permet d'importer une liste TV au format m3u pour Vavoo PVR.")
    add_dir("[B]4.[/B] Importer liste TV m3u Foxx",'foxxpvr', artworkPath + 'Logo Importer.png', "Permet d'importer une liste TV au format m3u pour Foxx PVR.")
    add_dir("[B]5.[/B] Importer liste TV m3u Catchup + Vavoo",'catchuppvr', artworkPath + 'Logo Importer.png', "Permet d'importer une liste TV au format m3u pour Catchup et Vavoo PVR.")
    add_dir("[B]6.[/B] Installation de CatchupTV",'catchuptv', artworkPath + 'Logo Installer.png', "Permet d'installer l'addon Catchup TV pour le replay des chaînes TV.")
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

###############################################
def men_skin():
    #Menu Skins
    xbmcplugin.setPluginCategory(__handle__, "Menu Skins")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]Skins Bazo-luc :[/B] HK3 + IPTV ou juste IPTV", 'men_skin_bazoluc', artworkPath + 'Logo Bazo-Luc.png', "Menu skins Bazo-luc (Installation d'Autowidget - Estuary v2 - Artic Horizon 2 - Maj Icônes - Gestion Icônes et Autowidget).")
    add_dir("[B]Skins Bazoland :[/B] HK3 + vStream + IPTV", 'men_skin_bazoland', artworkPath + 'Logo Bazoland v2.png', "Menu skins Bazoland (Installation d'Autowidget - Estuary v2 - Artic Horizon 2 - Maj Icônes - Gestion Icônes et Autowidget).")
    add_dir("[B]Skins Osmoze :[/B] vStream + IPTV PVR", 'men_skin_osmoze', artworkPath + 'Logo Osmoze.png', "Menu skins Osmoze (Installation d'Autowidget - Artic Fuse Bazoland - Gestion Mises à jour).")
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)


def men_skin_bazoluc():
      #Menu Skins
    xbmcplugin.setPluginCategory(__handle__, "Menu Bazo-Luc")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("Importer icônes", 'au_maj', artworkPath + 'Logo Importer.png', "Permet d'importer les icônes additionnelles pour les skins.")
    add_dir("[B]AutoWidget :[/B] Installer l'addon", 'autowidget', artworkPath + 'Logo Installer.png', "Permet d'installer l'addon Autowidget pour les skins.")
    add_dir("[B]Estuary v2[/B] avec IPTV", 'dl_skin', artworkPath + 'Logo Estuary V2.png', "Permet de télécharger une configuration du skin Estuary v2 avec IPTV seulement." )
    add_dir("[B]Estuary v2[/B] avec HK3 + IPTV", 'dl_skin2', artworkPath + 'Logo Estuary V2.png', "Permet de télécharger une configuration du skin Estuary v2 avec HK3 + IPTV.")
    add_dir("[B]Estuary v2[/B] avec HK3 Light", 'dl_skin3', artworkPath + 'Logo Estuary V2.png', "Permet de télécharger une configuration du skin Estuary v2 avec HK3 avec moins de Widgets (pour les petites Configs ou petites Box Android).")
    add_dir("[B]Arctic Horizon 2[/B] avec IPTV", 'dl_skin6', artworkPath + 'Logo AH 2.png', "Permet de télécharger une configuration du skin Arctic Horizon 2 avec IPTV seulement.")
    add_dir("[B]Arctic Horizon 2[/B] avec HK3 + IPTV", 'dl_skin5', artworkPath + 'Logo AH 2.png', "Permet de télécharger une configuration du Arctic Horizon 2 avec HK3 + IPTV.")
    add_dir("[B]Arctic Horizon 2[/B] avec HK3 Light", 'dl_skin4', artworkPath + 'Logo AH 2.png', "Permet de télécharger une configuration du Arctic Horizon 2 avec HK3 avec moins de Widgets (pour les petites Configs ou petites Box Android).")
    add_dir("[B][COLOR red]Supprimer Icônes et Autowidget pour mise à jour[/COLOR][/B]", 'del_icon_aw', artworkPath + 'Logo Supprimer.png', "Supprimer les dossiers Icônes additionnelles et Autowidget des skins afin de réinstaller un skin proprement.")
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

def men_skin_bazoland():
      #Menu Skins
    xbmcplugin.setPluginCategory(__handle__, "Menu Bazoland")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("Importer icônes", 'au_maj', artworkPath + 'Logo Importer.png', "Permet d'importer les icônes additionnelles pour les skins.")
    add_dir("[B]AutoWidget :[/B] Installer l'addon", 'autowidget', artworkPath + 'Logo Installer.png', "Permet d'installer l'addon Autowidget pour les skins.")
    add_dir("[B]Arctic Horizon 2[/B] avec HK3 + vStream + IPTV", 'dl_skin7', artworkPath + 'Logo AH 2.png', "Permet de télécharger une configuration du skin Arctic Horizon 2 avec HK3 + vStream + IPTV.")
    add_dir("[B] Arctic Horizon 2[/B] avec HK3 + Vstream (on continue fusioner) + iptv", 'dl_skin10', artworkPath + 'Logo AH 2.png', "Permet de Télécharger une configuration du skin Arctic Horizon 2 avec Hk3 + vStream (on continue fusioné) + iptv")
    add_dir("[B]Estuary v2 [/B] avec HK3 + vStream + IPTV", 'dl_skin8', artworkPath + 'Logo Estuary V2.png', "Permet de télécharger une configuration du skin Estuary v2 avec HK3 + vStream + IPTV.")
    add_dir("[B] Mimic [/B] avec VST + iptv", 'dl_skin11', artworkPath + 'Logo Mimic.png', "Permet de telecharger une configuration du skin Mimic avec vst + iptv")
    add_dir("[B] Mimic [/B] avec hk3 + vst (on continu fusioner) + iptv", 'dl_skin12', artworkPath + 'Logo Mimic.png', "Permet de telecharger une configuration du skin Mimic avec HK3 + vst (on continue fusioné) + iptv")
    add_dir("[B][COLOR red]Supprimer Icônes et Autowidget pour mise à jour[/COLOR][/B]", 'del_icon_aw', artworkPath + 'Logo Supprimer.png', "Supprimer les dossiers Icônes additionnelles et Autowidget des skins afin de réinstaller un skin proprement.")
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

def men_skin_osmoze():
      #Menu Skins
    xbmcplugin.setPluginCategory(__handle__, "Menu Bazoland - Arctic Fuse")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1. AutoWidget :[/B] Installer l'addon", 'autowidget', artworkPath + 'Logo Installer.png', "Permet d'installer l'addon Autowidget requis.")
    add_dir("[B]2. PVR Simple Client :[/B] Installer l'addon", 'pvr', artworkPath + 'Logo Installer.png', "Permet d'installer PVR Simple Client requis.")
    add_dir("[B]3. Importer liste m3u :[/B] Liste intégrée pour Foxx",'foxxpvr', artworkPath + 'Logo Importer.png', "Permet d'importer la liste TV au format m3u pour Foxx PVR.")
    add_dir("[B]4. Arctic Fuse :[/B] Installation", 'install_af', artworkPath + 'Logo Arctic Fuse.png', "Installation du skin Arctic Fuse.")
    add_dir("[B]5. Paramétrage : [/B] Arctic Fuse pour vStream + IPTV PVR", 'dl_skin9', artworkPath + 'Logo Importer.png', "Permet de télécharger la configuration du skin Arctic Fuse avec vStream + IPTV PVR, version pour Bazoland.")
    add_dir("[B]Mise à Jour[/B] du Skin", 'dl_skin9', artworkPath + 'Logo MAJ.png', "Permet de mettre à jour les modifications du skin.")
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

###############################################

def men_iptv():
     #Menu
    xbmcplugin.setPluginCategory(__handle__, "Menu IPTV")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1.[/B] Mode [B]STALKER[/B]", 'men_iptv_stalker', artworkPath + 'Logo Stalker.png', "Menu pour configurer l'IPTV en mode Stalker.")
    add_dir("[B]2.[/B] Mode [B]XTREAM[/B]", 'men_iptv_xtream', artworkPath + 'Logo Xtream.png', "Menu pour configurer l'IPTV en mode Xtream.")
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

###############################################

def men_iptv_stalker():
     #Menu
    xbmcplugin.setPluginCategory(__handle__, "Menu IPTV Stalker")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1.[/B] Ajouter un Compte", 'iptv_tobal', artworkPath + 'Logo Codes.png', "Permet de renseigner un code Rentry pour télécharger un compte Unique ou un compte Liste.")
    add_dir("[B]2.[/B] Sélectionner une adresse MAC", 'iptv_tobal2', artworkPath + 'Logo Importer.png', "Permet de choisir une adresse MAC présente dans la Liste importée.")
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

################################################

def men_iptv_xtream():
     #Menu
    xbmcplugin.setPluginCategory(__handle__, "Menu IPTV Xtream")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B]1.[/B] Importer compte Fournisseur 1", 'iptv_xt1', artworkPath + 'Logo Importer.png', "Permet d'importer le compte 1.")
    add_dir("[B]2.[/B] Importer compte Fournisseur 2", 'iptv_xt2', artworkPath + 'Logo Importer.png', "Permet d'importer le compte 2.")
    add_dir("[B]3.[/B] Importer compte Fournisseur 3", 'iptv_xt3', artworkPath + 'logo Importer.png', "Permet d'importer le compte 3.")
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

# MENU NETTOYAGE
def nettoye():
    xbmc
    #menu nettoyage
    xbmcplugin.setPluginCategory(__handle__, "Nettoyer Kodi")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[B][COLOR red]Vider Kodi en un seul clic[/COLOR][/B]", 'vider_cache', artworkPath + 'Logo Vider.png', "Vider en un seul clic, TOUS les dossiers Cache, Temp, Packages et Thumbnails de Kodi")
    add_dir("[B][COLOR deepskyblue]Vider Cache uniquement[/COLOR][/B]", 'cache_seul', artworkPath + 'Logo Vider.png', "Vider uniquement le dossier Cache de Kodi")
    add_dir("[B][COLOR deepskyblue]Vider Temp uniquement[/COLOR][/B]", 'tmp_seul', artworkPath + 'Logo Vider.png', "Vider uniquement le dossier Temp de Kodi")
    add_dir("[B][COLOR deepskyblue]Vider Packages uniquement[/COLOR][/B]", 'package_seul', artworkPath + 'Logo Vider.png', "Vider uniquement le dossier Packages de Kodi")
    add_dir("[B][COLOR deepskyblue]Vider Thumbnails uniquement[/COLOR][/B]", 'thumb_seul', artworkPath + 'Logo Vider.png', "Vider uniquement le dossier Thumbnails de Kodi")
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)  

############################################## FIN LISTE DES MENUS ###############################################
def fav_txt_r():
    import restaurer_fav
def fav_txt():
    import recuperer_fav
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

################## INSTALLATION DES ADDONS ##################

def addons():
    #Installation de l'addon U2Pplay (Script Externe)
    import install_u2p

def addons2():
    #Installation de l'addon VStream (Script Externe)
    import install_vstream

def pvr():
    #Installation de l'addon PVR Simple Client (Script Externe)
    import install_pvr 

def vavooto():
    #Installation de l'addon Vavooto (Script Externe)
    import install_vavoo 
 
def catchuptv():
    #Installation de l'addon Catchup TV & More beta (Script Externe)
    import install_catchuptv   

def upnext():
    #Installation de l'addon UPNext (Script Externe)
    import install_upnext

def autowidget():
    #Installation de l'addon AutoWidget (Script Externe)
    import install_autowidget

def install_autoexec():
    #Installation du service autoexec (Script Externe)
    import install_autoexec    

################## INSTALLATION DES PARAMETRES PVR ##################

def vavoopvr():
    #Installation de la liste m3u VAVOOTO (Script Externe)
    import vavoopvr
    vavoopvr.dl() 

def foxxpvr():
    #Installation de la liste m3u FOXX (Script Externe)
    import foxxpvr
    foxxpvr.dl()

def catchuppvr():
    #Installation de la liste m3u CATCHUP / VOVOOTO (Script Externe)
    import catchuppvr
    catchuppvr.dl()    
   
################## INSTALLATION DES REFERENCIELS ##################

def rep_jurialmunkey():
    #Installation de référenciel (Script Externe)
    import install_repo_jurialmunkey

def rep_vstream():
    #Installation de référenciel (Script Externe)
    import install_repo_vstream

def rep_autowidget():
    #Installation de référenciel (Script Externe)
    import install_repo_autowidget

def rep_kodinerds():
    #Installation de référenciel (Script Externe)
    import install_repo_kodinerds

def rep_michaz():
    #Installation de référenciel (Script Externe)
    import install_repo_michaz

def rep_catchuptv():
    #Installation de référenciel (Script Externe)
    import install_repo_catchuptv


################## DIVERS ##################

def log_updates():
    #Affichage des logs de mises à jour du plugin (Script Externe)
    import log_updates

def bazoland_news():
    #Affichage des news (Script Externe)
    import bazoland_news
    
def send_signalements():
    #Envoi de notification de signalement (Script Externe)
    import send_signalements
    send_signalements.main()
    
##############################################

def cuu():
    import codeunique

    # Appeler la fonction code() de codeunique.py
    codeunique.code()


def au_maj():
    #Installation des Icônes
    # mise a jour icone aura
    # telechargement et extraction du zip
    xbmc.sleep(5000)
    zipurl = 'http://tobal.duckdns.org/config_skins/iconvodBlanc.zip'
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
    xbmc.executebuiltin("Notification(EXTRACTION OK, icônes installés)")
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
   import bazoland_ah2_2

##############################################
def dl_skin8():
    import bazoland_estuary

##############################################

def dl_skin9():
    import pack_arctic_fuse
##############################################
def dl_skin10():
    import bazoland_ah2_1
##############################################
def dl_skin11():
    import mimic_vst
##############################################
def dl_skin12():
    import mimic2
##############################################

def install_af():
    import install_arctic_fuse

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

def mv1():
    import config_vst2
    config_vst2.code()

##############################################

def back_db():
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
    xbmc.executebuiltin("Notification(Ic, Effacement en cours...)")

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
        'men_repos':(men_repos, ""),
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
        'catchuppvr': (catchuppvr, ""),
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
        #'iptvx2': (iptvx2, ""),
        'iptv_xt2': (iptv_xt2, ""),
        'iptv_xt3': (iptv_xt3, ""),
        'vodt': (vodt, ""),
        'pv': (pv, ""),
        #'vm': (vm, ""),
        'dbt': (dbt, ""),
        #'dbtd': (dbtd, ""),
        'dl_skin7': (dl_skin7, ""),
        'cuu': (cuu, ""),
        #'cuuu': (cuuu,""),
        'pbazo': (pbazo,""),
        'dl_skin8': (dl_skin8, ""),
        'dl_skin9': (dl_skin9, ""),
        'install_af': (install_af, ""),
        'sr': (sr, ""),
        'del_icon_aw': (del_icon_aw, ""),
        'cache_vst': (cache_vst, ""),
        'mv1': (mv1,""),
        'men_skin_bazoluc': (men_skin_bazoluc, ""),
        'men_skin_bazoland': (men_skin_bazoland, ""),
        'men_skin_osmoze': (men_skin_osmoze, ""),
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
        
        #Lecture des News, logs et envoi de signalements de l'addon
        'log_updates': (log_updates, ""),
        'bazoland_news': (bazoland_news, ""),
        'send_signalements': (send_signalements, ""),        
        'install_autoexec': (install_autoexec, ""),
        
        #Téléchargement des référenrciels
        'rep_jurialmunkey': (rep_jurialmunkey, ""),
        'rep_vstream': (rep_vstream, ""),
        'rep_autowidget': (rep_autowidget, ""),
        'rep_kodinerds': (rep_kodinerds, ""),
        'rep_michaz': (rep_michaz, ""),
        'rep_catchuptv': (rep_catchuptv, ""),
        'fav_txt': (fav_txt, ""),
        'fav_txt_r': (fav_txt_r, ""),
        'dl_skin10': (dl_skin10, ""),
        'dl_skin11': (dl_skin11, ""),
        'dl_skin12': (dl_skin12, ""),
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
