"""
Copyright [2020] [Two Six Labs, LLC]

This script converts ths incidents portion of the CA fire incidents json to csv and uploads it to the Escalation dashboard for visualization
"""

import pandas as pd
import json

with open('incidents.json', 'r') as fin:
    incidents = json.load(fin)
incidents_df = pd.DataFrame(incidents['Incidents'])
# fill acres burned to placeholder for plotting
incidents_df['AcresBurned'] = incidents_df['AcresBurned'].fillna(1)
# # rename all columns to lowercase for convenience
# incidents_df = incidents_df.rename(columns={k: k.lower() for k in incidents_df.columns})
incidents_df.to_csv('incidents.csv', index=False)