import os
import ftplib
import xbmcgui
import xbmc
import xbmcaddon
import xbmcvfs

# Fonction pour sauvegarde automatique
def sav_auto():
    xbmc.executebuiltin("Notification(SAUVEGARDE,des fav)")
    xbmc.sleep(2000)
    import fav  # Assurez-vous que ce module est accessible depuis votre script Kodi
    xbmc.sleep(8000)
    xbmc.executebuiltin("Notification(FERMETURE,de kodi)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('Quit')
