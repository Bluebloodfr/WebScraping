# WebScraping

## Subjet

**Project** :
- Sujet Tourisme RSE
- Scrap via API & standard (page classique ou dynamique)
- Objectif NLP derrière

**Notation** :
- Envoyer GitHub sur Moodle
- Soutenance finale par gpr sur semaine exam

**Goal** :  
Recommander quel lieu visiter & quand en se basant sur
- le [CSV](https://www.data.gouv.fr/fr/datasets/datatourisme-la-base-nationale-des-donnees-publiques-dinformation-touristique-en-open-data) des  Point of Interest (POI) toursistique selon le gouvernement  
- l'[API](https://api.meteo-concept.com/documentation_openapi ) de prévision météo (necessite d'un compte et d'une clé API)
- les commentaires Google Maps (scrapping dynamique + NLP)

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
```bash
API_KEY=<weather api key>
```

2. Install dependencies
```bash
python -m venv .venv
.venv\Scripts\activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

2. Run the app
```bash
streamlit run app.py
```