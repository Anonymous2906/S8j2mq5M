import ftplib
import xbmc
import xbmcaddon
import xbmcgui

def obtenir_pseudo():
    # Obtenez les paramètres du plugin 'plugin.program.bazoconfigcommu'
    addon = xbmcaddon.Addon("plugin.program.bazoconfigcommu")
    pseudo = addon.getSetting("pseudo")
    return pseudo

def creer_dossier_pseudo():
    pseudo = obtenir_pseudo()
    if pseudo:
        try:
            # Connectez-vous au serveur FTP et créez le dossier
            ftp = ftplib.FTP()
            ftp.connect("tobal.duckdns.org", 50)  # Connexion au serveur FTP sur le port 50
            ftp.login("bazoland", "tobalbazo")
            ftp.cwd("/dossier_partager/profils")  # Accéder au dossier partagé des profils
            ftp.mkd(pseudo)
            ftp.quit()

            # Créez les sous-dossiers backup, fav_vst et fav_catchup
            ftp = ftplib.FTP()
            ftp.connect("tobal.duckdns.org", 50)  # Connexion au serveur FTP sur le port 50
            ftp.login("bazoland", "tobalbazo")
            ftp.cwd("/dossier_partager/profils/{}".format(pseudo))  # Accéder au dossier du pseudo
            ftp.mkd("backups")
            ftp.mkd("fav_vst")
            ftp.mkd("fav_catchup")
            ftp.mkd("past_config")
            ftp.quit()

            # Affichez un message de succès
            xbmcgui.Dialog().ok("Succès", "Le dossier '{}' a été créé avec succès.".format(pseudo))
        except ftplib.error_perm as e:
            xbmcgui.Dialog().ok("Erreur", "Impossible de créer le dossier '{}': {}".format(pseudo, e))
        except ftplib.error_temp as e:
            xbmcgui.Dialog().ok("Erreur", "Erreur temporaire lors de la connexion au serveur FTP : {}".format(e))
        except ftplib.all_errors as e:
            xbmcgui.Dialog().ok("Erreur", "Erreur de connexion au serveur FTP : {}".format(e))
    else:
        xbmcgui.Dialog().ok("Erreur", "Aucun pseudo saisi")

creer_dossier_pseudo()
