import xbmc
import xbmcvfs
import shutil
from zipfile import ZipFile
from io import BytesIO
from urllib.request import urlopen

def dl():
    # Désactiver l'addon autowidget
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "plugin.program.autowidget", "enabled": false }}')
    xbmc.sleep(5000)

    # Téléchargement et extraction du zip
    zipurl = 'http://tobal.duckdns.org:805/api/public/dl/F5DZg7Ne/kodi/bazoconfig/add/bazoland.zip'
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmcvfs.translatePath('special://home/userdata/addon_data'))

    xbmc.executebuiltin("Notification(EXTRACTION OK, skin installé)")
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(FICHIER TEMP, Effacement en cours...)")

    # Suppression du dossier temporaire
    dirPath = xbmcvfs.translatePath('special://home/temp/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')

    # Réactiver l'addon autowidget
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "plugin.program.autowidget", "enabled": true }}')
    xbmc.sleep(5000)
    xbmc.executebuiltin("Notification(TERMINE , ...)")

# Appel de la fonction dl
dl()
