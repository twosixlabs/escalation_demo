# Notes from Jed Session


Don’t show join keys if there is only one table option

Default to the correct axes options for graph types selected in UI

Smarter default layout dict heigh/width that isn’t 0. 

Float “buttons” div so it’s always visible on graph config page

x data dictionary button should probably have the name of the data dictionary in it. No need for “remove last data dictionary” button?

item 1, points 1 are not the best names

search for feature and where in the config it goes?

Groupby has - last item, but not the x. How can we be consistent across config wizard for interaction with these elements?

change yeast app to meet new data config schema

Adding graphic names with spaces in them cause server errors? This may actually be a race condition

todo: live edit dashboard- relaunch app with mounted app deploy data, don't rebuild whole container

Sanitize graph and page names- no / in names

If you rename the graph/page in the main config, can we rename the file rather than pointing to a new, empty file?

Closing properties button is hard

redirect dashboard/ to home for dashboard

Add edit button next to the json file names in the main config that let you edit the individual plots. Jed had to leave main config, and go to the individual page

Plotly icons greyed out makes them look unusable

Copy config files to make similar, but different plots- e.g, chymotrypsin instead of trypsin

Nice to have: "decimation" feature- only plot a random sample of a big data set.

Method not allowed; create another graph with same name as existing graph, create it on a page, get command doesn't work? 

Explicitly pass the args for each plotly graph- no defaults. List them all with defaults in the config wizard- provides visibility into what the options are for the user


# MVP Features

- Documentation for json config. Write from the perspective of a new user- how do you build one of these? What are the required fields? Point to the test configs as examples
- Document workflow for onboarding. What are the steps that a new user has to take to get this running on a local server?
- and link to external Docker deployment instructions (Heroku? AWS free tier?)
- Don't just validate schema format, but run functional/integration test validation of data against required requests defined in config. Can we run all of the Handler functions against each dataset using the config file to make sure we have consistency between a config and a newly-uploaded data file?
- Enforce no spaces or weird characters in column names. Note that we're lowercasing all columns in the sql upload. Do the same type of column sanitization in pandas for localcsv?
- change all examples to data in /escos/escalation/app_deploy_data
- better table

# Nice to have Features

## graphics functionality
- Move plot_manager to the top level of the config? I think we can assume we don't have more than one plot manager for a dashboard?
- Allow user to add their own hand-coded Plotly plots- where do they do the config, how is it included in the HTML?
- Save state of the website / user's preferences for graph configuration. Store the last form as a cookie and use it as the default? Store the form on the server side with a user-provided name and allow a user to select the form they want from a dropdown? This would work also as a way of sharing a graph config.
- Shareable graph configs- either a URL-encoded version for a GET that could be shared, or store a config server side that can be selected
- Break headers along underscores.

## Data management

- Data privacy- do we want to add some kind of key checking or password functionality?
- Add data download option (both most recent data and older versions of the data?), with a url endpoint (on its own blueprint)
- Data upload options: 1) direct upload via a web interface 2) API upload which will interact with versioned data, etc. These methods probably use the same controller/model functionality, and the direct upload is just a web interface to the functionality.
- Time data file uploads via app endpoint. The app is still using pg8000. Should we switch to psycopg2 at the cost of more annoying local development? Or separate settings for local/deployed?
## Wizard

- add pages in any order
- format/ validate form - use the dependencies
- add dependencies

## Config format

Simplify the config file- break it into one main config json with a separate config json for each page or graph?

## testing

- Mock sql backend for testing
- Test file upload

# USER STORIES

Real time data from fermenter (temp, pH) with updates on dashboard, including
