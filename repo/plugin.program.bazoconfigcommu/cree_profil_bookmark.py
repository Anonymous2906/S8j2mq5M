import ftplib
import xbmc
import xbmcaddon
import xbmcvfs
import shutil
import os

def obtenir_pseudo():
    # Obtenez les paramètres du plugin 'plugin.program.bazoconfigcommu'
    addon = xbmcaddon.Addon("plugin.program.bazoconfigcommu")
    pseudo = addon.getSetting("pseudo")
    return pseudo

def copier_fichiers_ftp(ftp, local_path, remote_path):
    with open(local_path, 'rb') as file:
        ftp.storbinary(f'STOR {remote_path}', file)

def creer_dossier_pseudo():
    pseudo = obtenir_pseudo()
    if pseudo:
        try:
            # Connectez-vous au serveur FTP et créez le dossier
            with ftplib.FTP() as ftp:
                ftp.connect("tobal.duckdns.org", 50)  # Connexion au serveur FTP sur le port 21
                ftp.login("tobal", "pqx862g5")
                ftp.cwd("/dossier_partager/bookmark_online/html/profils")  # Accéder au dossier partagé des profils

                # Créer le dossier pour le pseudo
                try:
                    ftp.mkd(pseudo)
                except ftplib.error_perm:
                    xbmc.executebuiltin('Notification(SYNCHRONISATION, Le profil "{}" est actif.)'.format(pseudo))
                    return

                # Créer les sous-dossiers
                for subfolder in ["backup", "fav_catchup", "past_config"]:
                    try:
                        ftp.mkd(f"{pseudo}/{subfolder}")
                    except ftplib.error_perm:
                        xbmc.executebuiltin('Notification(Erreur, Le dossier "{}" existe déjà.)'.format(subfolder))

                # Définir les chemins des fichiers locaux
                requete_path = xbmcvfs.translatePath("special://home/addons/plugin.program.bazoconfigcommu/resources/requete.php")
                vstream_path = xbmcvfs.translatePath("special://home/addons/plugin.program.bazoconfigcommu/vstream.db")

                # Copier les fichiers dans le dossier créé
                ftp.cwd(pseudo)
                copier_fichiers_ftp(ftp, requete_path, "requete.php")
                copier_fichiers_ftp(ftp, vstream_path, "vstream.db")

            # Affichez un message de succès
            xbmc.executebuiltin('Notification(ACTIVATION, Le profil "{}" a été activé pour la synchronisation.)'.format(pseudo))
        except ftplib.error_temp as e:
            xbmc.executebuiltin('Notification(Erreur, Erreur temporaire lors de la connexion au serveur FTP : {})'.format(e))
        except ftplib.all_errors as e:
            xbmc.executebuiltin('Notification(Erreur, Erreur de connexion au serveur FTP : {})'.format(e))
    else:
        xbmc.executebuiltin('Notification(Erreur, Aucun pseudo saisi)')

# Appel de la fonction pour créer le dossier et copier les fichiers
creer_dossier_pseudo()
