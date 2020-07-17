from ast import literal_eval
from glob import glob
import os
import re

from block_timer.timer import Timer
import pandas as pd

from app_deploy_data.app_settings import DATABASE_CONFIG
from database.csv_to_sql import CreateTablesFromCSVs


sql_backend = "psql"
relevant_file_types = {
    "_fc_raw_log10_stats_wide_format.csv": "flow_stat_wide",
    "_platereader.csv": "plate_reader",
    "_fc_meta.csv": "flow_meta",
    "_od_growth_analysis.csv": "growth_rate",
    "time_diff_summary_reindexed.csv": "fc_time_diff",
    "inducer_diff_summary_reindexed.csv": "fc_inducer_diff",
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


def build_fluorescence_fold_change_tables(filepath):
    input_filename = os.path.basename(filepath)
    print(f"processing {filepath}")
    if input_filename.endswith("reindexed.csv"):
        # already processed
        return

    pattern = r"(^.*)__(fc_raw_log10_stats_\w+_diff_summary)_(\w+)\.csv$"
    match = re.match(pattern, input_filename)
    output_filename = (
        "_".join(
            [match.groups(0)[0], match.groups(0)[2], match.groups(0)[1], "reindexed"]
        )
        + ".csv"
    )
    data = pd.read_csv(filepath)
    if data.empty:
        return

    columns_lookup = {
        "fc_raw_log10_stats_time_diff_summary": [
            "strain",
            "inducer_concentration",
            "experiment_id",
            "well",
        ],
        "fc_raw_log10_stats_inducer_diff_summary": [
            "strain",
            "timepoint",
            "experiment_id",
        ],
    }
    index_columns_for_file = columns_lookup[match.groups(0)[1]]
    data[index_columns_for_file] = data["Unnamed: 0"].apply(
        lambda x: pd.Series(literal_eval(x))
    )

    data.drop(["Unnamed: 0", "sample_ids"], inplace=True, axis=1)
    output_filepath = os.path.join(os.path.dirname(filepath), output_filename)
    print(f"Writing output_filepath {output_filepath}")
    data.to_csv(output_filepath, index=False)


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

    # reformat broken indices for fluorescence diff files
    format_strs = [
        f"../yeast_states_app/yeast_states_data_files/{data_converge_output_path}/*/pdt_*_fc_raw_log10_stats_time_diff_summary*",
        f"../yeast_states_app/yeast_states_data_files/{data_converge_output_path}/*/pdt_*_fc_raw_log10_stats_inducer_diff_summary*",
    ]
    for format_str in format_strs:
        list_of_time_diff_files = glob(format_str)
        print(list_of_time_diff_files)
        for filepath in list_of_time_diff_files:
            build_fluorescence_fold_change_tables(filepath)

    sql_creator = CreateTablesFromCSVs(sql_backend, DATABASE_CONFIG)

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
            # replace nulls with placeholder to allow for selection in app
            for odd_null_column in ["control_type", "standard_type"]:
                if odd_null_column in data.columns:
                    data[odd_null_column] = data[odd_null_column].fillna(
                        "not_specified"
                    )
            key_column = None
            print(f"Creating table name {table_name} with {data.shape[0]} rows")
            sql_creator.create_new_table(
                table_name, data, schema, key_columns=key_column, if_exists="replace"
            )
        print(f"Elapsed time writing {table_name}: {t.elapsed} seconds")
