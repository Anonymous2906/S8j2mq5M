import xbmc
import xbmcaddon
import time

# Récupérer les paramètres de l'addon
addon = xbmcaddon.Addon()
startup_delay = int(addon.getSetting('startup_delay'))

# Attendre le délai spécifié avant d'exécuter l'action
time.sleep(startup_delay)

# Insérez ici le code que vous souhaitez exécuter après le délai

# Commande à exécuter pour activer une fenêtre spécifique
xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.program.bazoconfigcommu/?action=sfav")')

# Revenir à l'écran d'accueil de Kodi
xbmc.executebuiltin('ActivateWindow(home)')
