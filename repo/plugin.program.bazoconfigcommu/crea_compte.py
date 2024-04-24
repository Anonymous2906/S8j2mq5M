import ftplib
import xbmcgui

def creer_dossier_pseudo():
    pseudo = xbmcgui.Dialog().input("Entrez votre pseudo :")
    if pseudo:
        try:
            ftp = ftplib.FTP()
            ftp.connect("tobal.duckdns.org", 50)  # Connexion au serveur FTP sur le port 50
            ftp.login("bazoland", "tobalbazo")
            ftp.cwd("/dossier_partager/Backups")
            ftp.mkd(pseudo)
            ftp.quit()
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
