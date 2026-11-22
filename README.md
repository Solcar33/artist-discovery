# Artist Discovery

Chaque semaine, ce projet me propose **trois artistes à découvrir** à partir de mon historique d'écoute Spotify, et publie une page de type blog : présentation, chiffres, un album pour commencer et des liens d'écoute.

Site : https://solcar33.github.io/artist-discovery/

> Projet d'apprentissage. Je le construis étape par étape et je note chaque étape dans [`notes.md`](notes.md).

## Comment ça marche

1. Mon historique Spotify est résumé en un **profil** : mes 50 artistes les plus écoutés et la liste des artistes que je connais déjà.
2. Pour chaque favori, **Last.fm** donne des artistes proches. Les scores sont cumulés et pondérés par mon nombre d'écoutes.
3. Trois artistes sont tirés parmi les meilleurs candidats, avec des styles différents. Le tirage est fixé par la semaine, et les artistes déjà présentés sont exclus.
4. Chaque fiche est complétée avec Last.fm, **MusicBrainz** (liens d'écoute) et **Wikipedia** (présentation).
5. Les fiches sont enregistrées en JSON (`content/`), puis transformées en pages HTML avec **Jinja2** (`docs/`).
6. **GitHub Actions** relance tout chaque lundi et **GitHub Pages** publie le site.

## Structure du projet

```
src/        code Python : profil, appels aux API, fiches, génération du site
templates/  modèles HTML (Jinja2)
static/     feuille de style CSS
content/    une fiche JSON par semaine
docs/       site généré, publié par GitHub Pages
scripts/    note.sh, pour tenir le journal d'apprentissage
notes.md    journal d'apprentissage
```

## Confidentialité

Ni mon historique Spotify ni mes clés ne sont dans le dépôt. Le dossier `data/` et le fichier `.env` sont ignorés par Git, et le workflow lit mon profil et ma clé Last.fm dans deux **secrets GitHub**.

## Lancer le projet chez soi

Il faut Python, un export de ses données Spotify placé dans `data/`, et une clé API Last.fm.

```bash
python -m venv .venv
source .venv/Scripts/activate          # Windows (Git Bash)
python -m pip install -r requirements.txt
echo "LASTFM_API_KEY=ta_cle" > .env
python src/fiche.py                    # génère la semaine dans content/
python src/build_site.py               # construit le site dans docs/
```

## Limites connues

- Les auditeurs affichés viennent de Last.fm : ce ne sont pas les « auditeurs mensuels » de Spotify.
- Le profil est un instantané de mes écoutes, à ré-exporter de temps en temps.
- La similarité de Last.fm est statistique : elle peut proposer le projet solo d'un membre d'un groupe que j'écoute déjà.

## Sources et crédits

- [Last.fm](https://www.last.fm) : artistes proches, chiffres, genres, albums.
- [MusicBrainz](https://musicbrainz.org) : liens d'écoute et références.
- [Wikipedia](https://www.wikipedia.org) : présentations des artistes, sous licence [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), via [Wikidata](https://www.wikidata.org).

## Suite

Une fois ma formation commencée, ajouter de l'IA pour rédiger la présentation et expliquer pourquoi chaque artiste m'est proposé.