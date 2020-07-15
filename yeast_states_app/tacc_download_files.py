# runs from yeast_states_app path

import os
from retry import retry

from agavepy import Agave

ag = Agave.restore()
# pointers to relevant files
data_converge_output_path = "test/batch_20200713124857_master/"
pdt_run_name = "20200715100000"
pdt_output_path = "preview"


@retry(ConnectionError, delay=4, backoff=2, tries=3)
def get_file_from_tacc(system_id, filepath):
    return ag.files.download(systemId=system_id, filePath=filepath)


output_directory = "yeast_states_data_files"
data_converge_system_id = "data-sd2e-projects.sd2e-project-43"


experiments = ag.files.list(
    systemId=data_converge_system_id, filePath=data_converge_output_path
)
experiment_names = [
    x["name"] for x in experiments if x["name"].startswith("YeastSTATES")
]

relevant_file_types = ["_fc_raw_log10_stats.csv", "_platereader.csv", "_fc_meta.csv"]

for experiment_name in experiment_names:
    experiment_filepath = os.path.join(data_converge_output_path, experiment_name)
    experiment_files = ag.files.list(
        systemId=data_converge_system_id, filePath=experiment_filepath,
    )
    for file in experiment_files:
        if any(file["name"].endswith(x) for x in relevant_file_types):
            # print(file["name"])
            relevant_filepath = os.path.join(experiment_filepath, file["name"])
            res = get_file_from_tacc(data_converge_system_id, relevant_filepath)
            # agave's particular syntax
            output_folder = os.path.join(output_directory, experiment_filepath)
            output_filepath = os.path.join(output_folder, file["name"])
            # print(f"writing {relevant_filepath} to {output_filepath}")
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            with open(output_filepath, "w", encoding="utf8",) as fh:
                fh.write(res.text)
                fh.close()


# Get PDT data
pdt_system_id = "data-sd2e-projects.sd2e-project-48"
experiments = ag.files.list(systemId=pdt_system_id, filePath=pdt_output_path)
experiment_names = [
    x["name"] for x in experiments if x["name"].startswith("YeastSTATES")
]
print(experiment_names)

pdt_relevant_file_types = ["od_growth_analysis.csv"]
for experiment_name in experiment_names:
    experiment_filepath = os.path.join(
        pdt_output_path, experiment_name, pdt_run_name, "xplan-od-growth-analysis"
    )
    print(f"looking for files in {experiment_filepath}")
    experiment_files = ag.files.list(
        systemId=pdt_system_id, filePath=experiment_filepath,
    )
    for file in experiment_files:
        if any(file["name"].endswith(x) for x in pdt_relevant_file_types):
            relevant_filepath = os.path.join(experiment_filepath, file["name"])
            res = get_file_from_tacc(pdt_system_id, relevant_filepath)

            output_folder = os.path.join(
                output_directory, data_converge_output_path, experiment_name
            )
            output_filepath = os.path.join(output_folder, file["name"])
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            print(f"downloading {relevant_filepath} to {output_filepath}")
            with open(output_filepath, "w", encoding="utf8",) as fh:
                fh.write(res.text)
                fh.close()

        # todo: load the record.json and assert that the pdt file matches the data converge. Should only need to do once per pdt_run_name?
