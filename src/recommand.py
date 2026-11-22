import random
import time
from collections import defaultdict
from datetime import date

from history import load_history, get_top_artists, get_known_artists
from lastfm import get_similar_artists

# Alias de groupes déjà connus, en attendant MusicBrainz (en minuscules)
A_IGNORER = {"bob marley", "dub incorporation"}


def get_candidates(nb_favoris=50, nb_similaires=20):
    """Classe les artistes à découvrir à partir de mes favoris."""
    ecoutes = load_history()
    connus = {nom.lower() for nom in get_known_artists(ecoutes)} | A_IGNORER

    scores = defaultdict(float)
    liens = defaultdict(list)

    for nom, nb in get_top_artists(ecoutes, nb_favoris):
        try:
            similaires = get_similar_artists(nom, nb_similaires)
        except RuntimeError as erreur:
            print(f"Ignoré : {nom} ({erreur})")
            continue

        for similaire in similaires:
            candidat = similaire["name"]
            if candidat.lower() in connus:
                continue
            scores[candidat] += float(similaire["match"]) * nb
            liens[candidat].append(nom)

        time.sleep(0.25)

    classement = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [(candidat, score, liens[candidat]) for candidat, score in classement]


def pick_artist_of_the_week(candidats, pool=30, exclus=()):
    """Tire un artiste parmi les `pool` meilleurs candidats non exclus.
    Le tirage dépend de la semaine : relancer donne le même résultat."""
    disponibles = [c for c in candidats if c[0].lower() not in exclus]
    annee, semaine, _ = date.today().isocalendar()
    hasard = random.Random(f"{annee}-W{semaine}")
    return hasard.choice(disponibles[:pool])


if __name__ == "__main__":
    candidats = get_candidates()
    nom, score, favoris = pick_artist_of_the_week(candidats)
    print(f"Artiste de la semaine : {nom}")
    print(f"Proche de : {', '.join(favoris)}")