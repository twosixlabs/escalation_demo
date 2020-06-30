#!/usr/bin/env bash

#docker volume create db_volume_escalate_os

#export MYSQL_ROOT_PASSWORD=test_pwd
#export MYSQL_DATABASE=escalation_os
#export MYSQL_USER=escalation_os_user
#export MYSQL_PASSWORD=escalation_os_pwd

#docker run -d \
#    -e MYSQL_ROOT_PASSWORD=test_pwd \
#    -e MYSQL_DATABASE=escalation_os \
#    -e MYSQL_USER=escalation_os_user \
#    -e MYSQL_PASSWORD=escalation_os_pwd \
#    --mount type=volume,src=db_volume_escalate_os,dst=/var/lib/mysql \
#    -p 3306:3306 \
#    --name escalation-os-mysql \
#    mysql:latest


# to connect
# todo: connect to mysql container within the docker container as in psql below
# mysql -h localhost -P 3306 --protocol=tcp -u escalation_os_user -pescalation_os_pwd -D escalation_os


## PSQL setup

#docker volume create psql_db_volume_escalate_os

#docker run -d \
#    -e PSQL_ROOT_PASSWORD=test_pwd \
#    -e POSTGRES_USER=escalation_os \
#    -e POSTGRES_PASSWORD=escalation_os_pwd \
#    -v psql_db_volume_escalate_os:/var/lib/postgresql/data \
#    -p 54320:5432 \
#    --name escalation-os-psql \
#    postgres:latest

# to connect to db
# docker exec -it escalation-os-psql psql -h localhost -p 5432 -U escalation_os -d escalation_os
