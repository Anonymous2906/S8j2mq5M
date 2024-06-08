import xbmc
import xbmcvfs
import xbmcaddon
import xbmcgui
import urllib.request
import sys

# Liste des noms de référentiels à installer
repository_names = ['repository.jurialmunkey']

for repository_name in repository_names:
    # Vérifiez si le référentiel est installé
    if not xbmc.getCondVisibility('System.HasAddon(' + repository_name + ')'):
        xbmc.executebuiltin("Notification(INSTALLATION, Référentiel " + repository_name + " Installation en cours...)")
        
        # Installez le référentiel
        xbmc.executebuiltin('InstallAddon(' + repository_name + ')')
        
        # Attendez que le référentiel soit installé
        while not xbmc.getCondVisibility('System.HasAddon(' + repository_name + ')'):
            xbmc.sleep(5000)  # Attendre 5 secondes avant de vérifier à nouveau

        xbmc.executebuiltin("Notification(INSTALLATION, Référentiel " + repository_name + " OK)")
    else:
        xbmc.executebuiltin("Notification(INSTALLATION, Référentiel " + repository_name + " déjà installé !)")

# Une fois que tous les référentiels sont installés, vous pouvez afficher une notification pour indiquer qu'un redémarrage est nécessaire
    xbmc.executebuiltin("Notification(REDEMARRAGE, Veuillez redémarrer KODI à la fin de vos installations...)")
#xbmc.sleep(2000)
#xbmc.executebuiltin('Quit')

sys.exit()