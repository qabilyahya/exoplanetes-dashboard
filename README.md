# SciPulse — Observatoire Scientifique

> Pipeline de données complet pour l'exploration et la visualisation d'articles scientifiques ArXiv et de posts Hacker News.

---

## 🏗️ Architecture

```
ArXiv JSON (100k articles)
        │
        ▼
  Logstash Pipeline ──────────────► arxiv-papers-raw (Elasticsearch)
        │                                    │
        │                                    ▼
        │                         Python Bulk Ingest
        │                                    │
        ▼                                    ▼
Great Expectations              arxiv-papers (mapping optimisé)
  (Validation qualité)                       │
        │                                    ▼
        │                         TF-IDF Enrichissement
        │                         (mots-clés automatiques)
        ▼                                    │
  PostgreSQL                                 ▼
        │                         Kibana Dashboard
        ▼
   dbt Models
   (staging + marts)
        │
        ▼
  Airflow DAGs
  (Orchestration)
```

---

## 🛠️ Stack Technique

| Composant | Technologie |
|-----------|-------------|
| Moteur de recherche | Elasticsearch 8.13 |
| Visualisation | Kibana 8.13 |
| Ingestion | Logstash 8.13 + Python |
| Orchestration | Apache Airflow 2.9 |
| Transformation | dbt-postgres |
| Qualité données | Great Expectations 1.17 |
| Stockage relationnel | PostgreSQL 16 |
| Object Storage | MinIO |
| ML / NLP | Scikit-learn (TF-IDF) |
| Containerisation | Docker Compose |

---

## 📁 Structure du projet

```
scipulse/
├── airflow/
│   └── dags/
│       ├── dag_arxiv_pipeline.py    # DAG pipeline ArXiv complet
│       └── dag_hn_poller.py         # DAG polling Hacker News
├── data/
│   └── arxiv-raw/                   # Données brutes ArXiv
├── dbt/
│   └── scipulse/
│       └── models/
│           ├── stg_arxiv_papers.sql # Staging ArXiv
│           └── fct_auteurs_prolifiques.sql
├── docker/
│   └── logstash/
│       └── pipeline/
│           └── arxiv.conf           # Pipeline Logstash
├── src/
│   ├── enrichment/
│   │   └── enrich_arxiv.py         # TF-IDF + croisement HN
│   ├── ingestion/
│   │   ├── arxiv_bulk_ingest.py    # Ingestion Python
│   │   ├── hn_poller.py            # Polling HN API
│   │   └── reindex_arxiv.py        # Réindexation avec mapping optimisé
│   ├── quality/
│   │   ├── validate_arxiv.py       # Validation Great Expectations
│   │   ├── validate_hn.py          # Validation HN
│   │   └── clean_arxiv.py          # Nettoyage des données
│   ├── search/
│   │   └── search_service.py       # Module de recherche ES
│   ├── transformation/
│   │   └── load_to_postgres.py     # Chargement ES → PostgreSQL
│   └── utils/
│       ├── mappings.py             # Mappings Elasticsearch
│       └── pipeline_metrics.py     # Métriques de monitoring
├── tests/
│   └── unit/
│       └── test_search_service.py  # Tests unitaires (13/13)
└── docker-compose.yml
```

---

## 🚀 Démarrage rapide

### Prérequis
- Docker Desktop avec 16 Go RAM alloués
- Python 3.10+

### Installation

```bash
# 1. Cloner le projet
git clone https://github.com/votre-repo/scipulse.git
cd scipulse

# 2. Démarrer la stack
docker compose up -d

# 3. Attendre que tous les services soient healthy
docker compose ps

# 4. Installer les dépendances Python
pip install elasticsearch scikit-learn great-expectations psycopg2-binary dbt-postgres requests pandas pytest
```

### Ingestion des données

```bash
# Ingestion via Python (index arxiv-papers-raw)
python -m src.ingestion.arxiv_bulk_ingest data/arxiv-raw/arxiv-cs-subset-100k.json

# Créer les mappings optimisés
python -m src.utils.mappings

# Réindexer avec le mapping optimisé
python -m src.ingestion.reindex_arxiv

# Enrichissement TF-IDF
python -m src.enrichment.enrich_arxiv --max 50000
```

### Validation qualité

```bash
# Validation ArXiv (score : 90%)
python -m src.quality.validate_arxiv

# Nettoyage des données
python -m src.quality.clean_arxiv

# Collecte de métriques
python -m src.utils.pipeline_metrics
```

### Tests

```bash
pytest tests/unit/test_search_service.py -v
# → 13/13 tests passent
```

---

## 📊 Dashboards Kibana

Ouvrir http://localhost:5601

### SciPulse — Observatoire Scientifique
- **100 000** articles ArXiv indexés
- **5 000** articles enrichis avec mots-clés TF-IDF
- **96** catégories distinctes
- Area chart : évolution temporelle par catégorie
- Bar chart : top 20 catégories
- Tag cloud : mots-clés les plus fréquents
- Table : articles récents

### SciPulse — Monitoring Pipeline
- Statut Elasticsearch en temps réel
- Volumes des index
- Taille des index
- Historique des métriques

---

## 🔍 Exemples de recherche

```python
from src.search.search_service import SciPulseSearch

search = SciPulseSearch()

# Recherche full-text
results = search.full_text("transformer attention mechanism")

# Articles similaires
similar = search.more_like_this("2301.07041")

# Recherche combinée avec filtres
results = search.combined_search(
    "neural network",
    categories=["cs.AI", "cs.LG"],
    date_from="2022-01-01"
)
```

---

## 🌐 Services

| Service | URL | Credentials |
|---------|-----|-------------|
| Kibana | http://localhost:5601 | - |
| Airflow | http://localhost:8080 | admin / admin |
| Elasticsearch | http://localhost:9200 | - |
| MinIO | http://localhost:9001 | minioadmin / minioadmin |
| PostgreSQL | localhost:5432 | scipulse / scipulse |

---

## 📈 Métriques du projet

| Métrique | Valeur |
|----------|--------|
| Articles indexés | 100 000 |
| Articles enrichis (TF-IDF) | 5 000 |
| Items Hacker News | 500 |
| Score qualité GX | 90% (9/10) |
| Titres nettoyés | 40 233 |
| Tests unitaires | 13/13 ✅ |
| Taille index ES | ~225 MB |

---

## 👨‍💻 Auteur

Yahya — Master Data & AI, HETIC
