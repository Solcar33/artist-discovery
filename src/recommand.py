import time
from collections import defaultdict

from history import load_history, get_top_artists, get_known_artists
from lastfm import get_similar_artists

ecoutes = load_history()
connus = {nom.lower() for nom in get_known_artists(ecoutes)}
top = get_top_artists(ecoutes, 50)

scores = defaultdict(float)
liens = defaultdict(list)

for nom, nb in top:
    try:
        similaires = get_similar_artists(nom,20)
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
for candidat, score in classement[:10]:
    print(f"{score:8.1f}  {candidat}  <-  {', '.join(liens[candidat][:3])}")
