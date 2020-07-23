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
Run `python build_app_config_json_template.py` to build a base config file. 
Everything blank or in `<>` should be changed.

How to set up [local file system and config](config_information/local_example/local_data_storage_config_info.md) for the app  
See an example of a [simple config](config_information/config_example/config_example.md) file (Recommended)  
See examples of [different plots](config_information/plotly_examples/plotly_config_info.md)   
After creating a json run validate_schema.py to verify that the config has been set up properly.

[Documentation](config_information/config_documentation/escos.md) for the config files


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