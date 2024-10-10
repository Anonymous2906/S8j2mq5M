import xbmc
import xbmcaddon
import xbmcvfs
import zipfile
import urllib.request
import os
import xml.etree.ElementTree as ET

# Fonction pour forcer la valeur du serveur dans settings.xml
def force_server_value():
    addon_data_path = xbmcvfs.translatePath('special://home/userdata/addon_data/plugin.program.bazoconfigcommu/')
    settings_file = os.path.join(addon_data_path, 'settings.xml')

    if os.path.exists(settings_file):
        try:
            tree = ET.parse(settings_file)
            root = tree.getroot()

            server_setting = root.find("./setting[@id='server']")
            if server_setting is not None:
                server_setting.text = 'http://tobal.duckdns.org/'
            else:
                new_setting = ET.SubElement(root, 'setting')
                new_setting.set('id', 'server')
                new_setting.text = 'http://tobal.duckdns.org/'

            tree.write(settings_file, encoding='ISO-8859-1', xml_declaration=True)
            xbmc.log("Server value forced successfully", xbmc.LOGINFO)
        except Exception as e:
            xbmc.log(f"Error while forcing server value: {str(e)}", xbmc.LOGERROR)
    else:
        xbmc.log(f"Settings file not found: {settings_file}", xbmc.LOGERROR)

# Fonction pour télécharger un fichier ZIP
def download_zip(url, download_path):
    try:
        xbmc.log(f"Downloading file from {url} to {download_path}", xbmc.LOGINFO)
        urllib.request.urlretrieve(url, download_path)
        xbmc.log(f"Download completed", xbmc.LOGINFO)
        return True
    except Exception as e:
        xbmc.log(f"Failed to download file: {e}", xbmc.LOGERROR)
        return False

# Fonction pour extraire un fichier ZIP
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

# VSTREAM - Fonction pour extraire les paramètres d'une URL
def extract_settings_from_url():
    url = "http://tobal.duckdns.org/config_vstream/config_vst_pastebin.txt"
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                return response.read().decode('utf-8').strip()
            else:
                xbmc.executebuiltin("Notification(Échec de récupération des paramètres depuis l'URL, time=5000)")
                return None
    except Exception as e:
        xbmc.executebuiltin(f"Notification(Erreur lors de l'extraction du contenu depuis l'URL : {str(e)}, time=5000)")
        return None

# VSTREAM - Mise à jour des paramètres pour les Pastes
def update_settings():
    settings_to_update = {
        'hpast': 'pastebin_url',
        'dossier1': 'pastebin_label_1',
        'past1': 'pastebin_id_1',
        'dossier2': 'pastebin_label_2',
        'past2': 'pastebin_id_2',
        'dossier3': 'pastebin_label_3',
        'past3': 'pastebin_id_3',
        'dossier4': 'pastebin_label_4',
        'past4': 'pastebin_id_4',
        'dossier5': 'pastebin_label_5',
        'past5': 'pastebin_id_5',
        'dossier6': 'pastebin_label_6',
        'past6': 'pastebin_id_6',
        'dossier7': 'pastebin_label_7',
        'past7': 'pastebin_id_7',
        'dossier8': 'bazoland_label_1',
        'past8': 'bazoland_id_1'
    }

    key_param = extract_settings_from_url()

    if key_param:
        key_values = key_param.split('\n')
        for key_value in key_values:
            key, value = key_value.split('=')
            key = key.strip().lower()
            value = value.strip()

            if key in settings_to_update:
                try:
                    addon = xbmcaddon.Addon("plugin.video.vstream")
                    addon.setSetting(id=settings_to_update[key], value=value)
                    xbmc.executebuiltin(f"Notification({key.capitalize()} ajouté(e), ok)")
                except Exception as e:
                    xbmc.executebuiltin(f"Notification(Erreur : {str(e)}, time=5000)")
            else:
                xbmc.executebuiltin(f"Notification(Clé inconnue : {key}, time=5000)")
    else:
        xbmc.executebuiltin("Notification(Aucune clé trouvée, time=5000)")

# Fonction principale
def main():
    # Forcer la valeur du serveur avant toute autre chose
    force_server_value()

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

    # Mettre à jour les paramètres de pastebin
    update_settings()

if __name__ == '__main__':
    main()