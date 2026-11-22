from urllib.parse import quote

import requests

HEADERS = {"User-Agent": "artist-discovery/0.1 (projet d'apprentissage)"}


def get_wikipedia_summary(qid, langues=("fr", "en")):
    """Renvoie (texte, url, langue) depuis Wikipedia, ou None si introuvable."""
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
    reponse = requests.get(url, headers=HEADERS, timeout=10)
    if reponse.status_code != 200:
        return None
    sitelinks = reponse.json()["entities"][qid].get("sitelinks", {})
    for langue in langues:
        lien = sitelinks.get(f"{langue}wiki")
        if not lien:
            continue
        titre = quote(lien["title"].replace(" ", "_"), safe="")
        resume = requests.get(
            f"https://{langue}.wikipedia.org/api/rest_v1/page/summary/{titre}",
            headers=HEADERS,
            timeout=10,
        )
        if resume.status_code == 200:
            data = resume.json()
            return data["extract"], data["content_urls"]["desktop"]["page"], langue
    return None


if __name__ == "__main__":
    from musicbrainz import find_artist, get_artist_links

    artiste = find_artist("Althea & Donna")
    liens = get_artist_links(artiste["id"])
    urls_wikidata = liens.get("wikidata", [])

    if not urls_wikidata:
        print("Pas d'identifiant Wikidata pour cet artiste")
    else:
        qid = urls_wikidata[0].rsplit("/", 1)[-1]
        print("Identifiant Wikidata :", qid)
        resultat = get_wikipedia_summary(qid)
        if resultat:
            texte, lien, langue = resultat
            print(langue, lien)
            print(texte[:300])
        else:
            print("Aucun article Wikipedia trouvé")