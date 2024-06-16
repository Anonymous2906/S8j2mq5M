import xbmc
import xbmcvfs
import zipfile
import os
import urllib.request

def download_zip(url, download_path):
    try:
        urllib.request.urlretrieve(url, download_path)
        return True
    except Exception as e:
        xbmc.log(f"Failed to download file: {e}", xbmc.LOGERROR)
        return False

def extract_zip(zip_path, extract_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        return True
    except Exception as e:
        xbmc.log(f"Failed to extract file: {e}", xbmc.LOGERROR)
        return False

def main():
    # Télécharger et extraire le fichier ZIP
    zip_url = "http://tobal.duckdns.org:805/api/public/dl/lRM-2m2W/config_vstream/resources.zip"
    download_path = 'special://home/userdata/addon_data/plugin.video.vstream/resources.zip'
    extract_path = 'special://home/addons/plugin.video.vstream/'

    if download_zip(zip_url, download_path):
        if extract_zip(download_path, extract_path):
            xbmc.log("File downloaded and extracted successfully", xbmc.LOGINFO)
        else:
            xbmc.log("Failed to extract the ZIP file", xbmc.LOGERROR)
    else:
        xbmc.log("Failed to download the ZIP file", xbmc.LOGERROR)

    # Supprimer le fichier ZIP après extraction
    xbmcvfs.delete(download_path)

    # Supprimer les fichiers de cache vidéo et pastebin
    xbmcvfs.delete('special://home/userdata/addon_data/plugin.video.vstream/video_cache.db')
    xbmcvfs.delete('special://home/userdata/addon_data/plugin.video.vstream/pastebin_cache.db')

    # Exécuter le plugin pour mettre à jour tous les contenus de pastebin
    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.vstream/?site=pastebin&function=refreshAllPaste&title=Mise+a+jour+des+contenus&sFav=refreshAllPaste)')

    # Attendre pendant 4000 millisecondes (4 secondes)
    xbmc.sleep(4000)

    # Recharger le skin
    xbmc.executebuiltin('ReloadSkin')

if __name__ == '__main__':
    main()