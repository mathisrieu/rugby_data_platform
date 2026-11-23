
#!/usr/bin/env bash
# Vérifie qu'une image rugby-data-stats est saine.
# Réseau coupé : les vérifications ne doivent pas nécessiter Internet.
#
# Utilisation :
#   docker build -t rugby-data-stats:local .
#   bash scripts/smoke_test_image.sh rugby-data-stats:local

set -euo pipefail

IMAGE="${1:?usage: $0 <image>}"
RUN=(docker run --rm --network none --entrypoint bash)

echo "→ dépendances Python"
"${RUN[@]}" "$IMAGE" -c \
  'python -c "import pandas, requests, bs4, msal; print(\"Dépendances Python OK\")"'

echo "→ environnement Python"
"${RUN[@]}" "$IMAGE" -c \
  'python --version && id'

echo "→ dbt"
"${RUN[@]}" "$IMAGE" -c 'dbt --version'

echo "→ dbt parse"
"${RUN[@]}" "$IMAGE" -c 'dbt parse'

echo "✓ image OK : $IMAGE"
