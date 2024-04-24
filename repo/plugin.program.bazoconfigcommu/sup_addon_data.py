import os
import shutil
import xbmcgui
import xbmcvfs
import xbmc

def supprimer_dossiers():
    # Dossiers à supprimer
    dossiers_a_supprimer = [
        "addon_data/iconvod",
        "addon_data/plugin.program.autowidget",
        "addon_data/plugin.video.sendtokodiU2P",
        "addon_data/plugin.video.vstream",
        "addon_data/script.skinshortcuts"
    ]

    for dossier in dossiers_a_supprimer:
        dir_path = xbmcvfs.translatePath("special://home/userdata/{}".format(dossier))
        try:
            shutil.rmtree(dir_path)
            xbmc.log("Dossier {} supprimé avec succès.".format(dossier))
        except Exception as e:
            xbmc.log("Erreur lors de la suppression du dossier {} : {}".format(dossier, str(e)))
        xbmc.sleep(1000)

supprimer_dossiers()
