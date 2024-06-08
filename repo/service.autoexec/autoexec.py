import os
import sqlite3
from ftplib import FTP, error_perm
import xbmcvfs
import xbmcgui
import xbmcaddon
import time

# Définir les chemins locaux
addon_data_dir = xbmcvfs.translatePath('special://home/userdata/addon_data/plugin.video.vstream/')
db_path = os.path.join(addon_data_dir, 'vstream.db')
temp_dir = os.path.join(addon_data_dir, 'temp')
os.makedirs(temp_dir, exist_ok=True)

output_files = {
    'favorite': os.path.join(addon_data_dir, 'favorites.txt'),
    'history': os.path.join(addon_data_dir, 'history.txt'),
    'resume': os.path.join(addon_data_dir, 'resume.txt'),
    'viewing': os.path.join(addon_data_dir, 'viewing.txt'),
    'watched': os.path.join(addon_data_dir, 'watched.txt'),
    'download': os.path.join(addon_data_dir, 'download.txt'),
    'sqlite_sequence': os.path.join(addon_data_dir, 'sqlite_sequence.txt')
}
video_cache_file = os.path.join(addon_data_dir, 'video_cache.db')

# Récupérer le pseudo de l'utilisateur
addon = xbmcaddon.Addon('plugin.program.bazoconfigcommu')
pseudo = addon.getSetting('pseudo')

# Définir les chemins FTP
ftp_server = 'tobal.duckdns.org'
ftp_port = 50
ftp_user = 'bazoland'
ftp_pass = 'tobalbazo'
ftp_dir = f'/dossier_partager/profils/{pseudo}/fav_vst/'
lock_file_name = 'backup.lock'
lock_file_path = os.path.join(temp_dir, lock_file_name)

def exporter_table_vers_txt(db_path, table_name, output_file):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            records = cursor.fetchall()
            with open(output_file, 'w', encoding='utf-8') as f:
                for record in records:
                    f.write(str(record) + '\n')
        xbmcgui.Dialog().notification(f"Exportation {table_name.capitalize()}", f"{table_name.capitalize()} exporté avec succès !", xbmcgui.NOTIFICATION_INFO, 5000)
    except Exception as e:
        xbmcgui.Dialog().notification(f"Exportation {table_name.capitalize()}", f"Erreur : {str(e)}", xbmcgui.NOTIFICATION_ERROR, 5000)

def uploader_vers_ftp(local_file, ftp_path):
    try:
        with FTP() as ftp:
            ftp.connect(ftp_server, ftp_port)
            ftp.login(ftp_user, ftp_pass)
            ftp.cwd(ftp_dir)
            with open(local_file, 'rb') as f:
                ftp.storbinary(f'STOR {ftp_path}', f)
        xbmcgui.Dialog().notification("Upload FTP", f"Fichier {ftp_path} téléchargé avec succès sur le serveur FTP !", xbmcgui.NOTIFICATION_INFO, 5000)
    except error_perm as e:
        xbmcgui.Dialog().notification("Upload FTP", f"Erreur de permission : {str(e)}", xbmcgui.NOTIFICATION_ERROR, 5000)
    except Exception as e:
        xbmcgui.Dialog().notification("Upload FTP", f"Erreur : {str(e)}", xbmcgui.NOTIFICATION_ERROR, 5000)

def downloader_depuis_ftp(ftp_path, local_file):
    try:
        with FTP() as ftp:
            ftp.connect(ftp_server, ftp_port)
            ftp.login(ftp_user, ftp_pass)
            ftp.cwd(ftp_dir)
            with open(local_file, 'wb') as f:
                ftp.retrbinary(f'RETR {ftp_path}', f.write)
        xbmcgui.Dialog().notification("Download FTP", f"Fichier {ftp_path} téléchargé avec succès depuis le serveur FTP !", xbmcgui.NOTIFICATION_INFO, 5000)
    except error_perm as e:
        xbmcgui.Dialog().notification("Download FTP", f"Erreur de permission : {str(e)}", xbmcgui.NOTIFICATION_ERROR, 5000)
    except Exception as e:
        xbmcgui.Dialog().notification("Download FTP", f"Erreur : {str(e)}", xbmcgui.NOTIFICATION_ERROR, 5000)

def supprimer_fichier(file_path):
    try:
        os.remove(file_path)
        xbmcgui.Dialog().notification("Suppression du fichier", f"{os.path.basename(file_path)} supprimé avec succès !", xbmcgui.NOTIFICATION_INFO, 5000)
    except Exception as e:
        xbmcgui.Dialog().notification("Suppression du fichier", f"Erreur : {str(e)}", xbmcgui.NOTIFICATION_ERROR, 5000)

def importer_txt_vers_table(db_path, table_name, input_file):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
                records = [tuple(eval(line.strip())) for line in f if line.strip()]
                if records:
                    placeholders = ', '.join(['?' for _ in records[0]])
                    columns = ', '.join([description[1] for description in cursor.execute(f"PRAGMA table_info({table_name})").fetchall()])
                    cursor.executemany(f"INSERT OR REPLACE INTO {table_name} ({columns}) VALUES ({placeholders})", records)
                    conn.commit()
        xbmcgui.Dialog().notification(f"Importation {table_name.capitalize()}", f"{table_name.capitalize()} importé avec succès !", xbmcgui.NOTIFICATION_INFO, 5000)
    except Exception as e:
        xbmcgui.Dialog().notification(f"Importation {table_name.capitalize()}", f"Erreur : {str(e)}", xbmcgui.NOTIFICATION_ERROR, 5000)

def fusionner_donnees(local_file, remote_file):
    local_data = set()
    remote_data = set()

    # Lire les données locales
    if os.path.exists(local_file):
        with open(local_file, 'r', encoding='utf-8', errors='ignore') as f:
            local_data = set(f.readlines())

    # Lire les données distantes
    if os.path.exists(remote_file):
        with open(remote_file, 'r', encoding='utf-8', errors='ignore') as f:
            remote_data = set(f.readlines())

    # Fusionner les données locales et distantes
    merged_data = local_data.union(remote_data)

    # Écrire les données fusionnées dans le fichier local
    with open(local_file, 'w', encoding='utf-8') as f:
        f.writelines(merged_data)

def fusionner_donnees_et_uploader(local_file, ftp_file_name):
    try:
        # Télécharger le fichier distant temporairement
        temp_file = os.path.join(temp_dir, ftp_file_name)
        downloader_depuis_ftp(ftp_file_name, temp_file)

        # Fusionner les données locales et distantes
        fusionner_donnees(local_file, temp_file)

        # Uploader le fichier fusionné
        uploader_vers_ftp(local_file, ftp_file_name)
    except Exception as e:
        xbmcgui.Dialog().notification("Fusion et Upload", f"Erreur : {str(e)}", xbmcgui.NOTIFICATION_ERROR, 5000)

def verifier_et_creer_lock():
    try:
        with FTP() as ftp:
            ftp.connect(ftp_server, ftp_port)
            ftp.login(ftp_user, ftp_pass)
            ftp.cwd(ftp_dir)
            while True:
                files = ftp.nlst()
                if lock_file_name in files:
                    xbmcgui.Dialog().notification("Backup en attente", "Une sauvegarde est déjà en cours. Attente de 30 secondes...", xbmcgui.NOTIFICATION_INFO, 5000)
                    time.sleep(30)
                else:
                    with open(lock_file_path, 'w') as f:
                        f.write('locked')
                    with open(lock_file_path, 'rb') as f:
                        ftp.storbinary(f'STOR {lock_file_name}', f)
                    return
    except Exception as e:
        xbmcgui.Dialog().notification("Erreur de verrouillage", f"Erreur : {str(e)}", xbmcgui.NOTIFICATION_ERROR, 5000)

def supprimer_lock():
    try:
        with FTP() as ftp:
            ftp.connect(ftp_server, ftp_port)
            ftp.login(ftp_user, ftp_pass)
            ftp.cwd(ftp_dir)
            ftp.delete(lock_file_name)
    except Exception as e:
        xbmcgui.Dialog().notification("Erreur de verrouillage", f"Erreur : {str(e)}", xbmcgui.NOTIFICATION_ERROR, 5000)

# Récupérer les paramètres de l'addon
addon = xbmcaddon.Addon('plugin.program.bazoconfigcommu')
startup_delay = int(addon.getSetting('startup_delay'))
backup_interval = int(addon.getSetting('backup_interval'))

# Vérifier si le script doit démarrer
if addon.getSetting('script_status') == 'start':
    # Attendre le délai spécifié avant d'exécuter l'action
    time.sleep(startup_delay * 60)  # Convertir le délai de minutes en secondes

    # Vérifier et attendre si le fichier de verrouillage existe avant la restauration
    try:
        with FTP() as ftp:
            ftp.connect(ftp_server, ftp_port)
            ftp.login(ftp_user, ftp_pass)
            ftp.cwd(ftp_dir)
            while True:
                files = ftp.nlst()
                if lock_file_name in files:
                    xbmcgui.Dialog().notification("Restauration en attente", "Une sauvegarde est déjà en cours. Attente de 30 secondes...", xbmcgui.NOTIFICATION_INFO, 5000)
                    time.sleep(30)
                else:
                    break
    except Exception as e:
        xbmcgui.Dialog().notification("Erreur de restauration", f"Erreur : {str(e)}", xbmcgui.NOTIFICATION_ERROR, 5000)

    # Télécharger les fichiers depuis le serveur FTP avant la restauration
    for table, file in output_files.items():
        remote_file = os.path.join(temp_dir, os.path.basename(file))
        downloader_depuis_ftp(os.path.basename(file), remote_file)
        fusionner_donnees(file, remote_file)

    # Exécuter la restauration des données utilisateur au démarrage
    for table, file in output_files.items():
        importer_txt_vers_table(db_path, table, file)

    # Ajout des nouvelles lignes après la restauration
    xbmcvfs.delete('special://home/userdata/addon_data/plugin.video.vstream/video_cache.db')
    xbmcvfs.delete('special://home/userdata/addon_data/plugin.video.vstream/pastebin_cache.db')
    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.vstream/?site=pastebin&function=refreshAllPaste&title=Mise+a+jour+des+contenus&sFav=refreshAllPaste)')
    xbmc.sleep(4000)
    xbmc.executebuiltin('ReloadSkin')

    while True:
        # Vérifier et créer le lock file avant de commencer la sauvegarde
        verifier_et_creer_lock()

        try:
            # Exécuter la fonction pour exporter les données et télécharger les fichiers exportés vers le serveur FTP
            for table, file in output_files.items():
                exporter_table_vers_txt(db_path, table, file)
                fusionner_donnees_et_uploader(file, os.path.basename(file))

            # Supprimer le fichier video_cache.db
            supprimer_fichier(video_cache_file)
        finally:
            # Supprimer le lock file après la sauvegarde
            supprimer_lock()

        # Attendre l'intervalle de sauvegarde en minutes avant la prochaine sauvegarde
        time.sleep(backup_interval * 60)
