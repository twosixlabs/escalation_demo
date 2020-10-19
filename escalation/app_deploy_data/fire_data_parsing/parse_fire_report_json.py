"""
Copyright [2020] [Two Six Labs, LLC]

This script converts ths incidents portion of the CA fire incidents json to csv and uploads it to the Escalation dashboard for visualization
"""

import json
import requests

import pandas as pd

ESCALATION_APP_UPLOAD_ENDPOINT = "http://escalation-demo.sd2e.org/upload"
TABLE_NAME = "california_fires"


incidents_filepath = "escalation/app_deploy_data/fire_data_parsing/incidents.json"
with open(incidents_filepath, "r") as fin:
    incidents = json.load(fin)
incidents_df = pd.DataFrame(incidents["Incidents"])
# fill acres burned to placeholder for plotting
incidents_df["AcresBurned"] = incidents_df["AcresBurned"].fillna(1)
# # rename all columns to lowercase for convenience
# incidents_df = incidents_df.rename(columns={k: k.lower() for k in incidents_df.columns})
incidents_df.to_csv(incidents_filepath, index=False)


notes = "Uploaded by Gitlab continuous integration scraper"


response = requests.post(
    ESCALATION_APP_UPLOAD_ENDPOINT,
    data={"data_source": TABLE_NAME, "username": "ci scraper", "notes": notes,},
    files={"csvfile": open(incidents_filepath, "rb")},
)
if response.status_code != 200:
    raise Exception(response.status_code)
