# To Triage
- Bug: crashes if the graphic config references data sources that do not exist. 
- Bug: program crashes if models.py does not exist
- Cool summary screenshots to put into the readme. Penguin test with formatted axes labels, showing tooltips, maybe change opacity- just make it snazzier
- add a single test case that does multiple requests on the same session, asserting that the cookie addendum dict starts 
empty, then preserves a round of filters after one request is made, and finally handles the fields being rewritten 
on another request. I think the current_app and request context may handle that nicely.

# Next release todo Features

## Nick

- Group by selector option processing in backend doesn't allow a "None" option. Can we include- switch between grouping and not in one graph
- models.py not refreshed when docker down run on volumes to handle any reset
- Light data Processor functionality for data diagnostics: 
    - Error bars for scatter plot: in case we want to live-calculate error bars (stddev?)
    - Can we apply functions to data to annotate graph- e.g., calculate correlation coefficient for filtered data
    - Processor class, reads config json explaining which data to use, how to apply a function, and what gets returned. Pass to render or to plotly? Include in plot title? Annotation?
- Legend
    - Clean up the Plotly modebar- remove useless buttons https://plotly.com/javascript/configuration-options/#hide-the-plotly-logo-on-the-modebar. Use Add Buttons to ModeBar functionality to add legend hide/show toggle
    - (not urgent) Add showlegend toggle to wizard graph config (field goes in plot_specific_info:layout)- default on/off
    - (won't do) Customize what goes into the legend from groupby args- some strings are long and repetitive
    - (won't do) Legend string shortening?

## Alexander

## Unassigned/Maybe do

- Wizard: numerical filters can have defaults via wizard. Put an inequality selector in the wizard?


# ToDo Work by category

## graphics functionality
- Allow user to add their own hand-coded Plotly plots- where do they do the config, how is it included in the HTML?
- Save state of the website / user's preferences for graph configuration. Store the last form as a cookie and use it as the default? Store the form on the server side with a user-provided name and allow a user to select the form they want from a dropdown? This would work also as a way of sharing a graph config.
- Shareable graph configs- either a URL-encoded version for a GET that could be shared, or store a config server side that can be selected
- Nice to have: "decimation" feature- only plot a random sample of a big data set.
- rich hover text- images? HTML?
- Default settings for appearance- opacity < 1?


## Data management

- Data privacy- do we want to add some kind of key checking or password functionality?
- Add data download option (both most recent data and older versions of the data?), next to identifiers on admin page
- script to update models.py. Integrate with delete db to clear db but leave metadata
- Render validation error response on file upload in HTML rather than printing json

## Wizard
- Allow Tables in the wizard
- Ability to rearrange panels
- Ability to rearrange graphs in panel
- search for feature (opacity, hover text) and where in the config it goes
- in-line documentation to configuration wizard-Add a second column to the config wizard that explains the properties that can be edited in a specific dropdown? Lots of hover text?
- reloading the editor after a post generates the same post effects again- duplicating the new additions

## Testing
- Don't just validate schema format, but run functional/integration test validation of data against required requests defined in config. Can we run all of the Handler functions against each dataset using the config file to make sure we have consistency between a config and a newly-uploaded data file?
- Test file upload

## Deployment
- How much RAM do we need to handle big data files? Can we stream things more efficiently than Pandas is doing?
- add link to external Docker deployment instructions (Heroku? AWS free tier? Google Cloud Run?)


# User stories to support

Real time data from fermenter (temp, pH) with updates on dashboard
Data-enabled publication. Upload static set of data and interactive viz to accompany a paper
