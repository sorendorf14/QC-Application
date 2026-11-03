# Quality Control Application Code Package

All the code for both the standard and tall tower versions of the QC code. More information on the input files for the code, what runs when, and other explanations is in the [File Organization Wiki](https://github.com/sorendorf14/QC-Application/wiki/File-Organization-and-Setup).

## Folder Contents
* `cal_file_setup.py`
    * Code that sets up the the station information (latitude, longitude, etc.) from the `id.dat` file. 
* `run_qc_all.py`
    * Code that you run to initiate the code. This code sets up file paths and determines which code to run from the user's responses to prompts.
* `tt_create_dotr_dot10.py`
    * Code that concatenates daily tall tower files into a monthly dataset and converts into file formats matching the standard `.r` and `.10` files in the standard format that the AMRDC uses. It also outputs a monthly csv 
* `get_data.py`
    * Standard AWS QC code that opens up the application using the original AWS files. 
* `get_data_TT.py`
    *  Tall tower version of the AWS QC code that opens up the application using the tall tower AWS files created in `tt_create_dotr_dot10.py`. 
* `reload_raw_get_data.py`
    * Standard AWS reload QC code that opens up the application using previously QC'ed output files.
* `reload_raw_get_data_TT.py`
    * Tall tower reload version of the AWS QC code that opens up the application using previously QC'ed output files. 



