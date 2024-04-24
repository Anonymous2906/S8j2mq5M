import requests
import re

def get_links_from_rentry(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        # Expression régulière pour trouver les liens dans le HTML
        link_regex = r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"'
        links = re.findall(link_regex, html_content)
        return links
    else:
        xbmc.log(f"Erreur lors de la récupération de la page {url}: {response.status_code}")
        return []

def main():
    addon = xbmcaddon.Addon()
    rentry_code = addon.getSetting('rentry_code')

    if not rentry_code:
        xbmc.log("Veuillez fournir un code rentry dans les paramètres de l'addon.")
        return

    url_rentry = f"https://rentry.co/{rentry_code}"
    links = get_links_from_rentry(url_rentry)
    for link in links:
        xbmc.log(f"URL trouvée : {link}")

if __name__ == '__main__':
    main()
