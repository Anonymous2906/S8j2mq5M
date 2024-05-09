import os
import ftplib
import xbmcgui
import xbmc
import xbmcaddon
import xbmcvfs

# Fonction pour désactiver l'addon
def desactiver_addon():
    # Récupérer l'addon
    addon = xbmcaddon.Addon('plugin.video.catchuptvandmore')
    # Désactiver l'addon en définissant un paramètre
    addon.setSetting('enabled', 'false')

# Fonction pour réactiver l'addon
def reactiver_addon():
    # Récupérer l'addon
    addon = xbmcaddon.Addon('plugin.video.catchuptvandmore')
    # Réactiver l'addon en définissant un paramètre
    addon.setSetting('enabled', 'true')

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

# Fonction pour restaurer les données utilisateur
def restaurer_donnees_utilisateur():
    # Utiliser des variables pour les informations de connexion
    hote = "tobal.duckdns.org"
    port = 50
    utilisateur = "bazoland"
    mot_de_passe = "tobalbazo"

    # Désactiver l'addon avant de procéder
    desactiver_addon()

    ftp = connecter_ftp(hote, port, utilisateur, mot_de_passe)
    if ftp is None:
        return  # Arrêter l'exécution si la connexion FTP échoue

    # Récupérer le pseudo à partir des paramètres de l'addon 'plugin.program.bazoconfigcommu'
    addon = xbmcaddon.Addon('plugin.program.bazoconfigcommu')
    pseudo = addon.getSetting('pseudo')

    if not pseudo:
        xbmcgui.Dialog().ok("Erreur", "Aucun pseudo trouvé dans les paramètres de l'addon")
        return

    destination_path = xbmcvfs.translatePath("special://home/userdata/addon_data/plugin.video.catchuptvandmore/favourites.json")

    source_path = f"/dossier_partager/profils/{pseudo}/fav_catchup/favourites.json"

    # Utiliser un bloc 'with' pour s'assurer que la connexion FTP sera fermée correctement
    with ftp:
        try:
            with open(destination_path, 'wb') as f:
                ftp.retrbinary(f'RETR {source_path}', f.write)

            xbmcgui.Dialog().ok("Restauration terminée", "Le fichier favourites.json a été restauré avec succès")
        except ftplib.all_errors as e:
            xbmcgui.Dialog().ok("Erreur FTP", "Erreur lors de la restauration : " + str(e))

    # Réactiver l'addon à la fin du script
    reactiver_addon()

# Appeler la fonction principale
restaurer_donnees_utilisateur()
