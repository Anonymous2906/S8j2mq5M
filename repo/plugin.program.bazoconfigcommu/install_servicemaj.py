import xbmc
import sys

# Liste des noms d'addons à installer
addon_names = ['service.majhk']

for addon_name in addon_names:
    # Vérifiez si l'addon est installé
    if xbmc.getCondVisibility('System.HasAddon(' + addon_name + ')'):
        xbmc.executebuiltin("Notification(DEINSTALLATION, Désinstallation de l'addon " + addon_name + " en cours...)")
        
        # Désinstaller l'addon
        xbmc.executebuiltin('UninstallAddon(' + addon_name + ')')
        
        # Attendez que l'addon soit désinstallé pendant 5 secondes maximum
        timeout = 50  # Nombre d'essais (50 * 100ms = 5s)
        while xbmc.getCondVisibility('System.HasAddon(' + addon_name + ')') and timeout > 0:
            xbmc.sleep(100)  # Attendre 100ms
            timeout -= 1

        # Vérifiez si l'addon a été désinstallé avec succès
        if not xbmc.getCondVisibility('System.HasAddon(' + addon_name + ')'):
            xbmc.executebuiltin("Notification(DEINSTALLATION, Désinstallation de l'addon " + addon_name + " OK)")
        else:
            xbmc.executebuiltin("Notification(DEINSTALLATION, vérification de désinstallation de " + addon_name + " en cours...)")
    
    # Installez l'addon après la désinstallation ou s'il n'était pas installé
    xbmc.executebuiltin("Notification(INSTALLATION, Installation de l'addon " + addon_name + " en cours...)")
    xbmc.executebuiltin('InstallAddon(' + addon_name + ')')
    
    # Attendez que l'addon soit installé pendant 5 secondes maximum
    timeout = 50  # Nombre d'essais (50 * 100ms = 5s)
    while not xbmc.getCondVisibility('System.HasAddon(' + addon_name + ')') and timeout > 0:
        xbmc.sleep(100)  # Attendre 100ms
        timeout -= 1

    # Vérifiez si l'addon a été installé avec succès
    if xbmc.getCondVisibility('System.HasAddon(' + addon_name + ')'):
        xbmc.executebuiltin("Notification(INSTALLATION, Installation de l'addon " + addon_name + " OK)")
    else:
        xbmc.executebuiltin("Notification(INSTALLATION, vérification de l'installation de " + addon_name + " en cours...)")

xbmc.executebuiltin("Notification(INFORMATION, Installation réussie.)")
sys.exit()