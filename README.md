# Escalation OS (EscOS)

## What is EscOS?
Escalation OS, or EscOS, is a lightweight visualization app for scientific labs. 
You can set up various plots and tables that can be viewed by others in your group.
 All that is required for is to set a config file, either by hand or using our UI builder, 
 and you can run your graphs either locally or on a server for others to view.
EscOS can provide insight to your lab what new experiments they should do. 
Additionally shows the most up to data for your group. 

## Wait, there are already many different visualization tools out there?
EscOS requires very little coding knowledge (unlike DASH) and is open source.
Unlike other open source visualizations tools (e.g. Metabase), 
EscOS is geared towards the scientific community. Allowing for plots 


## What are EscOS limitations?
As of the current version:
* Plots only a single line or scatter plot.
* Need to be connected to the internet
* Use a SQL database or local csv files (assuming csv in local handler)
* Local handler currently gets most recent data set
## Building a config file:
Run `python build_app_config_json_template.py` to build a starting file. 
Everything blank or in `<>` can be changed.

See 

The documentation is at [escalation_config](./escos.md "config file needed to use escalation OS") 


## How can I contribute?

### Developing for Escalation

- `pip install -r requirements-dev.txt`

- `pre-commit install` sets up the pre-commit hooks to auto-format the code

### How to add a new plot
* Needs to inherit from graphic_class.py
* Add to available_graphics.py
* Add a html file with javascript code required to plot

### How to add a new option feature
* add it to available_selectors.py
* create a html document input elements need name "\<id>|\<type>|<column_name>"
* add to create_data_subselect_info and reformat_filter_form_dict in controller.py
* build in functionality graphics_class or data_storer class
 