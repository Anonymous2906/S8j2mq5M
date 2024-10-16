import xbmcaddon
import xbmc
import xbmcvfs
import shutil
from zipfile import ZipFile
from io import BytesIO
from urllib.request import urlopen

def dl():
    # Désactiver l'addon autowidget
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "plugin.video.vstream", "enabled": false }}')
    xbmc.sleep(5000)

    # Téléchargement et extraction du zip
    zipurl = 'http://tobal.duckdns.org:805/api/public/dl/XC5LMkiW/kodi/bazoconfig/dossier_partager/config_vstream/sites.zip'
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmcvfs.translatePath('special://home/userdata/addon_data/plugin.video.vstream'))

    xbmc.executebuiltin("Notification(EXTRACTION OK, sources configurer )")
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(FICHIER TEMP, Effacement en cours...)")

    xbmc.sleep(5000)


    zipurl = 'http://tobal.duckdns.org:805/api/public/dl/PIZTo8dH/kodi/bazoconfig/dossier_partager/config_vstream/resources.zip'
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmcvfs.translatePath('special://home/addons/plugin.video.vstream'))

    xbmc.executebuiltin("Notification(EXTRACTION OK, vstbazoland configurer )")
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(FICHIER TEMP, Effacement en cours...)")

    # Suppression du dossier temporaire
    dirPath = xbmcvfs.translatePath('special://home/temp/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')

    # Réactiver l'addon autowidget
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "plugin.video.vstream", "enabled": true }}')
    xbmc.sleep(5000)
    xbmc.executebuiltin("Notification(TERMINE , ...)")

