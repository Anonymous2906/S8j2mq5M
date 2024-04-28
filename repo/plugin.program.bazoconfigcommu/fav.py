import os
import ftplib
import xbmcgui
import xbmc
import xbmcaddon
import xbmcvfs

# Fonction pour se connecter au serveur FTP
def connecter_ftp(hote, port, utilisateur, mot_de_passe):
    ftp = ftplib.FTP()
    try:
        ftp.connect(hote, port)
        ftp.login(utilisateur, mot_de_passe)
        return ftp
    except ftplib.all_errors as e:
        xbmcgui.Dialog().ok("Erreur FTP", "Impossible de se connecter : " + str(e))
        return None

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
        xbmcgui.Dialog().ok("Erreur", "Aucun pseudo trouvé dans les paramètres de l'addon")
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

            xbmcgui.Dialog().ok("Sauvegarde terminée", f"Le fichier vstream.db a été sauvegardé pour l'utilisateur {pseudo}")
        except ftplib.all_errors as e:
            xbmcgui.Dialog().ok("Erreur FTP", "Erreur lors de la sauvegarde : " + str(e))

# Appeler la fonction principale
sauvegarder_donnees_utilisateur()
