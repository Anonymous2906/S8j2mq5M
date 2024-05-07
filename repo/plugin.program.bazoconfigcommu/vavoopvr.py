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
    zipurl = 'http://tobal.duckdns.org:805/api/public/dl/N3F3G8WC/kodi/bazoconfig/pvr/vavoo/vavoo.zip'
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmcvfs.translatePath('special://home/userdata/addon_data/pvr.iptvsimple'))

    xbmc.executebuiltin("Notification(EXTRACTION OK, pvr foxx ok)")
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(FICHIER TEMP, Effacement en cours...)")

    xbmc.sleep(5000)
