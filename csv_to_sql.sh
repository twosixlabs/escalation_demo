#!/bin/sh

# This script is run from the host machine, using the Docker containers built to create sql tables from csv
# usage: . csv_to_sql.sh {sql_table_name} {path to csv file machine running script} {replace/append/fail}
# e.g.:
# . csv_to_sql.sh structural_metrics /Users/nick.leiby/repos/versioned-datasets/data/protein-design/structural_metrics/topology_mining_and_Longxing_chip_1.v1.structural_metrics.csv replace

echo "Aliasing $2 on host to /escalation/data.csv on Docker container"

docker-compose run \
--entrypoint "python database/csv_to_sql.py $1 /escalation/data.csv $3" \
-v $2:/escalation/data.csv \
web

