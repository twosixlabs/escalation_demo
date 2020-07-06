# MVP Features

- Add navigation toolbar to the top of the page that lets you move between dashboard/upload/download pages
- implement a web app interface selector for which of the uploaded data files gets rendered, storing this as application state
- Documentation for json config. Write from the perspective of a new user- how do you build one of these? What are the required fields? Point to the test configs as examples
- Document workflow for onboarding. What are the steps that a new user has to take to get this running on a local server?
- Choose and add a software license to Escalation OS
- Don't just validate schema format, but run functional/integration test validation of data against required requests defined in config. Can we run all of the Handler functions against each dataset using the config file to make sure we have consistency between a config and a newly-uploaded data file?
- Enforce no spaces or weird characters in column names. Note that we're lowercasing all columns in the sql upload. Do the same type of column sanitization in pandas for localcsv?


# Nice to have Features

## graphics functionality

- Allow user to add their own hand-coded Plotly plots- where do they do the config, how is it included in the HTML?
- Save state of the website / user's preferences for graph configuration. Store the last form as a cookie and use it as the default? Store the form on the server side with a user-provided name and allow a user to select the form they want from a dropdown? This would work also as a way of sharing a graph config.
- Shareable graph configs- either a URL-encoded version for a GET that could be shared, or store a config server side that can be selected
- Allow user to select which columns to use for group by in plotly (color labels) based on drop down

## Data management

- Which version of the data do we display? Management page to select "Active data files" or "active sql row keys" which get loaded. May combine multiple files/keys into single graph
- Add data download option (both most recent data and older versions of the data?), with a url endpoint (on its own blueprint)
- Data upload options: 1) direct upload via a web interface 2) API upload which will interact with versioned data, etc. These methods probably use the same controller/model functionality, and the direct upload is just a web interface to the functionality.

## Multi Select

- tooltip explaining how to use

## Config format

Simplify the config file- break it into one main config json with a separate config json for each page or graph?

## testing

- Mock sql backend for testing
- Test file upload

# USER STORIES

Real time data from fermenter (temp, pH) with updates on dashboard, including


