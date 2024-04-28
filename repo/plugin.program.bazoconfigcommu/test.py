import os
import shutil
import zipfile
import xbmcgui
import xbmcvfs
import xbmc
import ftplib
import xbmcaddon

def connecter_ftp(hote, port, utilisateur, mot_de_passe):
    try:
        ftp = ftplib.FTP()
        ftp.connect(hote, port)
        ftp.login(utilisateur, mot_de_passe)
        return ftp
    except Exception as e:
        raise Exception("Impossible de se connecter au serveur FTP : {}".format(str(e)))

def obtenir_pseudo():
    # Obtenez les paramètres du plugin 'plugin.program.bazoconfigcommu'
    addon = xbmcaddon.Addon("plugin.program.bazoconfigcommu")
    pseudo = addon.getSetting("pseudo")
    return pseudo

def creer_dossier_backups(ftp, destination_path):
    if not ftp:
        raise Exception("Connexion FTP non établie")

    try:
        # Créer le dossier de destination s'il n'existe pas
        ftp.mkd(destination_path)
    except ftplib.error_perm as e:
        # Le dossier existe déjà, c'est normal, pas besoin de le créer
        pass

def sauvegarder_donnees_utilisateur():
    try:
        # Se connecter au serveur FTP
        hote = "tobal.duckdns.org"
        port = 50
        utilisateur = "bazoland"
        mot_de_passe = "tobalbazo"
        ftp = connecter_ftp(hote, port, utilisateur, mot_de_passe)

        # Désactiver l'addon autowidget
        xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "plugin.program.autowidget", "enabled": false }}')
        xbmc.sleep(5000)

        pseudo = obtenir_pseudo()
        if pseudo:
            source_path = xbmcvfs.translatePath("special://home/userdata/addon_data")
            destination_path = "/dossier_partager/profils/{}/backups/".format(pseudo)

            creer_dossier_backups(ftp, destination_path)

            # Chemin de fichier pour le zip
            zip_file_path = os.path.join(xbmcvfs.translatePath('special://temp'), "{}_addon_data.zip".format(pseudo))

            try:
                # Créer un fichier zip contenant le dossier addon_data
                with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(source_path):
                        for file in files:
                            source_file_path = os.path.join(root, file)
                            zipf.write(source_file_path, os.path.relpath(source_file_path, source_path))

                # Transférer le fichier zip vers le serveur FTP
                with open(zip_file_path, 'rb') as f:
                    ftp.storbinary('STOR {}'.format(os.path.join(destination_path, "{}_addon_data.zip".format(pseudo))), f)

                xbmcgui.Dialog().ok("Sauvegarde terminée", "Les données ont été sauvegardées pour l'utilisateur {}".format(pseudo))
            except Exception as e:
                xbmcgui.Dialog().ok("Erreur", "Une erreur est survenue lors de la sauvegarde : {}".format(str(e)))
            finally:
                # Supprimer le fichier zip temporaire
                if xbmcvfs.exists(zip_file_path):
                    xbmcvfs.delete(zip_file_path)
        else:
            xbmcgui.Dialog().ok("Erreur", "Aucun pseudo saisi")

        # Réactiver l'addon autowidget
        xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "plugin.program.autowidget", "enabled": true }}')
        xbmc.sleep(5000)
        xbmc.executebuiltin("Notification(TERMINE , ...)")

        # Déconnexion du serveur FTP
        ftp.quit()
    except Exception as e:
        xbmcgui.Dialog().ok("Erreur", "Une erreur est survenue lors de la connexion au serveur FTP : {}".format(str(e)))

sauvegarder_donnees_utilisateur()
