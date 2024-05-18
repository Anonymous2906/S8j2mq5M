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
        xbmc.executebuiltin('Notification(Erreur FTP, Impossible de se connecter : ' + str(e) + ', 5000)')
        return None

# Fonction pour vérifier si le script doit être arrêté
def verifier_arret():
    addon = xbmcaddon.Addon('plugin.program.bazoconfigcommu')
    if addon.getSetting('script_status') == 'stop':
        return True
    return False

# Fonction pour restaurer les données utilisateur
def restaurer_donnees_utilisateur():
    global restauration_effectuee
    if restauration_effectuee or verifier_arret():
        return  # Si la restauration a déjà été effectuée ou si le script doit être arrêté, ne pas la répéter

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
        xbmc.executebuiltin('Notification(Erreur, Aucun pseudo trouvé dans les paramètres de l\'addon, 5000)')
        return

    source_path = f"/dossier_partager/profils/{pseudo}/fav_vst/"
    destination_path = xbmcvfs.translatePath("special://home/userdata/addon_data/plugin.video.vstream/")

    # Utiliser un bloc 'with' pour s'assurer que la connexion FTP sera fermée correctement
    with ftp:
        try:
            vstream_db_path = os.path.join(destination_path, "vstream.db")
            with open(vstream_db_path, 'wb') as f:
                ftp.retrbinary(f'RETR {os.path.join(source_path, "vstream.db")}', f.write)

            xbmc.executebuiltin('Notification(Restauration terminée, Le fichier vstream.db a été restauré pour l\'utilisateur ' + pseudo + ', 5000)')
            restauration_effectuee = True

            # Supprimer les fichiers de cache
            xbmcvfs.delete('special://home/userdata/addon_data/plugin.video.vstream/video_cache.db')
            xbmcvfs.delete('special://home/userdata/addon_data/plugin.video.vstream/pastebin_cache.db')

            # Exécuter le plugin vStream pour forcer la mise à jour des contenus
            xbmc.executebuiltin('RunPlugin(plugin://plugin.video.vstream/?site=pastebin&function=refreshAllPaste&title=Mise+a+jour+des+contenus&sFav=refreshAllPaste)')
            xbmc.sleep(4000)
            xbmc.executebuiltin('ReloadSkin()')
        except ftplib.all_errors as e:
            xbmc.executebuiltin('Notification(Erreur FTP, Erreur lors de la restauration : ' + str(e) + ', 5000)')

# Fonction pour sauvegarder les données utilisateur
def sauvegarder_donnees_utilisateur():
    if verifier_arret():
        return  # Si le script doit être arrêté, ne pas exécuter la sauvegarde

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
        xbmc.executebuiltin('Notification(Erreur, Aucun pseudo trouvé dans les paramètres de l\'addon, 5000)')
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

            xbmc.executebuiltin('Notification(Sauvegarde terminée, Le fichier vstream.db a été sauvegardé pour l\'utilisateur ' + pseudo + ', 5000)')
        except ftplib.all_errors as e:
            xbmc.executebuiltin('Notification(Erreur FTP, Erreur lors de la sauvegarde : ' + str(e) + ', 5000)')

# Récupérer les paramètres de l'addon
addon = xbmcaddon.Addon('plugin.program.bazoconfigcommu')
startup_delay = int(addon.getSetting('startup_delay'))
backup_interval = int(addon.getSetting('backup_interval'))  # Nouveau paramètre pour l'intervalle de sauvegarde

# Vérifier si le script doit démarrer
if addon.getSetting('script_status') == 'start':
    # Attendre le délai spécifié avant d'exécuter l'action
    time.sleep(startup_delay * 60)  # Convertir le délai de minutes en secondes

    # Exécuter la restauration des données utilisateur au démarrage
    restaurer_donnees_utilisateur()

    # Boucle principale pour exécuter le script avec l'intervalle de sauvegarde spécifié
    while True:
        sauvegarder_donnees_utilisateur()
        time.sleep(backup_interval * 60)  # Attendre l'intervalle de sauvegarde en minutes avant la prochaine sauvegarde
