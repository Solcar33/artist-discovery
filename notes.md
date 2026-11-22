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

- **État :** phases 0, 1 et 2 terminées. L'historique Spotify est lu, le top 50 calculé (`src/history.py`), Last.fm est interrogé (`src/lastfm.py`) et les candidats sont classés (`src/recommand.py`).
- **Prochaine étape :** 2.6, choisir l'artiste de la semaine par tirage au hasard pondéré parmi les meilleurs candidats, puis phase 3 (fiche de l'artiste : MusicBrainz, Wikipedia, Last.fm).
- **Rappels :** clé API dans `.env`, jamais dans le code ni dans le chat. Venv à activer avec `source .venv/Scripts/activate`. Branche `master`. Vérifier les sorties après chaque modification.

### 2026-11-22 Étape 2.1 à 2.3 : clé Last.fm, fichier .env et installation de requests
- **Ce que j'ai fait :** créé une clé API Last.fm, l'ai rangée dans `.env`, vérifié qu'il est ignoré par Git, installé `requests` et `python-dotenv`, puis généré `requirements.txt`.
- **Pourquoi :** appeler l'API Last.fm pour trouver des artistes proches des miens. La clé est un secret : elle ne doit jamais être dans le code, dans les notes ni sur GitHub.
- **Commande ou code clé :** `git check-ignore -v .env`, `python -m pip install requests python-dotenv`, `python -m pip freeze > requirements.txt`
- **Ce que j'ai appris :** `python -m pip` garantit d'utiliser le pip du venv. `requirements.txt` liste les dépendances pour recréer l'environnement. On vérifie qu'un secret est ignoré par Git avant de commiter. pip installe aussi les dépendances de `requests` tout seul.
- **Question restante :** comment `python-dotenv` lit-il le fichier `.env` ?

### 2026-11-22 Étape 2.4 : premier appel à l'API Last.fm
- **Ce que j'ai fait :** écrit `src/lastfm.py` avec `get_similar_artists`, qui appelle `artist.getsimilar`. Testé avec Foo Fighters.
- **Pourquoi :** obtenir des artistes proches des miens, base des recommandations. Une API répond en JSON, comme mon export Spotify.
- **Commande ou code clé :** `requests.get(BASE_URL, params=params, timeout=10)`
- **Ce que j'ai appris :** `load_dotenv` et `os.getenv` lisent la clé dans `.env`. Pas de `raise_for_status` car l'erreur afficherait l'URL avec ma clé. Un fichier enregistré au mauvais endroit laisse un fichier vide dans `src/`. Un soulignement rouge dans VS Code est un avertissement à lire avant de lancer.
- **Question restante :** comment Last.fm calcule-t-il le score de similarité ?

### 2026-11-22 Étape 2.5 : candidats à partir de mes 50 artistes
- **Ce que j'ai fait :** écrit `src/recommand.py` : il appelle Last.fm pour chacun de mes 50 artistes, retire ceux que je connais déjà, cumule les scores pondérés par mes écoutes et affiche les 10 meilleurs candidats avec les favoris qui les ont fait remonter.
- **Pourquoi :** un artiste proche de plusieurs de mes favoris est un meilleur candidat. Les favoris concernés serviront à expliquer pourquoi il est recommandé.
- **Commande ou code clé :** `scores[candidat] += float(similaire["match"]) * nb`
- **Ce que j'ai appris :** `defaultdict` évite de tester si une clé existe. `sorted` avec `key=lambda x: x[1]` trie sur le score. J'avais écrit `lambda x:[1]` : Python n'a signalé aucune erreur, mais toutes les clés étaient égales, donc l'ordre d'origine était gardé. Comparer des noms rate les alias (Bob Marley contre Bob Marley & The Wailers).
- **Question restante :** comment identifier un même artiste sous plusieurs noms (MusicBrainz) ?
### 2026-11-22 Étape 2.6 Choisir l'artiste de la semaine
- **Ce que j'ai fait :** réorganiser recommand.py en fonctions get_candidates et pick_artist_of_the_week. Le tirage est fixé par la semaine ISO. Ajouté une liste A_IGNORER pour les alias connus.
- **Pourquoi :** Une execution automatique chaque semaine doit pouvoir êtree relancée sans changer d'artiste. Un tirage dans les 30 meilleurs laisse sa chance aux artistes moins connus.
- **Commande ou code clé :** `random.Random(f"{annee}-W{semaine}").choice(candidats[:pool])`
- **Ce que j'ai appris :** Une graine rend le hasard reproductible. isocalendat donne année, semaine et jour. le | fusionne duex ensembles. Une fonction qui renvoie ses données est plus réutilisable qu'une qui les affiche.
- **Question restante :** Comment éviter de retomber sur un artiste déjà recommandé les semaines précédentes

### 2026-11-22 Étape 3.1 Infos d'un artiste via last.fm
- **Ce que j'ai fait :** Factorisé src/lastfm.py avec une fonction interne _appeler, puis ajouté get_artist_info (auditeurs, écoutes, genres, bio, mbid).
- **Pourquoi :** Remplir la fiche de l'artiste. Factoriser évite de recopier les mêmes vérifications pour chaque méthode de l'API.
- **Commande ou code clé :** `_appeler("artist.getinfo", artist=artiste, autocorrect=1)`
- **Ce que j'ai appris :** **params collect les paramètres nommés, ** les déverse dans un dictionnaire. dict.get évite une KeyError si la clé manque. Après un refactoring, je relance recommand.py pour vérifier que le résultat n'a pas changé. Les auditeurs Last.fm ne sont que les auditeurss mensuel de Spotify.
- **Question restante :** Comment nettoyer le HTML de la bio ?

### 2026-11-22 Étape 3.2 Liens et réseaux sociaux avec MusicBrainz
- **Ce que j'ai fait :** Créé  src/musicbrainz.py avec find_artist (recherche par nom) et get_artist_links (liens regroupés par type) Ajouté une reprise automatique quand le server répond 503
- **Pourquoi :** La fiche doit contenir les liens de l'artiste (écoute, sites, bases de données). MusicBrainz les liste sans clé API, mais impose un User-Agent et une limite de 1 requête par seconde.
- **Commande ou code clé :** `requests.get(url, params=params, headers=HEADERS, timeout=10)`
- **Ce que j'ai appris :** Un 503 vient du server, pas de mon code. Le backoff exponentiel double l'attente à chaque échec. Les clés d'une API se copient exactement : resource et  pas ressource, artists et pas artist. La recherche renvoie le meilleur résultat : je vérifie le nom et le score. Une source peut être incomplète, donc la page affichera seulement les liens trouvés.
- **Question restante :** Comment éviter de se tromper d'artiste en cas d'homonyme ?

### 2026-11-22 Étape 3.3 Bio avec Wikidata et Wikipedia
- **Ce que j'ai fait :** créé wikipedia.py : à partir de l'identifiant Wikidata, récupère le titre de la page Wikipedia (fr puis en) puis son résumé en texte brut.
- **Pourquoi :** Une bio propre sans HTML, meilleure que celle de Last.fm. Wikidata relie les versions linguistiques d'un sujet et évite les homonymes. Le repli du français cers l'anglais couvre les artistes sans article français.
- **Commande ou code clé :** `quote(titre, safe="")`
- **Ce que j'ai appris :** Un 404 sur un identifiant valide vient souvent d'une url mal écrite : j'avais mis wikipedia.org au lieu de wikidata?org. Des print temporaires m'ont montré où ça cassait. Une SyntaxError arrive quand deux instructions sont collées sur une ligne. Une clé de dictionnaire s'écrit entre guillemets. Wikipedia et Wikidata sont deux sources différentes.
- **Question restante :** Que faire quand l'artiste n'a aucun article Wikipedia ?

### 2026-11-22 Étape 3.4 Assembler la fiche de l'artiste
- **Ce que j'ai fait :** Créé src/fiche.py : build_fiche réunit Last.fm, MusicBrainz et Wikipedia dans un dictionnaire, save_fiche l'enregistre en JSON dans content/. Une source en panne laisse un champ vide au lieu de planter.
- **Pourquoi :** Le site lira un fichier JSON par semaine. Les sources peuvent tomber en panne ou être incomplète : la fiche doit se générer quand même.
- **Commande ou code clé :** `json.dump(fiche, f, ensure_ascii=False, indent=2)`
- **Ce que j'ai appris :** L'indentation décide de ce qui s'exécute : un return trop à droite dans un if renvoyait None, donc le fichier contenait null. Il faut ouvrir le résultat et pas seulement lire le message de succès. isoformat sans parenthèses stocke la fonction. py_compile vérifie la syntaxe sans exécuter. Ne jamais afficher le détail d'une erreur réseau :  il contient l'URL, donc la clé.
- **Question restante :** Comment éviter de recommander deux fois le mê^me artiste d'une semaine à l'autre ?

### 2026-11-22 Étape 3.5 Ne pas recommander deux fois le même artiste
- **Ce que j'ai fait :** Ajouté get_past_artists dans fiche.py, qui lit les fiches des semaines précédentes, et un paramètre exclus dans pick_artist_of_the_week.
- **Pourquoi :** Le site se met à jour chaque semaine : sans mémoire, le même artiste pourrait revenir. On exclut les semaines passées mais pas la semaine en cours, pour qu'une relance donne le même résultat.
- **Commande ou code clé :** `[c for candidats if C[0].lower() not in exclus]`
- **Ce que j'ai appris :** glob liste les fichiers d'un dossier, continue saute un tour de boucle. Une fonction utilitaire évite de dupliquer le nom de fichier. Tester avec un faux fichier de la semaine précédente, puis le supprimer.
- **Question restante :** Comment mon programme saura-t-il quels artistes ont déjà été publiés quand il tournera sur GitHub Actions ?
