import os
import ftplib
import xbmc
import xbmcaddon
import xbmcvfs
import time

# Variable pour garder une trace de l'état de la restauration
restauration_effectuee = False

# Fonction pour se connecter au serveur FTP
def connecter_ftp(hote, port, utilisateur, mot_de_passe):
    ftp = ftplib.FTP()
    try:
        ftp.connect(hote, port)
        ftp.login(utilisateur, mot_de_passe)
        return ftp
    except ftplib.all_errors as e:
        xbmc.log("Erreur FTP : " + str(e), level=xbmc.LOGERROR)
        return None

# Fonction pour restaurer les données utilisateur
def restaurer_donnees_utilisateur():
    global restauration_effectuee
    if restauration_effectuee:
        return  # Si la restauration a déjà été effectuée, ne pas la répéter

    # Utiliser des variables pour les informations de connexion
    hote = "tobal.duckdns.org"
    port = 50
    utilisateur = "bazoland"
    mot_de_passe = "tobalbazo"

    ftp = connecter_ftp(hote, port, utilisateur, mot_de_passe)
    if ftp is None:
        return  # Arrêter l'exécution si la connexion FTP échoue

    # Récupérer le pseudo à partir des paramètres de l'addon 'plugin.program.bazoconfigcommu'
    addon = xbmcaddon.Addon('plugin.program.bazoconfigcommu')
    pseudo = addon.getSetting('pseudo')

    if not pseudo:
        xbmc.log("Aucun pseudo trouvé dans les paramètres de l'addon", level=xbmc.LOGERROR)
        return

    source_path = f"/dossier_partager/profils/{pseudo}/fav_vst/"
    destination_path = xbmcvfs.translatePath("special://home/userdata/addon_data/plugin.video.vstream/")

    # Utiliser un bloc 'with' pour s'assurer que la connexion FTP sera fermée correctement
    with ftp:
        try:
            vstream_db_path = os.path.join(destination_path, "vstream.db")
            with open(vstream_db_path, 'wb') as f:
                ftp.retrbinary(f'RETR {os.path.join(source_path, "vstream.db")}', f.write)

            xbmc.log("Restauration terminée : Le fichier vstream.db a été restauré pour l'utilisateur " + pseudo, level=xbmc.LOGINFO)
            restauration_effectuee = True
        except ftplib.all_errors as e:
            xbmc.log("Erreur FTP lors de la restauration : " + str(e), level=xbmc.LOGERROR)

# Fonction pour sauvegarder les données utilisateur
def sauvegarder_donnees_utilisateur():
    # Utiliser des variables pour les informations de connexion
    hote = "tobal.duckdns.org"
    port = 50
    utilisateur = "bazoland"
    mot_de_passe = "tobalbazo"

    ftp = connecter_ftp(hote, port, utilisateur, mot_de_passe)
    if ftp is None:
        return  # Arrêter l'exécution si la connexion FTP échoue

    # Récupérer le pseudo à partir des paramètres de l'addon 'plugin.program.bazoconfigcommu'
    addon = xbmcaddon.Addon('plugin.program.bazoconfigcommu')
    pseudo = addon.getSetting('pseudo')

    if not pseudo:
        xbmc.log("Aucun pseudo trouvé dans les paramètres de l'addon", level=xbmc.LOGERROR)
        return

    source_path = xbmcvfs.translatePath("special://home/userdata/addon_data/plugin.video.vstream/")
    destination_path = f"/dossier_partager/profils/{pseudo}/fav_vst/"

    # Utiliser un bloc 'with' pour s'assurer que la connexion FTP sera fermée correctement
    with ftp:
        try:
            # Créer le dossier de destination s'il n'existe pas
            try:
                ftp.mkd(destination_path)
            except ftplib.error_perm:
                # Le dossier existe déjà, c'est normal, pas besoin de le créer
                pass

            vstream_db_path = os.path.join(source_path, "vstream.db")
            with open(vstream_db_path, 'rb') as f:
                ftp.storbinary(f'STOR {os.path.join(destination_path, "vstream.db")}', f)

            xbmc.log("Sauvegarde terminée : Le fichier vstream.db a été sauvegardé pour l'utilisateur " + pseudo, level=xbmc.LOGINFO)
        except ftplib.all_errors as e:
            xbmc.log("
