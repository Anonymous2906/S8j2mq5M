import xbmcgui
import os
import xbmcvfs
import sys
import urllib.request


# Téléchargement du fichier texte
sources_download = 'http://tobal.duckdns.org:805/api/public/dl/pUNLpwHr/config_skins/Arctic%20Fuse/bazoland_news.txt'											
sources_loc = xbmcvfs.translatePath('special://home/addons/plugin.program.bazoconfigcommu/bazoland_news.txt')											
urllib.request.urlretrieve(sources_download, sources_loc)

# Chemin vers le fichier texte
path = xbmcvfs.translatePath('special://home/addons/plugin.program.bazoconfigcommu/bazoland_news.txt')

# Lecture du contenu du fichier avec l'encodage utf-8
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Création de la fenêtre Kodi
dialog = xbmcgui.Dialog()
dialog.textviewer('[COLOR deepskyblue]BAZOLAND[/COLOR] - INFORMATIONS', content)

sys.exit()