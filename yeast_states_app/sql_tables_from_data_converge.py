from glob import glob
import os

import pandas as pd

from app_deploy_data.app_settings import DATABASE_CONFIG
from database.csv_to_sql import CreateTablesFromCSVs


sql_backend = "psql"
relevant_file_types = {
    "_fc_raw_log10_stats_wide_format.csv": "flow_stat_wide",
    "_platereader.csv": "plate_reader",
    "_fc_meta.csv": "flow_meta",
    "_od_growth_analysis.csv": "growth_rate",
}


def flow_log10_stats_to_wide(input_file_folder, input_filename):
    output_filename = input_filename.replace(".csv", "_wide_format.csv")
    df = pd.read_csv(os.path.join(input_file_folder, input_filename))

    subdf = df.drop(["mean_log10", "std_log10"], axis=1)
    subdf = subdf[subdf.channel == "BL1-H"]

    mean_df = df[df.channel == "BL1-H"][
        ["sample_id", "experiment_id", "aliquot_id", "mean_log10"]
    ].rename(columns={"mean_log10": "BL1H_mean_log10"})

    rr = pd.wide_to_long(
        subdf,
        stubnames="bin(log10)",
        sep="_",
        i=["sample_id", "experiment_id", "aliquot_id", "channel"],
        j="log10_bin",
        suffix=r"\d\.\d+",
    )

    # give the dataframe one column for each channel, with the value of the g
    reshaped_df = rr.reset_index().pivot_table(
        values="bin(log10)",
        index=["sample_id", "experiment_id", "aliquot_id", "log10_bin"],
        columns="channel",
        aggfunc="first",
    )
    # check that the number of data points is as expected:
    # number of columns*rows in the reshaped_df = numbe of rows in the original df times the number of data columns we wanted to include
    assert len(reshaped_df.columns) * reshaped_df.shape[0] == subdf.shape[0] * len(
        [x for x in subdf.columns if x.startswith("bin(log10)_")]
    )

    # add the id columns back in from index
    reshaped_df.reset_index(inplace=True)

    reshaped_df = reshaped_df.merge(
        mean_df,
        left_on=["sample_id", "experiment_id", "aliquot_id"],
        right_on=["sample_id", "experiment_id", "aliquot_id"],
    )
    reshaped_df.to_csv(os.path.join(input_file_folder, output_filename), index=False)


if __name__ == "__main__":
    data_converge_output_path = "test/batch_20200713124857_master"

    # get wide format flow data
    file_type_ending = "_fc_raw_log10_stats.csv"
    format_str = f"../yeast_states_app/yeast_states_data_files/{data_converge_output_path}/*/*{file_type_ending}"
    list_of_fc_files = glob(format_str)
    print(list_of_fc_files)
    for filepath in list_of_fc_files:
        print(filepath)
        flow_log10_stats_to_wide(
            input_file_folder=os.path.dirname(filepath),
            input_filename=os.path.basename(filepath),
        )

    sql_creator = CreateTablesFromCSVs(sql_backend, DATABASE_CONFIG)

    from block_timer.timer import Timer

    # create sql tables for relevant file types
    for relevant_file_type, table_name in relevant_file_types.items():
        with Timer(print_title=False) as t:

            format_str = f"../yeast_states_app/yeast_states_data_files/{data_converge_output_path}/*/*{relevant_file_type}"
            print(format_str)
            list_of_files = glob(format_str)
            print(list_of_files)
            # assuming all schemas the same
            schema = sql_creator.get_schema_from_csv(list_of_files[0])
            data = pd.concat([pd.read_csv(f) for f in list_of_files]).reset_index(
                drop=True
            )
            key_column = None
            print(f"Creating table name {table_name} with {data.shape[0]} rows")
            sql_creator.create_new_table(
                table_name, data, schema, key_columns=key_column, if_exists="replace"
            )
        print(f"Elapsed time writing {table_name}: {t.elapsed} seconds")
