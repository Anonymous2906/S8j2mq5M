import os
import sqlite3
from ftplib import FTP, error_perm
import xbmcvfs
import xbmcgui
import xbmcaddon

# Définir les chemins locaux
addon_data_dir = xbmcvfs.translatePath('special://home/userdata/addon_data/plugin.video.vstream/')
db_path = os.path.join(addon_data_dir, 'vstream.db')
input_files = {
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

def importer_txt_vers_table(db_path, table_name, input_file):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            with open(input_file, 'r', encoding='latin-1') as f:  # Spécifier le codage ici
                records = [tuple(eval(line.strip())) for line in f if line.strip()]
                if records:
                    placeholders = ', '.join(['?' for _ in records[0]])
                    columns = ', '.join([description[1] for description in cursor.execute(f"PRAGMA table_info({table_name})").fetchall()])
                    cursor.executemany(f"INSERT OR REPLACE INTO {table_name} ({columns}) VALUES ({placeholders})", records)
                    conn.commit()
        xbmcgui.Dialog().notification(f"Importation {table_name.capitalize()}", f"{table_name.capitalize()} importé avec succès !", xbmcgui.NOTIFICATION_INFO, 5000)
    except Exception as e:
        xbmcgui.Dialog().notification(f"Importation {table_name.capitalize()}", f"Erreur : {str(e)}", xbmcgui.NOTIFICATION_ERROR, 5000)

def downloader_depuis_ftp(ftp_path, local_file):
    try:
        with FTP() as ftp:
            ftp.connect(ftp_server, ftp_port)
            ftp.login(ftp_user, ftp_pass)
            ftp.cwd(ftp_dir)
            with open(local_file, 'wb') as f:
                ftp.retrbinary(f'RETR {ftp_path}', f.write)
        xbmcgui.Dialog().notification("Téléchargement FTP", f"Fichier {ftp_path} téléchargé avec succès depuis le serveur FTP !", xbmcgui.NOTIFICATION_INFO, 5000)
    except error_perm as e:
        xbmcgui.Dialog().notification("Téléchargement FTP", f"Erreur de permission : {str(e)}", xbmcgui.NOTIFICATION_ERROR, 5000)
    except Exception as e:
        xbmcgui.Dialog().notification("Téléchargement FTP", f"Erreur : {str(e)}", xbmcgui.NOTIFICATION_ERROR, 5000)

def supprimer_fichier(file_path):
    try:
        os.remove(file_path)
        xbmcgui.Dialog().notification("Suppression du fichier", f"{os.path.basename(file_path)} supprimé avec succès !", xbmcgui.NOTIFICATION_INFO, 5000)
    except Exception as e:
        xbmcgui.Dialog().notification("Suppression du fichier", f"Erreur : {str(e)}", xbmcgui.NOTIFICATION_ERROR, 5000)

# Exécuter la fonction pour télécharger les fichiers depuis le serveur FTP et importer les données dans la base de données
for table, file in input_files.items():
    downloader_depuis_ftp(os.path.basename(file), file)
    importer_txt_vers_table(db_path, table, file)

# Supprimer le fichier video_cache.db si nécessaire
supprimer_fichier(video_cache_file)
