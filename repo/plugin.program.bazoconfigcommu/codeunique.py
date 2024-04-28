import xbmcaddon
import xbmc
import requests
import re

def code():
    settings_to_update = {
        'code_hk3': 'numAnotepad0',
        'code_config_vt': 'vst',
        'code_db_torrent': 'dbtd',
        'code_iptvx1': 'iptvx1',
        'code_iptvx2': 'iptvx2',
        'code_iptvx3': 'iptvx3',
        'code_m3u_foxx': 'codem3u',
        'code_m3u_vavoo': 'codem3u2',
    }

    addon = xbmcaddon.Addon("plugin.program.bazoconfigcommu")
    numAnotepad0 = addon.getSetting("cu")
    if not numAnotepad0:
        xbmc.executebuiltin("Notification(Aucune clé trouvée dans les paramètres de l'addon, time=5000)")
        return

    rentry_url = f"https://rentry.co/{numAnotepad0.strip()}/raw"

    try:
        response = requests.get(rentry_url)
        if response.status_code == 200:
            key_rentry = response.text.strip()
            if key_rentry:
                key_values = key_rentry.split('\n')
                for key_value in key_values:
                    key, value = key_value.split('=')
                    key = key.strip().lower()
                    value = value.strip()

                    if key in settings_to_update:
                        try:
                            addon.setSetting(id=settings_to_update[key], value=value)
                            xbmc.executebuiltin(f"Notification({key.capitalize()} ajouté(e), ok)")
                        except Exception as e:
                            xbmc.executebuiltin(f"Notification(Erreur HK: {str(e)}, time=5000)")
                    else:
                        xbmc.executebuiltin(f"Notification(Clé inconnue : {key}, time=5000)")
            else:
                xbmc.executebuiltin("Notification(Aucune clé rentry.co trouvée, time=5000)")
        else:
            xbmc.executebuiltin("Notification(Échec de récupération de la clé depuis rentry.co, time=5000)")
    except Exception as e:
        xbmc.executebuiltin(f"Notification(Erreur lors de la récupération de la clé depuis rentry.co : {str(e)}, time=5000)")

if __name__ == "__main__":
    code()
