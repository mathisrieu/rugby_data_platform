#!/usr/bin/env bash
# Vérifie qu'une image rugby-data est saine. Réseau coupé : rien ne doit en avoir besoin.
# Utilisable en local comme en CI :
#   docker build -t rugby-data .
#   bash scripts/smoke_test_image.sh rugby-data
set -euo pipefail

IMAGE="${1:?usage: $0 <image>}"
RUN=(docker run --rm --network none -e AIRFLOW_VAR_ENV=DEV --entrypoint bash)

echo "→ dépendances Python"
"${RUN[@]}" "$IMAGE" -c 'python -c "import pandas, requests, bs4, msal, airflow; print(\"airflow\", airflow.__version__)"'

echo "→ dbt"
"${RUN[@]}" "$IMAGE" -c 'dbt --version'

echo "→ dbt parse"
"${RUN[@]}" "$IMAGE" -c 'dbt parse'

echo "→ chargement des DAGs"
docker run -i --rm --network none -e AIRFLOW_VAR_ENV=DEV --entrypoint python "$IMAGE" - < "$(dirname "$0")/check_dagbag.py"

echo "✓ image OK : $IMAGE"
