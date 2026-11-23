# Rugby Data Platform

> Une plateforme de data engineering pour collecter, transformer et préparer des données statistiques de rugby à l'aide de Python, Apache Airflow, dbt et DuckDB.

Ce projet personnel explore la construction d'un pipeline de données de bout en bout autour de plusieurs compétitions de rugby. Il couvre la récupération des calendriers, des effectifs et des joueurs par match, puis la préparation de statistiques exploitables selon une architecture médaillon.

## Vue d'ensemble

Les traitements sont organisés en étapes distinctes : Airflow orchestre les tâches, Python collecte et prépare les données, puis dbt et DuckDB contribuent à leur transformation et à leur agrégation.

```mermaid
flowchart LR
    S["Sources web"] --> A["Collecte Python"]
    A --> B["Bronze<br/>données brutes"]
    B --> C["Silver<br/>données nettoyées et structurées"]
    C --> D["Gold<br/>données agrégées"]
    O["Apache Airflow"] -. orchestre .-> A
    O -. orchestre .-> C
    T["dbt + DuckDB"] --> D
```

### Étapes du pipeline

1. **Collecter** les calendriers, les effectifs et les données de joueurs et de matchs depuis des sources web.
2. **Conserver** les données récupérées dans la zone Bronze.
3. **Nettoyer et structurer** les données dans la zone Silver avec des traitements Python.
4. **Transformer et agréger** les données avec dbt et DuckDB pour préparer la zone Gold.
5. **Orchestrer** les traitements et leurs dépendances avec des DAGs Apache Airflow.

Les dossiers de données sont séparés par environnement (`DEV`, `INT`, `AP`, `PROD`). Les chemins sont définis dans `src/config.py` et peuvent être sélectionnés avec la variable `RUGBY_ENV` dans les traitements Python.

## Périmètre fonctionnel

Le dépôt contient des traitements autour de plusieurs sujets :

- calendriers de compétitions ;
- effectifs des équipes ;
- joueurs associés aux matchs ;
- statistiques individuelles de joueurs ;
- transformations Bronze → Silver → Gold.

Les DAGs de statistiques prévoient notamment les compétitions suivantes : Top 14, Pro D2, Premiership, Champions Cup, Challenge Cup et United Rugby Championship (URC). Un DAG complet est généré pour chaque couple compétition/saison configuré dans `airflow/dags/dag-player-stats.py` ; les tâches et leurs dépendances sont définies une seule fois puis réutilisées. Chaque DAG peut être déclenché manuellement et dispose de ses propres statuts et logs de tâches.

## Technologies

| Domaine | Outils |
|---|---|
| Langage et transformations | Python, pandas |
| Collecte web | Requests, Beautiful Soup |
| Orchestration | Apache Airflow |
| Modélisation analytique | dbt Core, dbt-duckdb, DuckDB |
| Qualité du code et tests | Ruff, pytest |
| Exécution reproductible | Docker, GitHub Actions |

## Démarrer en local avec Docker Compose

Tout tourne sur ta machine dans un seul conteneur : Airflow, le code Python et dbt. Compose construit l'image du projet, conserve l'état d'Airflow et stocke les données dans le dossier local `data/`. Il n'est pas nécessaire de lancer une commande Airflow séparément.

```bash
mkdir -p data
export AIRFLOW_UID="$(id -u)"
docker compose up --build -d
```

Ouvre ensuite `http://localhost:8081`. Au premier démarrage, Airflow crée un compte administrateur et affiche ses identifiants dans les logs :

```bash
docker compose logs airflow
```

Commandes courantes :

```bash
docker compose stop       # arrêter sans supprimer le conteneur
docker compose start      # redémarrer
docker compose down       # supprimer le conteneur, garder l'état Airflow
docker compose up -d      # recréer/démarrer en arrière-plan
docker compose logs -f airflow
```

Les données de pipeline restent dans `data/` et l'état d'Airflow (base locale, compte et journaux) dans un volume Docker nommé. `docker compose down -v` supprime aussi ce volume et réinitialise Airflow. Le port est limité à la machine locale ; `AIRFLOW_PORT` permet de le changer si `8081` est déjà pris.

Le dossier de données par défaut est `data/` à la racine du dépôt. `RUGBY_DATA_DIR` permet de le déplacer ; Compose le configure pour pointer vers le dossier monté dans le conteneur. Le même réglage fonctionne lors d'une exécution Python hors Docker.

> **Note :** cette configuration `standalone` avec SQLite est destinée au développement et à une utilisation locale, pas à un déploiement de production. L'image reste autonome et peut être reconstruite ailleurs avec Docker Compose.

## Tests et contrôles

L'intégration continue vérifie le lint, les tests Python, l'analyse dbt et la construction ainsi que le smoke test de l'image Docker.

Pour exécuter les tests Python dans un environnement de développement :

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip install -r requirements-lint.txt
pytest
ruff check src tests airflow/dags scripts
```

Pour construire l'image et vérifier son fonctionnement de base :

```bash
docker build -t rugby-data .
bash scripts/smoke_test_image.sh rugby-data
```

Le smoke test vérifie notamment les dépendances, le parsing dbt et le chargement des DAGs Airflow sans accès réseau.

## Structure du dépôt

```text
airflow/dags/   Orchestration des pipelines
dbt/models/     Modèles analytiques Silver et Gold
scripts/        Vérifications et smoke tests
src/            Collecte, transformations et utilitaires Python
tests/          Tests automatisés
```

## Données et utilisation

Ce dépôt contient le code du pipeline, **pas les jeux de données extraits**. Les données collectées restent la propriété de leurs sources, notamment RugbyPass et AllRugby. Avant toute collecte ou réutilisation, il appartient à l'utilisateur de vérifier les conditions d'utilisation des sites concernés et de respecter les droits applicables.

Ce projet est présenté à des fins d'apprentissage et de portfolio. Il ne constitue ni une API de données ni une autorisation de redistribuer les contenus collectés.
