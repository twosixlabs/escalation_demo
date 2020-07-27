# How to set up a local file system for EscOS
In the config file, you need 
1. "data_backend": "local_csv".
2. "data_file_directory": <path (relative or absolute) ending with folder_with_data>.
The application assumes that your data structure is laid out something like: 
    - <folder_with_data>  
       - <data_source_1_folder>
           - <data_source_1_file_1>.csv
           - <data_source_1_file_2>.csv
       - <data_source_2_folder>
           - <data_source_2_file_1>.csv
           - <data_source_2_file_2>.csv
           - <data_source_2_file_3>.csv
       - <data_source_3_folder>
           - <data_source_3_file_1>.csv  
3. "data_sources":\[<data_source_1_folder>,<data_source_2_folder>, etc.\] -- list of folders that contain the data
 the application will use. All csv files in the same folder should have the same schema.
  By default, it will use all the csv files in the folder.
This can be changed on the Admin tab on the webpage.
4. available_pages.<page_name>.graphics.<graphic_name>.data_sources -- list of which data sources the graphic uses and 
instructions on how to combine the files
    - the first element of the list will look like {
    "data_source_type": <data_source>
}, this gives the first folder to find the data for this graphic.
 If your graphic only needs the data in this folder no more items in this list are needed.
    - the second item in the list will look like {
    "data_source_type": <another_data_source>,
"join_keys": \[
    \[
        <data_source>:<column_name>,
        <another_data_source>:<column_name>,
    \], etc.]} -- The second folder that has your data. The application will perform a left 
    join between the data in the first folder and this data using the pairs of keys as specified in the join_keys list.
    - And so on, as many folders as the graphic needs

**All columns in the config file should be referenced as** <data_source_folder>:<column_name>
## Example
Consider the [local_data_example.json](local_data_example.json)
with the following file structure at relative path
tests/test_data/:
- test_data/
   - penguin_size/
       - main_data.csv
       - gentoo_data.csv
   - mean_penguin_stat/
       - only_file_mean_penguin_stat.csv
    