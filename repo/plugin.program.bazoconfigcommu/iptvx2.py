import xbmcaddon
import xbmc
import requests
import re

def code():
    settings_to_update = {
        'iptv': 'iptv',
        'adr_xt2': 'serverx1',
        'u_xt2': 'userx1',
        'p_xt2': 'passx1',
        'n_xt2': 'nomx1',
    }

    key_alldebrid = iptvx1()

    if key_alldebrid:
        key_values = key_alldebrid.split('\n')
        for key_value in key_values:
            key, value = key_value.split('=')
            key = key.strip().lower()
            value = value.strip()

            if key in settings_to_update:
                try:
                    addon = xbmcaddon.Addon("plugin.video.sendtokodiU2P")
                    addon.setSetting(id=settings_to_update[key], value=value)
                    xbmc.executebuiltin(f"Notification({key.capitalize()} ajouté(e),ok)")
                except Exception as e:
                    xbmc.executebuiltin(f"Notification(Erreur HK: {str(e)}, time=5000)")
            else:
                xbmc.executebuiltin(f"Notification(Clé inconnue : {key}, time=5000)")
    else:
        xbmc.executebuiltin("Notification(Aucune clé Anotepad trouvée, time=5000)")

def iptvx1():
    addon = xbmcaddon.Addon()
    iptvx1 = addon.getSetting("iptvx2")
    url = f"https://rentry.co/{iptvx1.strip()}/raw"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.strip()
        else:
            xbmc.executebuiltin("Notification(Échec de récupération de la clé depuis rentry.co, time=5000)")
            return None
    except Exception as e:
        xbmc.executebuiltin(f"Notification(Erreur lors de l'extraction du contenu depuis rentry.co : {str(e)}, time=5000)")
        return None

if __name__ == "__main__":
    code()
