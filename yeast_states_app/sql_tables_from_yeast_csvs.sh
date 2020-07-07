#!/usr/bin/env bash
#make sure your python path is on escos
python database/csv_to_sql.py flow_meta /Users/alexander.zaitzeff/Documents/escos/yeast_states_app/yeast_states_data_files/NovelChassis-OR-Circuit-Cycle0-24hour__fc_meta.csv
python database/csv_to_sql.py growth_rate /Users/alexander.zaitzeff/Documents/escos/yeast_states_app/yeast_states_data_files/pdt_NovelChassis-OR-Circuit-Cycle0-24hour__od_growth_analysis.csv
python database/csv_to_sql.py plate_reader /Users/alexander.zaitzeff/Documents/escos/yeast_states_app/yeast_states_data_files/NovelChassis-OR-Circuit-Cycle0-24hour__platereader.csv
# pivoted version of the flow_stat table
python database/csv_to_sql.py flow_stat_wide /Users/alexander.zaitzeff/Documents/escos/yeast_states_app/yeast_states_data_files/wide_format_NovelChassis-OR-Circuit-Cycle0-24hour__fc_raw_log10_stats.csv

    docker exec escalation-os-psql psql -h localhost -p 5432 -U escalation_os -d escalation_os -c "alter table flow_meta add column experiment_id_short text; update flow_meta set experiment_id_short = right(experiment_id, 14);"
sqlacodegen postgresql+pg8000://escalation_os:escalation_os_pwd@localhost:54320/escalation_os --outfile database/models.py



