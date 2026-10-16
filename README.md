# Dashboard Exoplanètes

Dashboard Streamlit sur les exoplanètes (NASA Exoplanet Archive), pour un public débutant.

**Message :** Sur 5 903 exoplanètes connues, seule une poignée ressemble vraiment à la Terre, et Kepler-452 b est la meilleure candidate.

**Lien en ligne :** [à ajouter après le déploiement]

## Lancer en local

```
python -m pip install -r requirements.txt
python -m streamlit run Presentation.py
```

## Contenu

- `Presentation.py` : page d'accueil (3 KPIs)
- `pages/1_Recherche.py` : recherche avec filtres
- `pages/2_Top_3.py` : classement des 3 planètes les plus proches de la Terre
- `utils.py` : fonctions communes (chargement avec `@st.cache_data`)
- `prepare_data.py` : préparation des données
- `projet_E_exoplanets.csv` : données d'origine (NASA)
- `exoplanetes_clean.csv` : données préparées, utilisées par l'app