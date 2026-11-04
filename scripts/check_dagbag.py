"""Charge les DAGs du dossier configuré et sort en erreur au moindre problème d'import.

Utilisé par scripts/smoke_test_image.sh, à l'intérieur de l'image Docker :
    docker run -i --rm --entrypoint python <image> - < scripts/check_dagbag.py
"""

import sys

from airflow.models import DagBag

bag = DagBag(include_examples=False)

for file, message in bag.import_errors.items():
    print(f"ERREUR d'import : {file}\n{message}", file=sys.stderr)

print(f"{len(bag.dags)} DAG(s) chargé(s) : {sorted(bag.dag_ids)}")
sys.exit(1 if bag.import_errors or not bag.dags else 0)
