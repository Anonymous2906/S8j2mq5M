import xbmcaddon
import xbmc
import requests

def code():
    settings_to_update = {
        'dossier1': 'pastebin_label_1',
        'past1': 'pastebin_id_1',
        'dossier2': 'pastebin_label_2',
        'past2': 'pastebin_id_2',
        'dossier3': 'pastebin_label_3',
        'past3': 'pastebin_id_3',
        'dossier4': 'pastebin_label_4',
        'past4': 'pastebin_id_4',
        'dossier5': 'pastebin_label_5',
        'past5': 'pastebin_id_5',
        'dossier6': 'pastebin_label_6',
        'past6': 'pastebin_id_6',
        'dossier7': 'pastebin_label_7',
        'past7': 'pastebin_id_7',
        'dossier8': 'bazoland_label_1',
        'past8': 'bazoland_id_1'
    }

    key_alldebrid = extract_anotpadall()

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
                    xbmc.executebuiltin(f"Notification({key.capitalize()} ajouté(e), ok)")
                except Exception as e:
                    xbmc.executebuiltin(f"Notification(Erreur : {str(e)}, time=5000)")
            else:
                xbmc.executebuiltin(f"Notification(Clé inconnue : {key}, time=5000)")
    else:
        xbmc.executebuiltin("Notification(Aucune clé Anotepad trouvée, time=5000)")

def extract_anotpadall():
    bazoconfigcommu_addon = xbmcaddon.Addon("plugin.program.bazoconfigcommu")
    dbtd = bazoconfigcommu_addon.getSetting("dbtd")
    pseudo = bazoconfigcommu_addon.getSetting("pseudo")

    if not dbtd:
        xbmc.executebuiltin("Notification(Aucune clé dbtd trouvée dans les paramètres de l'addon, time=5000)")
        return None

    if not pseudo:
        xbmc.executebuiltin("Notification(Aucun pseudo trouvé dans les paramètres de l'addon, time=5000)")
        return None

    url = f"http://tobal.duckdns.org/profils/{pseudo}/past_config/{dbtd.strip()}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.strip()
        else:
            xbmc.executebuiltin("Notification(Échec de récupération de la clé depuis Bazoland, time=5000)")
            return None
    except Exception as e:
        xbmc.executebuiltin(f"Notification(Erreur lors de l'extraction du contenu depuis Bazoland : {str(e)}, time=5000)")
        return None

if __name__ == "__main__":
    code()
