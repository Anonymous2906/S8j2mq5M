import xbmc
import xbmcvfs
import xbmcgui
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO

def download_and_extract(url, save_path):
    progress_dialog = xbmcgui.DialogProgress()
    progress_dialog.create('Téléchargement en cours', 'Veuillez patienter...')
    req = urlopen(url)
    total_size = int(req.headers['Content-Length'])
    downloaded = 0
    block_size = 8192  # Taille des blocs à télécharger
    with open(save_path, 'wb') as f:
        while True:
            buffer = req.read(block_size)
            if not buffer:
                break
            downloaded += len(buffer)
            f.write(buffer)
            percent = int(downloaded * 100 / total_size)
            progress_dialog.update(percent, 'Téléchargé: {}%'.format(percent))
            if progress_dialog.iscanceled():
                progress_dialog.close()
                return False
    progress_dialog.close()
    return True

# installer le skin cosmic bazoluc iptv
# téléchargement et extraction du zip
xbmc.sleep(5000)
zipurl = 'http://tobal.duckdns.org:805/api/public/dl/bDj_Ruq9/kodi/bazoconfig/backup_db/mediasNewSauve.bd.zip'
zip_save_path = xbmcvfs.translatePath('special://home/userdata/addon_data/plugin.video.sendtokodiU2P/mediasNewSauve.bd.zip')

if download_and_extract(zipurl, zip_save_path):
    with ZipFile(zip_save_path) as zfile:
        zfile.extractall(xbmcvfs.translatePath('special://home/userdata/addon_data/plugin.video.sendtokodiU2P'))
    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.sendtokodiU2P/?action=gestiondb)')
    xbmcgui.Dialog().ok('Succès', 'La base de données a été téléchargée et extraite.')
else:
    xbmcgui.Dialog().ok('Annulation', 'Le téléchargement a été annulé par l\'utilisateur.')