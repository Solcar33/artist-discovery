from history import load_history, get_top_artists

ecoutes = load_history()
for artiste, nb in get_top_artists(ecoutes, 50):
    print(f"{nb:>5}  {artiste}")