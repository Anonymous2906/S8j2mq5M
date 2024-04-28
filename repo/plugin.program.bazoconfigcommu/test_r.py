import os
import xbmcgui
import xbmcvfs
import xbmc
import zipfile
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
    addon = xbmcaddon.Addon("plugin.program.bazoconfigcommu")
    pseudo = addon.getSetting("pseudo")
    return pseudo

def restaurer_donnees_utilisateur():
    try:
        pseudo = obtenir_pseudo()
        if pseudo:
            destination_path = xbmcvfs.translatePath("special://home/userdata/addon_data")

            # Se connecter au serveur FTP
            hote = "tobal.duckdns.org"
            port = 50
            utilisateur = "bazoland"
            mot_de_passe = "tobalbazo"
            ftp = connecter_ftp(hote, port, utilisateur, mot_de_passe)

            # Désactiver les addons
            addons_a_desactiver = ["plugin.program.autowidget", "plugin.video.sendtokodiU2P", "plugin.video.vstream"]
            for addonid in addons_a_desactiver:
                xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "%s", "enabled": false }}' % addonid)

            xbmc.sleep(5000)

            source_path = "/dossier_partager/profils/{}/backups/{}_addon_data.zip".format(pseudo, pseudo)

            # Vérifier si le fichier zip de sauvegarde existe sur le serveur FTP
            if not ftp.nlst(source_path):
                xbmcgui.Dialog().ok("Erreur", "Aucune sauvegarde trouvée pour l'utilisateur {}".format(pseudo))
                return

            # Chemin de fichier pour le zip téléchargé
            zip_file_path = os.path.join(xbmcvfs.translatePath('special://temp'), "{}_addon_data.zip".format(pseudo))

            try:
                # Télécharger le fichier zip depuis le serveur FTP
                with open(zip_file_path, 'wb') as f:
                    ftp.retrbinary('RETR {}'.format(source_path), f.write)

                # Extraire le contenu du fichier zip vers le dossier addon_data dans userdata
                with zipfile.ZipFile(zip_file_path, 'r') as zipf:
                    zipf.extractall(destination_path)

                xbmcgui.Dialog().ok("Restauration terminée", "Les données ont été restaurées pour l'utilisateur {}".format(pseudo))
            except Exception as e:
                xbmcgui.Dialog().ok("Erreur", "Une erreur est survenue lors de la restauration : {}".format(str(e)))
            finally:
                # Supprimer le fichier zip temporaire
                if xbmcvfs.exists(zip_file_path):
                    xbmcvfs.delete(zip_file_path)

            # Réactiver les addons
            for addonid in addons_a_desactiver:
                xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "%s", "enabled": true }}' % addonid)

            xbmc.sleep(5000)
            xbmc.executebuiltin("Notification(TERMINE , ...)")

            # Déconnexion du serveur FTP
            ftp.quit()
        else:
            xbmcgui.Dialog().ok("Erreur", "Aucun pseudo saisi")

    except Exception as e:
        xbmcgui.Dialog().ok("Erreur", "Une erreur est survenue : {}".format(str(e)))

restaurer_donnees_utilisateur()
