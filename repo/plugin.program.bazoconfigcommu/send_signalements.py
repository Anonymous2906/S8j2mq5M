import xbmc
import xbmcgui
import xbmcvfs
import os
import urllib.request
import urllib.error

class MyKodiScript:

    def __init__(self):
        self.initialize()

    def initialize(self):
        # Chemin vers le fichier texte
        self.file_path = xbmcvfs.translatePath('special://temp/my_text_file.txt')
        xbmc.log(f"Chemin du fichier : {self.file_path}", xbmc.LOGINFO)

        # Vérifier si le fichier existe, sinon le supprimer
        if xbmcvfs.exists(self.file_path):
            xbmc.log("Le fichier existe, suppression du fichier.", xbmc.LOGINFO)
            xbmcvfs.delete(self.file_path)
            xbmc.log("Fichier supprimé.", xbmc.LOGINFO)
        else:
            xbmc.log("Le fichier n'existe pas.", xbmc.LOGINFO)

    def run(self):
        # Boucle pour permettre plusieurs saisies
        while True:
            self.get_text_from_user()
            # Demander à l'utilisateur s'il souhaite continuer
            if not self.ask_to_continue():
                break
        # Envoyer le contenu du fichier via HTTP après toutes les saisies
        self.send_text_via_http()

    def get_text_from_user(self):
        # Ouvrir le clavier virtuel
        keyboard = xbmc.Keyboard('', 'Entrez le texte à envoyer')
        keyboard.doModal()

        # Si l'utilisateur appuie sur 'OK'
        if keyboard.isConfirmed():
            user_input = keyboard.getText()
            xbmc.log(f"Texte saisi : {user_input}", xbmc.LOGINFO)
            self.save_text_to_file(user_input)

    def save_text_to_file(self, text):
        # Vérifier si le répertoire existe, sinon le créer
        directory = os.path.dirname(self.file_path)
        if not xbmcvfs.exists(directory):
            xbmc.log(f"Le répertoire {directory} n'existe pas, création du répertoire.", xbmc.LOGINFO)
            xbmcvfs.mkdirs(directory)

        # Ajouter le texte dans le fichier en utilisant open en mode append
        try:
            xbmc.log("Ouverture du fichier en mode ajout.", xbmc.LOGINFO)
            with open(self.file_path, 'a', encoding='utf-8') as file:
                file.write(text + '\n')
            xbmc.log("Écriture dans le fichier réussie.", xbmc.LOGINFO)

            # Notification de confirmation
            xbmcgui.Dialog().notification('Succès', 'Information enregistrée !', xbmcgui.NOTIFICATION_INFO, 5000)
        except Exception as e:
            xbmc.log(f"Erreur lors de l'écriture du fichier : {str(e)}", xbmc.LOGERROR)
            xbmcgui.Dialog().notification('Erreur', 'Échec de l\'enregistrement du texte.', xbmcgui.NOTIFICATION_ERROR, 5000)

    def send_text_via_http(self):
        # Lire le contenu du fichier texte
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = file.read()
            xbmc.log(f"Contenu du fichier lu : {data}", xbmc.LOGINFO)

            # URL et en-têtes pour la requête HTTP
            url = "https://ntfy.sh/bazoland_signalements"
            headers = {
                "Title": "SIGNALEMENT",
                "Priority": "default",
                "Tags": "rotating_light"
            }

            # Préparer la requête
            req = urllib.request.Request(url, data.encode('utf-8'), headers)
            # Envoyer la requête
            with urllib.request.urlopen(req) as response:
                self.show_notification("SIGNALEMENT", "[COLOR yellowgreen]Envoyée ![/COLOR]")
                xbmc.log("Requête envoyée avec succès.", xbmc.LOGINFO)
        except urllib.error.URLError as e:
            self.show_notification("SIGNALEMENT", "[COLOR red]Non envoyée ![/COLOR]")
            xbmc.log(f"Erreur lors de l'envoi de la requête : {str(e)}", xbmc.LOGERROR)
        except Exception as e:
            xbmc.log(f"Erreur lors de la lecture du fichier ou de l'envoi de la requête : {str(e)}", xbmc.LOGERROR)

    def show_notification(self, title, message):
        # Afficher une notification à l'utilisateur
        xbmcgui.Dialog().notification(title, message, xbmcgui.NOTIFICATION_INFO, 5000)

    def ask_to_continue(self):
        # Demander à l'utilisateur s'il souhaite continuer
        dialog = xbmcgui.Dialog()
        continue_input = dialog.yesno('Continuer', 'Voulez-vous saisir une autre information (N° saison, N° épisode ou autre...) ?')
        xbmc.log(f"L'utilisateur souhaite continuer : {continue_input}", xbmc.LOGINFO)
        return continue_input

def main():
    script = MyKodiScript()
    script.run()

if __name__ == '__main__':
    main()