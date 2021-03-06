# To Triage

- add a single test case that does multiple requests on the same session, asserting that the cookie addendum dict starts 
empty, then preserves a round of filters after one request is made, and finally handles the fields being rewritten 
on another request. I think the current_app and request context may handle that nicely.


# Nick 

- Cookbook examples for app deployment and integration: example scripts to integrate data uploads from GitLFS
- Wizard: Scope this: numerical filters can have defaults via wizard. Put an inequality selector in the wizard? Estimate work.
- Remove all assert False tests- add actual tests

- Scope: Light data Processor functionality for data diagnostics: 
    - Error bars for scatter plot: in case we want to live-calculate error bars (stddev?)
    - Can we apply functions to data to annotate graph- e.g., calculate correlation coefficient for filtered data
    - Processor class, reads config json explaining which data to use, how to apply a function, and what gets returned. Pass to render or to plotly? Include in plot title? Annotation?
- Test file upload
- what isn't tested now- a survey. pytest test coverage? Or nosetest? Python tools


# Alexander

- Cool summary screenshots to put into the readme. Penguin test with formatted axes labels, showing tooltips, maybe change opacity- just make it snazzier
- Investigate feasibility: rich hover text- images? HTML?
- Fix Selenium basic page load test
- what isn't tested now- a survey
- Joining a table to itself in the wizard causes errors- don't let the user do this. Can we edit the dropdown so additional data sources don't contain main data source? Has to update when main data source change.


## Unassigned/Maybe do

- Scope: can we build a URL POST request with a graph name/URL + cookie to share a filtered/configured graph with a copy-pastable link
    - Save state of the website / user's preferences for graph configuration. Store the last form as a cookie and use it as the default? Store the form on the server side with a user-provided name and allow a user to select the form they want from a dropdown? This would work also as a way of sharing a graph config.
    - Shareable graph configs- either a URL-encoded version for a GET that could be shared, or store a config server side that can be selected

# ToDo Work by category

## graphics functionality
- Allow user to add their own hand-coded Plotly plots- where do they do the config, how is it included in the HTML?

- Nice to have: "decimation" feature- only plot a random sample of a big data set.
- Default settings for appearance- opacity < 1?


## Data management

- Data privacy- do we want to add some kind of key checking or password functionality?
- Render validation error response on file upload in HTML rather than printing json

## Wizard
- Allow Tables in the wizard
- Ability to rearrange panels
- Ability to rearrange graphs in panel
- search for feature (opacity, hover text) and where in the config it goes
- in-line documentation to configuration wizard-Add a second column to the config wizard that explains the properties that can be edited in a specific dropdown? Lots of hover text?
- reloading the editor after a post generates the same post effects again- duplicating the new additions
- Bug: restarts on "Detected change in '/usr/local/lib/python3.7/encodings/__pycache__/unicode_escape.cpython-37.pyc', reloading", happens in container debug mode on launch

## Testing
- Test a configured app. Don't just validate schema format, but run functional/integration test validation of data against required requests defined in config. Can we run all of the Handler functions against each dataset using the config file to make sure we have consistency between a config and a newly-uploaded data file?
    - e.g., join a main and additional data source that are the same- we should be able to catch this kind of error
       
## Deployment
- How much RAM do we need to handle big data files? Can we stream things more efficiently than Pandas is doing?
- add link to external Docker deployment instructions (Heroku? AWS free tier? Google Cloud Run?)

## Miscellaneous
- change confirm/alert boxes to modals/make them better. Deleting pages, deactivate all data sources in Admin

# User stories to support

Real time data from fermenter (temp, pH) with updates on dashboard
Data-enabled publication. Upload static set of data and interactive viz to accompany a paper
