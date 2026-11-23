
# Image Python légère
FROM python:3.12-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app/src:/app \
    RUGBY_DATA_DIR=/app/data \
    DBT_PROJECT_DIR=/app \
    DBT_PROFILES_DIR=/app/dbt \
    DBT_SEND_ANONYMOUS_USAGE_STATS=False

# Répertoire de travail
WORKDIR /app

# Installation des dépendances Python ETL
COPY requirements.txt .
RUN pip install -r requirements.txt

# Installation de dbt dans un environnement séparé
COPY requirements-dbt.txt .

RUN python -m venv /opt/dbt-venv \
    && /opt/dbt-venv/bin/pip install -r requirements-dbt.txt \
    && ln -s /opt/dbt-venv/bin/dbt /usr/local/bin/dbt

# Copie du code ETL
COPY src/ ./src/

# Copie du projet dbt
COPY dbt/ ./dbt/
COPY dbt_project.yml .

# Création des répertoires nécessaires
RUN mkdir -p /app/data /tmp/dbt

# Utilisateur non-root pour la sécurité
RUN useradd --create-home --uid 10001 app \
    && chown -R app:app /app /tmp/dbt

USER app

# Commande par défaut
CMD ["python", "--version"]
