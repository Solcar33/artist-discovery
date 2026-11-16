# Notes de projet : artist-discovery

## Modèle d'entrée (à copier pour chaque étape)

### [Date] Étape X.Y : titre
- **Ce que j'ai fait :**
- **Pourquoi :**
- **Commande ou code clé :**
- **Ce que j'ai appris :**
- **Question restante :**

---

## Journal

### 2026-11-16 Étape 0 : fondations
- **Ce que j'ai fait :** créé le dossier `artist-discovery`, `git init`, dossiers `data/` et `src/`, `.gitignore`, venv Python `.venv`, script `scripts/note.sh`, fichier `CLAUDE.md`, puis dépôt GitHub privé relié avec `git push`.
- **Pourquoi :** isoler le projet, versionner le code, et ne jamais publier mes données Spotify ni mes clés API.
- **Commande ou code clé :** `python -m venv .venv`, `source .venv/Scripts/activate`, `git remote add origin <url>`, `git push -u origin master`
- **Ce que j'ai appris :** Git 2.56, Python 3.15.0, VS Code 1.146.0. J'ai gardé la branche `master`. `.venv/` est un dossier (environnement Python), `.env` est un fichier (secrets) : deux choses différentes, toutes deux dans `.gitignore`. `>>` ajoute à la fin d'un fichier, `>` l'écrase.
- **Question restante :** aucune pour l'instant.

### 2026-11-16 Étape 1.1 : explorer la forme de l'export Spotify
- **Ce que j'ai fait :** extrait l'export dans `data/my_spotify_data`, repéré les fichiers utiles (`StreamingHistory_music_*.json`, `YourLibrary.json`, `Follow.json`, `Wrapped2025.json`) et écrit `src/explore.py` qui affiche le type, le nombre d'écoutes et les noms des champs.
- **Pourquoi :** regarder la structure des données avant de calculer, pour ne pas deviner les noms de champs.
- **Commande ou code clé :** `python src/explore.py`
- **Ce que j'ai appris :** `json.load` renvoie une liste de dictionnaires. Les champs sont `endTime`, `artistName`, `trackName` et `msPlayed` (en millisecondes). Spotify découpe en fichiers de 10 000 écoutes, d'où `_0`, `_1`. `encoding="utf-8"` sert à lire les accents. Les fichiers sensibles (paiements, adresse, identifiants) ne se touchent pas et restent dans `data/`, ignoré par Git.
- **Question restante :** comment obtenir l'historique complet (« Extended streaming history ») au lieu des 12 derniers mois ?

### 2026-11-16 Étape 1.2 : calculer mon top artistes
- **Ce que j'ai fait :** écrit `src/top_artists.py` : il lit tous les `StreamingHistory_music_*.json`, ne garde que les écoutes d'au moins 30 secondes, compte par artiste et affiche le top 10. Résultat : 12 911 écoutes au total, 7 863 valides.
- **Pourquoi :** un titre passé en quelques secondes n'est pas une vraie écoute. Sans ce filtre, environ 40 % de bruit fausserait le classement.
- **Commande ou code clé :** `Counter(e["artistName"] for e in ecoutes_valides)`
- **Ce que j'ai appris :** `glob` pour trouver plusieurs fichiers, `extend` ajoute les éléments d'une liste (contrairement à `append`), compréhension de liste pour filtrer, `Counter.most_common` pour classer. Une `KeyError` veut dire que la clé du dictionnaire est mal orthographiée (`artistNames` au lieu de `artistName`).
- **Question restante :** le seuil de 30 secondes est-il le bon pour mon usage ?

### 2026-11-16 Étape 1.3 : ranger le code en fonctions
- **Ce que j'ai fait :** créé `src/history.py` avec `load_history`, `get_top_artists` et `get_known_artists`. `top_artists.py` ne fait plus qu'appeler ces fonctions.
- **Pourquoi :** séparer la lecture des données de l'affichage, pour réutiliser l'historique en phase 2 sans recopier le code.
- **Commande ou code clé :** `from history import load_history, get_top_artists`
- **Ce que j'ai appris :** l'indentation définit le bloc en Python (`ImportError` si une fonction est mal indentée). Sur AZERTY, Shift+8 donne un 8 et pas un underscore (`NameError`). Une erreur se lit de bas en haut : la dernière ligne dit quoi, le fichier et la ligne disent où.
- **Question restante :** comment Python sait-il où chercher les modules à importer ?
### 2026-11-16 Étape 1.4 Passer à 50 artists et corriger un bug de chargement
- **Ce que j'ai fait :** passer le top à 50 artistes. Constater que les chiffres avaient changé après le refactoring, retrouver un return man indenté dans load_history qui ne lisa le 1er fichier (10000 au lieu 12911 écoutes).
- **Pourquoi :** les recommandations reposeront sur ces chiffres. Avec 50 artistes de départ le choix sera plus varié, et le 50e a encore 32 écoutes, donc un signal solide.
- **Commande ou code clé :** `lenload_history())`
- **Ce que j'ai appris :** après un refactoring, comparer la sortie avec celle d'avant. Un bug sillencieux (pas d'erreur, mais des chiffres faux) est plus dangereux qu'une erreur. Un return dans une boucle for arrête la boucle au premier tour. grep et sed -n 'X,Yp' pour inspecter un fichier.
- **Question restante :** Comment écrire un test automatique qui vérifie que load_history renvoie bien toutes les écoutes ?

## Reprise

- **État :** phases 0 et 1 terminées (lecture de l'historique, top 50 artistes, code dans `src/history.py`).
- **Prochaine étape :** 2.1, créer un compte Last.fm et obtenir une clé API, puis 2.2 la ranger dans `.env`.
- **Rappels :** clé API jamais dans le code ni dans le chat. Venv à activer avec `source .venv/Scripts/activate`. Branche `master`.