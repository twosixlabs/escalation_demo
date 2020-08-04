# Escalation

## What is Escalation?
Escalation is a web app that runs a lightweight visualization dashboard for data analysis. 
You can set up plots and tables that update along with your data or analysis, and have interactivity options to allow for data browsing.

Some user cases for Escalation:
- An academic lab that wants to have better visibility into experiments conducted by its members, or an at-a-glance record of experimental progress
- A project team at a small company that wants to share progress or up to date results with management

All that is required for is to set a config file, either by hand or using the included UI Configuration Wizard, 
and you can run Escalation locally or on a server for others to view.

You can see an example of Escalation running on data for DARPA's Synergistic Discovery and Design program [here](http://escos.sd2e.org/). We also have a demo app (ToDo: Include link to Penguin demo app instructions)


## Wait, aren't there already lots of different visualization tools out there?
Yes. Escalation has a few advantages:
- Straightforward and low-cost deployment
- Improved data privacy: everything can be local
- Open-source code
- Integration with data versioning and analysis pipelines (In development)


## What are the limitations of Escalation?
As of the current version:
* Plots only a single line or scatter plot.
* Need to be connected to the internet
* Use a SQL database or local csv files (assuming csv in local handler)
* Local handler currently gets most recent data set

[Documentation](config_information/config_documentation/escos.md) for the config files

# Setup

## What do you need for the app to work?

Each of these components are discussed further below.

- Configuration files
    - Escalation uses configuration files (json) to build the dashboard organizational structure, link the data in visualizations, and construct the visualizations themselves.
    - These configuration files can be built by hand, using the Configuration Wizard, or any combination of the two
- Data 
    - When setting up Escalation, you choose to use either a CSV or SQL backend.
    - Depending on the backend, you'll either link the app to a database (new or existing) or a file system path containing your data files. 
     A file backend may be easier for those unfamiliar with SQL, but SQL is more performant, and storing data in a database offers advantages beyond the database's use in Escalation
    - Escalation includes tooling to ingest CSV files into SQL, automatically building the necessary SQL data tables and the code necessary to integrate them with Escalation.
    - ToDo: Data Migration helpers- what happens when the format of your data changes over time?
- Python environment to run the app
    - You need a Python environment set up to run the web app. See instructions for setting up an environment, using Docker to handle the environment for you.


## Building Configuration files:
Run `python build_app_config_json_template.py` to build a base config file. 
Everything blank or in `<>` should be changed.

How to set up [local file system and config](config_information/local_example/local_data_storage_config_info.md) for the app.  
An example of a [main config file](config_information/main_config_example/main_config_example.md).  
Examples of [different plots and graphic config files](config_information/plotly_examples/plotly_config_info.md).  
Examples of [different selectors](config_information/selector_examples/selector_config_info.md). 


## Loading your data

### SQL data
    
Todo: Instructions for SQL data ingestion

### CSV data

Todo: Instructions for CSV data
    
## Running the app

### Running Locally (testing, development of your custom Escalation dashboard)

You can run the app in a Docker container locally. You can also set up a custom Python virtual environment and run the server locally as you would any other Flask web app. 
ToDo: More detailed instructions on virtual env setup, requirements install,  and running the app 

### Running Escalation as a web-accessible server
We have Dockerized Escalation for ease of maintaining code compatibility and dependencies. Running via Docker containers is recommended. 
We recognize that Docker is less common in academic settings, but highly recommend using it. 
Here are [Docker's instructions](https://docs.docker.com/get-started/) on getting started using Docker.

With Docker set up, you 



# How can I contribute? (advanced)

### Developing for Escalation

- `pip install -r requirements-dev.txt`
- `pre-commit install` sets up the pre-commit hooks to auto-format the code. This is optional, the repo is formatted with Flake and Black. 


### How to add a new type of plot
Development for Escalation has focused on Plotly, but the code base should be compatible with other libraries or custom graphics. If you want to use something other than Plotly, your code should:
* Needs to inherit from graphic_class.py
* Be added to available_graphics.py
* Include an html file with javascript code required to plot

### How to add a new option feature
* add it to available_selectors.py
* create a html document input elements need name "\<id>|\<type>|<column_name>"
* add to create_data_subselect_info and reformat_filter_form_dict in controller.py
* build in functionality graphics_class or data_storer class
 

# License

The Apache 2.0 License applies to all code and materials associated with Escalation.


Copyright \[2020] \[Two Six Labs, LLC]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

