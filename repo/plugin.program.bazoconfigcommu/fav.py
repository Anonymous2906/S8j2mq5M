import os
import shutil
import zipfile
import xbmcgui
import xbmcvfs
import xbmc
import ftplib

def connecter_ftp(hote, port, utilisateur, mot_de_passe):
    try:
        ftp = ftplib.FTP()
        ftp.connect(hote, port)
        ftp.login(utilisateur, mot_de_passe)
        return ftp
    except Exception as e:
        raise Exception("Impossible de se connecter au serveur FTP : {}".format(str(e)))

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

        pseudo = xbmcgui.Dialog().input("Entrez votre pseudo :")
        if pseudo:
            source_path = xbmcvfs.translatePath("special://home/userdata/addon_data/plugin.video.vstream/")
            destination_path = "/dossier_partager/Favoris/{}/".format(pseudo)

            try:
                # Créer le dossier de destination s'il n'existe pas
                ftp.mkd(destination_path)
            except ftplib.error_perm as e:
                # Le dossier existe déjà, c'est normal, pas besoin de le créer
                pass

            # Chemin du fichier vstream.db
            vstream_db_path = os.path.join(source_path, "vstream.db")

            try:
                # Transférer le fichier vstream.db vers le serveur FTP
                with open(vstream_db_path, 'rb') as f:
                    ftp.storbinary('STOR {}'.format(os.path.join(destination_path, "vstream.db")), f)

                xbmcgui.Dialog().ok("Sauvegarde terminée", "Le fichier vstream.db a été sauvegardé dans le dossier Favoris pour l'utilisateur {}".format(pseudo))
            except Exception as e:
                xbmcgui.Dialog().ok("Erreur", "Une erreur est survenue lors de la sauvegarde : {}".format(str(e)))
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
