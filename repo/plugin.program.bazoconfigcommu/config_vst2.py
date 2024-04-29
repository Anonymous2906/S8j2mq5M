import xbmcaddon
import xbmc
import requests

def code():
    settings_to_update = {
        'hpast': 'pastebin_url',
        'bazoland': 'bazoland_url',
        'aalldeb': 'hoster_alldebrid_premium',
        'talldeb': 'hoster_alldebrid_token',
    }

    key_alldebrid = extract_rentry()

    if key_alldebrid:
        key_values = key_alldebrid.split('\n')
        for key_value in key_values:
            key, value = key_value.split('=')
            key = key.strip().lower()
            value = value.strip()

            if key in settings_to_update:
                try:
                    addon = xbmcaddon.Addon("plugin.video.vstream")
                    addon.setSetting(id=settings_to_update[key], value=value)
                    xbmc.executebuiltin(f"Notification({key.capitalize()} ajouté(e),ok)")
                except Exception as e:
                    xbmc.executebuiltin(f"Notification(Erreur HK: {str(e)}, time=5000)")
            else:
                xbmc.executebuiltin(f"Notification(Clé inconnue : {key}, time=5000)")
    else:
        xbmc.executebuiltin("Notification(Aucune clé Rentry.co trouvée, time=5000)")

def extract_rentry():
    addon = xbmcaddon.Addon()
    num_rentry = addon.getSetting("vst")
    url = f"https://rentry.co/{num_rentry.strip()}/raw"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            key_rentry = response.text.strip()
            return key_rentry
        else:
            xbmc.executebuiltin("Notification(Échec de récupération de la clé depuis Rentry.co, time=5000)")
            return None
    except Exception as e:
        xbmc.executebuiltin(f"Notification(Erreur lors de la récupération de la clé depuis Rentry.co : {str(e)}, time=5000)")
        return None

if __name__ == "__main__":
    code()
