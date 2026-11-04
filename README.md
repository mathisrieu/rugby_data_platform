# Rugby Data Platform


## Description

Projet de Data Engineering permettant de mettre à disposition les statistiques de match des joueurs Top 14.

## Architecture

Le projet suit une architecture médaillon (bronze -> silver -> gold)

- les données brutes sont scrappées depuis différentes sources web et chargées en zone bronze
- ces données sont ensuite sont nettoyées, transformées, et mappées puis chargées en zone silver
- elles sont ensuite agrégées et mise au format parquet en zone gold


## Technologies

- Python
- Airflow
- dbt
- Pandas
- BeautifulSoup


## Données et mentions légales

Les données collectées appartiennent à leurs sources respectives
(rugbypass.com, allrugby.com). Ce dépôt ne contient ni ne redistribue
aucune donnée. Leur usage est soumis aux conditions d'utilisation de
ces sites, et ce projet est destiné à un usage strictement personnel
et non commercial.
