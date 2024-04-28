import os
import shutil
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

def restaurer_donnees_utilisateur():
    try:
        # Se connecter au serveur FTP
        hote = "tobal.duckdns.org"
        port = 50
        utilisateur = "bazoland"
        mot_de_passe = "tobalbazo"
        ftp = connecter_ftp(hote, port, utilisateur, mot_de_passe)

        # Récupérer le pseudo à partir des paramètres de l'addon
        addon = xbmcaddon.Addon('plugin.program.bazoconfigcommu')
        pseudo = addon.getSetting('pseudo')

        if pseudo:
            source_path = "/dossier_partager/profils/{}/fav_vst/".format(pseudo)
            destination_path = xbmcvfs.translatePath("special://home/userdata/addon_data/plugin.video.vstream/")

            # Vérifier si le dossier source existe sur le serveur FTP
            if not ftp.nlst(source_path):
                xbmcgui.Dialog().ok("Erreur", "Le dossier source n'existe pas sur le serveur FTP.")
                return

            # Télécharger le fichier vstream.db depuis le serveur FTP
            vstream_db_path = os.path.join(destination_path, "vstream.db")
            try:
                with open(vstream_db_path, 'wb') as f:
                    ftp.retrbinary('RETR {}'.format(os.path.join(source_path, "vstream.db")), f.write)
                xbmcgui.Dialog().ok("Restauration terminée", "Le fichier vstream.db a été restauré pour l'utilisateur {}".format(pseudo))
            except Exception as e:
                xbmcgui.Dialog().ok("Erreur", "Une erreur est survenue lors de la restauration : {}".format(str(e)))
        else:
            xbmcgui.Dialog().ok("Erreur", "Aucun pseudo saisi")

        # Déconnexion du serveur FTP
        ftp.quit()

        # Actualiser le skin
        xbmc.executebuiltin("ReloadSkin()")
    except Exception as e:
        xbmcgui.Dialog().ok("Erreur", "Une erreur est survenue : {}".format(str(e)))

restaurer_donnees_utilisateur()
