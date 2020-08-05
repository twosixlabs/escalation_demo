#!/usr/bin/env bash
python ../yeast_states_app/sql_tables_from_data_converge.py
#docker exec escalation-os-psql psql -h localhost -p 5432 -U escalation_os -d escalation_os -c "alter table growth_rate add column experiment_id_long text; update growth_rate set experiment_id_long = 'experiment.transcriptic.' || experiment_id;"
#sqlacodegen postgresql+pg8000://escalation_os:escalation_os_pwd@localhost:54320/escalation_os --outfile app_deploy_data/models.py

# mysql syntax
docker exec escalation-os-mysql mysql -h localhost -P 3306 --protocol=tcp -u escalation_os_user -pescalation_os_pwd -D escalation_os -e "alter table growth_rate add column experiment_id_long text; update growth_rate set experiment_id_long = 'experiment.transcriptic.' || experiment_id;"
sqlacodegen mysql+mysqlconnector://escalation_os_user:escalation_os_pwd@localhost:3307/escalation_os --outfile app_deploy_data/models.py


