import xbmcaddon
import xbmc
import requests

def iptvx1():
    # Obtenir l'addon Kodi
    addon = xbmcaddon.Addon()
    # Obtenir la valeur du paramètre iptvx1 depuis les paramètres de l'addon Kodi
    iptvx1 = addon.getSetting("iptvx1")
    # Construire l'URL pour obtenir la clé depuis le serveur
    url = f"http://tobal.duckdns.org:805/api/public/dl/{iptvx1.strip()}?inline=true"

    try:
        # Effectuer une requête pour obtenir la clé
        response = requests.get(url)
        if response.status_code == 200:
            # Retourner le texte de la réponse (la clé)
            return response.text.strip()
        else:
            # Si la requête échoue, afficher une notification
            xbmc.executebuiltin("Notification(Échec de récupération de la clé depuis Bazoland, time=5000)")
            return None
    except Exception as e:
        # Si une exception se produit lors de la requête, afficher une notification avec l'erreur
        xbmc.executebuiltin(f"Notification(Erreur lors de l'extraction du contenu depuis Bazoland : {str(e)}, time=5000)")
        return None

def code():
    # Dictionnaire des paramètres à mettre à jour dans l'addon Kodi
    settings_to_update = {
        'iptv': 'iptv',
        'adr_xt1': 'serverx1',
        'u_xt1': 'userx1',
        'p_xt1': 'passx1',
        'n_xt1': 'nomx1',
    }

    # Obtenir la clé depuis le serveur
    key_alldebrid = iptvx1()

    if key_alldebrid:
        # Si la clé est obtenue avec succès
        key_values = key_alldebrid.split('\n')
        for key_value in key_values:
            key, value = key_value.split('=')
            key = key.strip().lower()
            value = value.strip()

            if key in settings_to_update:
                try:
                    # Mettre à jour les paramètres de l'addon Kodi avec les valeurs obtenues
                    addon = xbmcaddon.Addon("plugin.video.sendtokodiU2P")
                    addon.setSetting(id=settings_to_update[key], value=value)
                    xbmc.executebuiltin(f"Notification({key.capitalize()} ajouté(e),ok)")
                except Exception as e:
                    # En cas d'erreur lors de la mise à jour des paramètres, afficher une notification avec l'erreur
                    xbmc.executebuiltin(f"Notification(Erreur HK: {str(e)}, time=5000)")
            else:
                # Si la clé n'est pas reconnue, afficher une notification
                xbmc.executebuiltin(f"Notification(Clé inconnue : {key}, time=5000)")
    else:
        # Si aucune clé n'est obtenue, afficher une notification
        xbmc.executebuiltin("Notification(Aucune clé Anotepad trouvée, time=5000)")

if __name__ == "__main__":
    # Exécuter la fonction principale
    code()
