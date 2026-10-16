# Cadrage — Dashboard Exoplanètes

**Groupe :** Yehia Qabil, 
**Données :** NASA Exoplanet Archive — 38 449 lignes, réduites à 5 903 planètes (`default_flag == 1`, une ligne par planète)
**Lien du dashboard :** [http://localhost:8501/]

## 1. Message clé

> Sur 5 903 exoplanètes connues, seule une poignée ressemble vraiment à la Terre, et Kepler-452 b est la meilleure candidate.

## 2. Audience cible

Un public **débutant** (étudiants, curieux) qui n'a jamais étudié l'astronomie.
Conséquences pour le dashboard : unités simples (°C, années-lumière, « × Terre »), peu de texte, une seule couleur d'accent (orange) pour l'essentiel, le reste en gris.

## 3. KPIs retenus

| KPI | Contexte affiché | Vanity ou actionnable ? |
|---|---|---|
| **5 903 planètes connues** | +1 573 sur les 5 dernières années (tendance) | Seul, le total serait une *vanity metric*. Avec la tendance, il montre que la liste change vite : le classement doit être mis à jour régulièrement. **Actionnable.** |
| **74 % découvertes par transit** | Comparaison avec les autres méthodes | Montre un **biais** : le transit trouve surtout des planètes grosses et proches de leur étoile. Le lecteur sait qu'il doit rester prudent. **Actionnable.** |
| **844 planètes de taille Terre (19 %)** | Part du total (comparaison) | C'est le point de départ de la recherche : le nombre de candidates à trier avec les filtres. **Actionnable.** |

## 4. Structure prévue

Application **multi-pages** (dossier `pages/`) : synthèse, puis détail.

| Page | Zone KPIs | Zone détail | Filtres (sidebar) |
|---|---|---|---|
| **Présentation** | 3 KPIs ci-dessus, en 3 colonnes | Onglets : découvertes par année (barres), méthodes de détection (barres horizontales), distance à l'étoile par zone du Système solaire | — |
| **Recherche** | Nombre de planètes trouvées | Nuage de points taille × température (axe log pour la taille, zone « type Terre » surlignée), tableau des résultats, réactifs aux filtres | Taille, température, distance à l'étoile |
| **Top 3** | Score de la n°1 | Barres horizontales du score (Terre = 1), fiches des 3 planètes | Mode strict (données complètes uniquement) |

## 5. Choix de conception justifiés

- **Titre = message** : le lecteur comprend la conclusion en moins de 5 secondes.
- **Barres** pour comparer des catégories (méthodes, années), **nuage de points** pour croiser deux mesures (taille et température).
- **Axe logarithmique** pour la taille : les planètes vont de 0,3 à plus de 20 fois la Terre ; en linéaire, les petites planètes seraient écrasées.
- **Une seule couleur d'accent** (canal pré-attentif) : l'orange montre ce qui compte (Terre, Top 3), le reste est gris.
- **Score de ressemblance** : moyenne de 5 critères (taille, température, ensoleillement, masse, type d'étoile), de 0 à 1. Limite affichée : il ne dit rien de l'atmosphère ni de l'eau.
- **`@st.cache_data`** : les données sont chargées une seule fois, l'app reste rapide quand on change un filtre.
