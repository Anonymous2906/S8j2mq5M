import xbmc
import xbmcvfs
import xbmcgui
import shutil
from urllib.request import urlopen
from zipfile import ZipFile
import os

# Fonction pour télécharger et extraire le fichier ZIP avec une boîte de dialogue de progression
def download_and_extract(url, save_path):
    progress_dialog = xbmcgui.DialogProgress()
    progress_dialog.create('Téléchargement de la Mise à Jour', 'Téléchargement en cours...')
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
            progress_dialog.update(percent, 'Téléchargement: {}%'.format(percent))
            if progress_dialog.iscanceled():
                progress_dialog.close()
                return False
    progress_dialog.update(100, 'Extraction en cours...')
    with ZipFile(save_path, 'r') as zfile:
        zfile.extractall(os.path.dirname(save_path))
    os.remove(save_path)  # Suppression du fichier ZIP après extraction
    progress_dialog.close()
    return True

# Création du répertoire de sauvegarde si nécessaire
save_directory = xbmcvfs.translatePath('special://home/temp/temp/hk3-ah2/')
xbmcvfs.mkdirs(save_directory)

# Téléchargement et extraction du zip
zipurl = 'http://tobal.duckdns.org/config_skins/ah2/hk3-ah2.zip'
save_path = os.path.join(save_directory, 'hk3-ah2.zip')

# Barre de progression pour le téléchargement et l'extraction
download_successful = download_and_extract(zipurl, save_path)

if download_successful:
    xbmc.executebuiltin("Notification(TELECHARGEMENT ET EXTRACTION OK, Préparation...)")

    # Barre de progression pour l'exécution du reste du script
    progress_dialog = xbmcgui.DialogProgress()
    progress_dialog.create('Mise à Jour en cours...', 'Veuillez patienter...')
    progress = 0

    # Désactiver l'addon autowidget
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "plugin.program.autowidget", "enabled": false }}')
    xbmc.sleep(3000)

    # Copie des fichiers extraits
    source_dir1 = xbmcvfs.translatePath('special://home/temp/temp/hk3-ah2/')
    destination_dir1 = xbmcvfs.translatePath('special://home/userdata/addon_data')

    files_to_copy = [
        (source_dir1, destination_dir1),
    ]

    total_files = len(files_to_copy)

    for source, destination in files_to_copy:
        if os.path.isdir(source):
            shutil.copytree(source, destination, dirs_exist_ok=True)
        else:
            shutil.copy(source, destination)
        progress += 1
        progress_percent = int(progress * 100 / total_files)
        progress_dialog.update(progress_percent, 'Copie des fichiers: {}%'.format(progress_percent))

    # Réactiver l'addon autowidget
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "plugin.program.autowidget", "enabled": true }}')
    xbmc.sleep(3000)

    progress_dialog.close()
    xbmc.executebuiltin("Notification(MISE A JOUR, Terminée !)")

    # Suppression du dossier temporaire
    shutil.rmtree(xbmcvfs.translatePath('special://home/temp/temp/'))
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')

else:
    xbmc.executebuiltin("Notification(TELECHARGEMENT ET EXTRACTION ANNULÉS, Préparation annulée)")

