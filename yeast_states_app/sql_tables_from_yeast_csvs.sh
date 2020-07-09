#!/usr/bin/env bash
#make sure your python path is on escos/escalation
python database/csv_to_sql.py flow_meta ../yeast_states_app/yeast_states_data_files/NovelChassis-OR-Circuit-Cycle0-24hour__fc_meta.csv replace
python database/csv_to_sql.py growth_rate ../yeast_states_app/yeast_states_data_files/pdt_NovelChassis-OR-Circuit-Cycle0-24hour__od_growth_analysis.csv replace
python database/csv_to_sql.py plate_reader ../yeast_states_app/yeast_states_data_files/NovelChassis-OR-Circuit-Cycle0-24hour__platereader.csv replace
# pivoted version of the flow_stat table
python database/csv_to_sql.py flow_stat_wide ../yeast_states_app/yeast_states_data_files/wide_format_NovelChassis-OR-Circuit-Cycle0-24hour__fc_raw_log10_stats.csv replace

docker exec escalation-os-psql psql -h localhost -p 5432 -U escalation_os -d escalation_os -c "alter table flow_meta add column experiment_id_short text; update flow_meta set experiment_id_short = right(experiment_id, 14);"
sqlacodegen postgresql+pg8000://escalation_os:escalation_os_pwd@localhost:54320/escalation_os --outfile app_deploy_data/models.py

# mysql syntax
#docker exec escalation-os-mysql mysql -h localhost -P 3306 --protocol=tcp -u escalation_os_user -pescalation_os_pwd -D escalation_os -e "alter table flow_meta add column experiment_id_short text; update flow_meta set experiment_id_short = right(experiment_id, 14);"
#sqlacodegen mysql+mysqlconnector://escalation_os_user:escalation_os_pwd@localhost:3307/escalation_os --outfile app_deploy_data/models.py


