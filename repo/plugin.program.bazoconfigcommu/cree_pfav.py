import os
import xbmcgui
import xbmc
import ftplib

# Fonction pour se connecter au serveur FTP
def connecter_ftp(hote, port, utilisateur, mot_de_passe):
    try:
        ftp = ftplib.FTP()
        ftp.connect(hote, port)
        ftp.login(utilisateur, mot_de_passe)
        return ftp
    except Exception as e:
        raise Exception("Impossible de se connecter au serveur FTP : {}".format(str(e)))

# Fonction pour créer un dossier pour le profil s'il n'existe pas sur le serveur FTP
def creer_dossier_profil(pseudo, ftp):
    try:
        dossier_profil = "/dossier_partager/Favoris/{}".format(pseudo)
        # Vérifier si le dossier du profil existe, sinon le créer
        if not dossier_profil in ftp.nlst():
            ftp.mkd(dossier_profil)
            xbmcgui.Dialog().ok("Dossier profil créé", "Le dossier pour le pseudo '{}' a été créé avec succès.".format(pseudo))
        else:
            xbmcgui.Dialog().ok("Dossier profil existant", "Le dossier pour le pseudo '{}' existe déjà.".format(pseudo))
    except Exception as e:
        xbmcgui.Dialog().ok("Erreur", "Une erreur est survenue lors de la création du dossier profil : {}".format(str(e)))

# Fonction principale pour demander le pseudo et créer le dossier profil sur le serveur FTP
def main():
    try:
        # Se connecter au serveur FTP
        hote = "tobal.duckdns.org"
        port = 50
        utilisateur = "bazoland"
        mot_de_passe = "tobalbazo"
        ftp = connecter_ftp(hote, port, utilisateur, mot_de_passe)

        pseudo = xbmcgui.Dialog().input("Entrez votre pseudo :")
        if pseudo:
            # Créer le dossier du profil si nécessaire sur le serveur FTP
            creer_dossier_profil(pseudo, ftp)
        else:
            xbmcgui.Dialog().ok("Erreur", "Aucun pseudo saisi.")

        # Déconnexion du serveur FTP
        ftp.quit()
    except Exception as e:
        xbmcgui.Dialog().ok("Erreur", "Une erreur est survenue : {}".format(str(e)))

# Appel de la fonction principale
main()
