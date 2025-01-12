# WebScraping

## Subjet

Project :
- Sujet Tourisme RSE
- Scrap via API & standard (page classique ou dynamique)
- Objectif NLP derrière

Notation :
- Envoyer GitHub sur Moodle
- Soutenance finale par gpr sur semaine exam

---

Goal : Recommander Quel lieu visiter & quand en se basant sur :
- les centres d'interêt [API](https://gitlab.adullact.net/adntourisme/datatourisme/api)
- les prévision météo [API](https://api.meteo-concept.com/documentation_openapi )
- Commentaires Google Maps (scrapping dynamique + NLP)


## Structure

Le déroulé d'une requete :
1. Utilisateur met sa région
2. Get les centres d'interêts & leurs loc
3. Chechercher météo avec à locs
4. Chercher les commentraires Google Maps associés
5. SentimentsAnalysis sur ces commentaires
6. Affichage (optionnel)

## Initialisation

1. Create a file .env on root
```
ROOT_DIR=<root directory>
API_KEY=<weather api key>
```

2. Download datatourism zip file
```bash
./src/tourism/download_zip.sh
```

3. Run the app
```bash
streamlit run app.py
```