# MVP Features


- Document workflow for onboarding. What are the steps that a new user has to take to get this running on a local server?
- Document building the Docker container version of the app, running from container, and link to external Docker deployment instructions (Heroku? AWS free tier?)
- Don't just validate schema format, but run functional/integration test validation of data against required requests defined in config. Can we run all of the Handler functions against each dataset using the config file to make sure we have consistency between a config and a newly-uploaded data file?
- Enforce no spaces or weird characters in column names. Note that we're lowercasing all columns in the sql upload. Do the same type of column sanitization in pandas for localcsv?
- Fix bug in filter if the filter value has a space in the string, can't select?
- change all examples to data in /escos/escalation/app_deploy_data
- yeast states pages all long
- admin and upload have the left hand gap
- Documentation for json config. Write from the perspective of a new user- how do you build one of these? What are the required fields? Point to the test configs as examples  
    - File tree page needs to do something
        - Edit Config buttons
        - add a graphic
        - add a page
    - editor page
        - submit button needs to write a json file
        - take in previous config file
    

# Nice to have Features

## graphics functionality
- Move plot_manager to the top level of the config? I think we can assume we don't have more than one plot manager for a dashboard?
- Use more of the screen real estate. How is Plotly deciding how big to make a plot? How can we control it?
- Sometimes opening a filter selector, with long strings, results in the selector stretching past the right edge of the screen and introducing a horizontal scroll bar- you can't see which options you've selected
- Allow user to add their own hand-coded Plotly plots- where do they do the config, how is it included in the HTML?
- Save state of the website / user's preferences for graph configuration. Store the last form as a cookie and use it as the default? Store the form on the server side with a user-provided name and allow a user to select the form they want from a dropdown? This would work also as a way of sharing a graph config.
- Shareable graph configs- either a URL-encoded version for a GET that could be shared, or store a config server side that can be selected
- Allow user to select which columns to use for group by in plotly (color labels) based on drop down
- Break headers along underscores.

## Data management

- Add data download option (both most recent data and older versions of the data?), with a url endpoint (on its own blueprint)
- Data upload options: 1) direct upload via a web interface 2) API upload which will interact with versioned data, etc. These methods probably use the same controller/model functionality, and the direct upload is just a web interface to the functionality.

## Wizard

- improve the pop up boxes.
- add pages in any order
- toll tips buttons
- format form

## Config format

Simplify the config file- break it into one main config json with a separate config json for each page or graph?

## testing

- Mock sql backend for testing
- Test file upload

# USER STORIES

Real time data from fermenter (temp, pH) with updates on dashboard, including



