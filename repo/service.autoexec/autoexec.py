import xbmc
import xbmcvfs
import zipfile
import urllib.request

def download_zip(url, download_path):
    try:
        xbmc.log(f"Downloading file from {url} to {download_path}", xbmc.LOGINFO)
        urllib.request.urlretrieve(url, download_path)
        xbmc.log(f"Download completed", xbmc.LOGINFO)
        return True
    except Exception as e:
        xbmc.log(f"Failed to download file: {e}", xbmc.LOGERROR)
        return False

def extract_zip(zip_path, extract_path):
    try:
        xbmc.log(f"Extracting file from {zip_path} to {extract_path}", xbmc.LOGINFO)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        xbmc.log(f"Extraction completed", xbmc.LOGINFO)
        return True
    except Exception as e:
        xbmc.log(f"Failed to extract file: {e}", xbmc.LOGERROR)
        return False

def main():
    # Chemins des fichiers
    zip_url = "http://tobal.duckdns.org:805/api/public/dl/lRM-2m2W/config_vstream/resources.zip"
    download_path = xbmcvfs.translatePath('special://home/temp/temp/plugin.video.vstream/resources.zip')
    extract_path = xbmcvfs.translatePath('special://home/addons/plugin.video.vstream/')

    # Créer les répertoires si nécessaire
    xbmcvfs.mkdirs(xbmcvfs.translatePath('special://home/temp/temp/plugin.video.vstream/'))

    # Télécharger et extraire le fichier ZIP
    if download_zip(zip_url, download_path):
        if extract_zip(download_path, extract_path):
            xbmc.log("File downloaded and extracted successfully", xbmc.LOGINFO)
        else:
            xbmc.log("Failed to extract the ZIP file", xbmc.LOGERROR)
    else:
        xbmc.log("Failed to download the ZIP file", xbmc.LOGERROR)

    # Supprimer les fichiers de cache vidéo et pastebin
    if xbmcvfs.delete('special://home/userdata/addon_data/plugin.video.vstream/video_cache.db'):
        xbmc.log("Deleted video cache", xbmc.LOGINFO)
    else:
        xbmc.log("Failed to delete video cache", xbmc.LOGERROR)

    if xbmcvfs.delete('special://home/userdata/addon_data/plugin.video.vstream/pastebin_cache.db'):
        xbmc.log("Deleted pastebin cache", xbmc.LOGINFO)
    else:
        xbmc.log("Failed to delete pastebin cache", xbmc.LOGERROR)

    # Exécuter le plugin pour mettre à jour tous les contenus de pastebin
    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.vstream/?site=pastebin&function=refreshAllPaste&title=Mise+a+jour+des+contenus&sFav=refreshAllPaste)')
    xbmc.log("Executed plugin to refresh all pastebin contents", xbmc.LOGINFO)

    # Attendre pendant 4000 millisecondes (4 secondes)
    xbmc.sleep(4000)
    xbmc.log("Waited for 4 seconds", xbmc.LOGINFO)

    # Recharger le skin
    xbmc.executebuiltin('ReloadSkin')
    xbmc.log("Reloaded skin", xbmc.LOGINFO)

if __name__ == '__main__':
    main()