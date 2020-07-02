#!/usr/bin/env bash
python database/csv_to_sql.py flow_meta /Users/nick.leiby/repos/escos/scratch/yeast_states_data_files/NovelChassis-OR-Circuit-Cycle0-24hour__fc_meta.csv
python database/csv_to_sql.py dose_response /Users/nick.leiby/repos/escos/scratch/yeast_states_data_files/pdt_YeastSTATES-OR-Gate-CRISPR-Dose-Response__od_growth_analysis.csv
python database/csv_to_sql.py plate_reader /Users/nick.leiby/repos/escos/scratch/yeast_states_data_files/YeastSTATES-Beta-Estradiol-OR-Gate-Plant-TF-Growth-Curves__platereader.csv
python database/csv_to_sql.py flow_stat /Users/nick.leiby/repos/escos/scratch/yeast_states_data_files/NovelChassis-OR-Circuit-Cycle0-24hour__fc_raw_log10_stats.csv

sqlacodegen postgresql+pg8000://escalation_os:escalation_os_pwd@localhost:54320/escalation_os --outfile database/models.py
