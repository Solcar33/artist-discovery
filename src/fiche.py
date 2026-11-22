import json
from datetime import date
from pathlib import Path

import requests

from lastfm import get_artist_info, get_top_album
from musicbrainz import find_artist, get_artist_links
from recommand import get_candidates, pick_artists_of_the_week
from wikipedia import get_wikipedia_summary

CONTENT_DIR = Path("content")


def _essayer(source, fonction, *args):
    """Appelle 'fonction'. Si la source est en panne, renvoie None au lieu de planter."""
    try:
        return fonction(*args)
    except RuntimeError as erreur:  # nos propres messages : sans clés
        print(f"{source} indisponible : {erreur}")
    except requests.RequestException as erreur:
        # on affiche que le type : le détail contient l'URL, donc la clé Last.fm
        print(f"{source} indisponible : {type(erreur).__name__}")
    return None


def build_fiche(nom, favoris):
    """Assemble la fiche d'un artiste à partir de toutes les sources."""
    fiche = {"nom": nom, "favoris": favoris}

    info = _essayer("Last.fm", get_artist_info, nom)
    fiche["lastfm"] = info
    fiche["album"] = _essayer("Last.fm (album)", get_top_album, nom)

    mbid = info["mbid"] if info else ""
    if not mbid:
        trouve = _essayer("MusicBrainz (recherche)", find_artist, nom)
        if trouve and trouve["score"] >= 90:
            mbid = trouve["id"]

    liens = (
        _essayer("MusicBrainz (liens)", get_artist_links, mbid)
        if mbid
        else None
    )
    fiche["liens"] = liens or {}

    fiche["wikipedia"] = None
    if fiche["liens"].get("wikidata"):
        qid = fiche["liens"]["wikidata"][0].rsplit("/", 1)[-1]
        resume = _essayer("Wikipedia", get_wikipedia_summary, qid)
        if resume:
            texte, url, langue = resume
            fiche["wikipedia"] = {"texte": texte, "url": url, "langue": langue}
    return fiche


def _id_semaine():
    """Identifiant de la semaine en cours, par exemple 2026-W47."""
    annee, semaine, _ = date.today().isocalendar()
    return f"{annee}-W{semaine:02d}"


def _fichier_semaine():
    """Nom du fichier de la semaine en cours, par exemple 2026-W47.json."""
    return f"{_id_semaine()}.json"


def get_past_artists():
    """Noms (en minuscules) des artistes présentés les semaines précédentes."""
    deja_vus = set()
    for chemin in CONTENT_DIR.glob("*.json"):
        if chemin.name.lower() == _fichier_semaine().lower():
            continue  # la semaine en cours n'est pas exclue d'elle-même
        with open(chemin, encoding="utf-8") as f:
            data = json.load(f)
        # ancien format : une seule fiche ; nouveau format : une liste "decouvertes"
        for fiche in data.get("decouvertes", [data]):
            deja_vus.add(fiche["nom"].lower())
    return deja_vus


def save_week(semaine):
    """Enregistre la semaine dans content/ sous le nom AAAA-Wss.json."""
    CONTENT_DIR.mkdir(exist_ok=True)
    chemin = CONTENT_DIR / _fichier_semaine()
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(semaine, f, ensure_ascii=False, indent=2)
    return chemin


if __name__ == "__main__":
    candidats = get_candidates()
    choisis = pick_artists_of_the_week(candidats, exclus=get_past_artists())
    if not choisis:
        raise SystemExit("Aucune découverte générée : vérifie les secrets et les sources")
    fiches = [build_fiche(nom, favoris) for nom, score, favoris in choisis]
    semaine = {
        "semaine": _id_semaine(),
        "date": date.today().isoformat(),
        "decouvertes": fiches,
    }
    print("Semaine enregistrée :", save_week(semaine))