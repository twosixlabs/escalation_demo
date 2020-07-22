# How to set up local file system for EscOS

  
- <folder_with_data>  
   - <data_source_1>
       - <data_source_1_file_1>.csv
       - <data_source_1_file_2>.csv
   - <data_scource_2>
       - <data_source_2_file_1>.csv
       - <data_source_2_file_2>.csv
       - <data_source_2_file_3>.csv
   - <data_scource_3>
       - <data_source_3_file_1>.csv

## Example
Consider the local_data_example.json
with the following file structure at relative path
tests/test_data/:
- test_data/
   - penguin_size/
       - main_data.csv
       - gentoo_data.csv
   - mean_penguin_stat/
       - only_file_mean_penguin_stat.csv

Now the lines in the config json dealing with data storage will be explained  
"data_backend": "local_csv" -- The data is being stored as csv files (opposed to e.g. in a database)  
"data_sources": \[
        "penguin_size",
        "mean_penguin_stat"
    \] -- Name of folders in path which be used in this config
    
Now in the config at
available_pages.penguins.graphics.graphic_0.data_sources: [
{
    "data_source_type": "penguin_size"
} - first folder to find the data your graph only needs the data in tha 


{
    "data_source_type": "mean_penguin_stat",
    "join_keys": [