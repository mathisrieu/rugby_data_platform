# syntax=docker/dockerfile:1
#
# Image Airflow + code du projet + dbt (dans un environnement séparé).
#   docker build -t rugby-data .
#   docker run --rm -p 8080:8080 \
#       -v "$PWD/data:/Volumes/rugby_data" \
#       rugby-data airflow standalone
#
# /Volumes/rugby_data est la racine des données définie dans src/config.py.

ARG AIRFLOW_VERSION=2.10.1
ARG PYTHON_VERSION=3.12
FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION}

ARG AIRFLOW_VERSION
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# --- Dépendances Python (mêmes contraintes Airflow que la CI) ---
COPY requirements.txt /tmp/requirements.txt
RUN grep -qxF "apache-airflow==${AIRFLOW_VERSION}" /tmp/requirements.txt \
    || { echo "ERREUR: AIRFLOW_VERSION=${AIRFLOW_VERSION} diffère du pin de requirements.txt" >&2; exit 1; } \
    && pip install -r /tmp/requirements.txt

# --- dbt : environnement isolé, exposé via un lien symbolique dans le PATH ---
COPY requirements-dbt.txt /tmp/requirements-dbt.txt
RUN python -m venv /home/airflow/dbt-venv \
    && /home/airflow/dbt-venv/bin/pip install -r /tmp/requirements-dbt.txt \
    && ln -s /home/airflow/dbt-venv/bin/dbt /home/airflow/.local/bin/dbt

# --- Répertoires de travail (racine des données + projet) ---
# hadolint ignore=DL3066
USER root
RUN mkdir -p /Volumes/rugby_data /opt/rugby/data \
    && chown -R airflow:root /Volumes/rugby_data /opt/rugby
# hadolint ignore=DL3066
USER airflow
WORKDIR /opt/rugby

# --- Code du projet (copié en dernier : meilleur usage du cache de build) ---
COPY --chown=airflow:root src ./src
COPY --chown=airflow:root airflow/dags ./airflow/dags
COPY --chown=airflow:root dbt ./dbt
COPY --chown=airflow:root dbt_project.yml ./

# Les DAGs importent `player_stats...` (depuis src/) et `src.players_per_match...` (depuis la racine).
ENV PYTHONPATH=/opt/rugby:/opt/rugby/src \
    AIRFLOW__CORE__DAGS_FOLDER=/opt/rugby/airflow/dags \
    AIRFLOW__CORE__LOAD_EXAMPLES=False \
    DBT_PROJECT_DIR=/opt/rugby \
    DBT_PROFILES_DIR=/opt/rugby/dbt \
    DBT_SEND_ANONYMOUS_USAGE_STATS=False

LABEL org.opencontainers.image.title="rugby-data" \
      org.opencontainers.image.description="Pipeline de données Top 14 : Airflow + dbt + DuckDB"
