import xbmc
import xbmcvfs

def main():
    # Supprimer les fichiers de cache vidéo et pastebin
    xbmcvfs.delete('special://home/userdata/addon_data/plugin.video.vstream/video_cache.db')
    xbmcvfs.delete('special://home/userdata/addon_data/plugin.video.vstream/pastebin_cache.db')

    # Exécuter le plugin pour mettre à jour tous les contenus de pastebin
    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.vstream/?site=pastebin&function=refreshAllPaste&title=Mise+a+jour+des+contenus&sFav=refreshAllPaste)')

    # Attendre pendant 4000 millisecondes (4 secondes)
    xbmc.sleep(4000)

    # Recharger le skin
    xbmc.executebuiltin('ReloadSkin')

if __name__ == '__main__':
    main()

