import xbmc
import xbmcvfs
import xbmcaddon
import xbmcgui
import urllib.request
import sys

# Remplacez 'nom_de_l_addon' par le nom de l'addon que vous souhaitez installer à partir du référentiel.
addon_name = 'pvr.iptvsimple'

# Vérifiez si l'addon est installé
if not xbmc.getCondVisibility('System.HasAddon(' + addon_name + ')'):
    xbmc.executebuiltin("Notification(INSTALLATION, Système TV PVR, installation en cours)")
    
    # Installez l'addon
    xbmc.executebuiltin('InstallAddon(' + addon_name + ')')
    
    # Attendez que l'addon soit installé
    while not xbmc.getCondVisibility('System.HasAddon(' + addon_name + ')'):
        xbmc.sleep(10000)  # Attendre 10 secondes avant de vérifier à nouveau

    xbmc.executebuiltin("Notification(INSTALLATION, Addon installé, téléchargement des paramètres en cours)")

    # Créer le dossier si nécessaire
    settings_folder = xbmcvfs.translatePath('special://home/userdata/addon_data/pvr.iptvsimple/')
    if not xbmcvfs.exists(settings_folder):
        xbmcvfs.mkdir(settings_folder)

    # Télécharger les fichiers
    settings_download2 = 'http://tobal.duckdns.org:805/api/public/dl/9W8kXAqm/kodi/bazoconfig/pvr/instance-settings-1.xml'
    settings_loc2 = xbmcvfs.translatePath('special://home/userdata/addon_data/pvr.iptvsimple/instance-settings-1.xml')
    urllib.request.urlretrieve(settings_download2, settings_loc2)
    xbmc.executebuiltin("Notification(INSTALLATION, Téléchargements terminés)")
    xbmcgui.Dialog().ok('Installation réussie', 'L\'addon a été installé avec succès et les paramètres appliqués.')

    # Désactivation / Activation de l'addon pour application et application des paramètres    
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "pvr.iptvsimple", "enabled": false }}')
    xbmc.sleep(10000)  # Attendre 3 secondes    
    #xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "pvr.iptvsimple", "enabled": true }}')
    #xbmc.executebuiltin("Notification(INFORMATION, Redémarrage nécéssaire pour appliquer les paramètres.)")
    
else:
    xbmc.executebuiltin("Notification(INFORMATION, Services TV Actifs)")
sys.exit()