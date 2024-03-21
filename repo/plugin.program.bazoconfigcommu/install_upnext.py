import xbmc
import sys

# Liste des noms d'addons à installer
addon_names = ['service.upnext']

for addon_name in addon_names:
    # Vérifiez si l'addon est installé
    if not xbmc.getCondVisibility('System.HasAddon(' + addon_name + ')'):
        xbmc.executebuiltin("Notification(INSTALLATION, Addon " + addon_name + " non installé, installation en cours)")
        
        # Installez l'addon
        xbmc.executebuiltin('InstallAddon(' + addon_name + ')')
        
        # Attendez que l'addon soit installé pendant 5 secondes maximum
        timeout = 50  # Nombre d'essais (50 * 100ms = 5s)
        while not xbmc.getCondVisibility('System.HasAddon(' + addon_name + ')') and timeout > 0:
            xbmc.sleep(100)  # Attendre 100ms
            timeout -= 1

        # Vérifiez si l'addon a été installé avec succès
        if xbmc.getCondVisibility('System.HasAddon(' + addon_name + ')'):
            xbmc.executebuiltin("Notification(INSTALLATION, Addon " + addon_name + " OK)")
        else:
            xbmc.executebuiltin("Notification(INSTALLATION, vérification de " + addon_name + " en cours...)")
    else:
        xbmc.executebuiltin("Notification(INSTALLATION, Addon " + addon_name + " déjà installé !)")

xbmc.executebuiltin("Notification(INFORMATION, Installation réussie.)")
sys.exit()