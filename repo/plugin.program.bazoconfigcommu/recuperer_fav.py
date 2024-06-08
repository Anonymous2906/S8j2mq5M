import os
import sqlite3
from ftplib import FTP, error_perm
import xbmcvfs
import xbmcgui
import xbmcaddon

# Définir les chemins locaux
addon_data_dir = xbmcvfs.translatePath('special://home/userdata/addon_data/plugin.video.vstream/')
db_path = os.path.join(addon_data_dir, 'vstream.db')
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

def exporter_table_vers_txt(db_path, table_name, output_file):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            records = cursor.fetchall()
            with open(output_file, 'w') as f:
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

def supprimer_fichier(file_path):
    try:
        os.remove(file_path)
        xbmcgui.Dialog().notification("Suppression du fichier", f"{os.path.basename(file_path)} supprimé avec succès !", xbmcgui.NOTIFICATION_INFO, 5000)
    except Exception as e:
        xbmcgui.Dialog().notification("Suppression du fichier", f"Erreur : {str(e)}", xbmcgui.NOTIFICATION_ERROR, 5000)

# Exécuter la fonction pour exporter les données et télécharger les fichiers exportés vers le serveur FTP
for table, file in output_files.items():
    exporter_table_vers_txt(db_path, table, file)
    uploader_vers_ftp(file, os.path.basename(file))

# Supprimer le fichier video_cache.db
supprimer_fichier(video_cache_file)
