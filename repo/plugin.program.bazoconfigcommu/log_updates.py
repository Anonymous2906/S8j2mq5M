import xbmcgui
import os
import xbmcvfs
import sys
import urllib.request

# Chemin vers le fichier texte
path = xbmcvfs.translatePath('special://home/addons/plugin.program.bazoconfigcommu/changelog.txt')

# Lecture du contenu du fichier avec l'encodage utf-8
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Création de la fenêtre Kodi
dialog = xbmcgui.Dialog()
dialog.textviewer('[COLOR deepskyblue]BAZOLAND[/COLOR] - MISE A JOUR', content)

sys.exit()