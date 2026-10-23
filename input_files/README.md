# Input File Package Readme

## Example Input Files
You will need files like these as input, but these are just examples of AMRDC's AWS data.  Edit your AWS file formats to match these input file format or alter the code to read in your data format. Some of these files only need to have certain lines of the file altered (e.g., filenames.csv), where others need to be redone for your AWS information (id.dat) and data (e.g., 089000320.r)

There is further information on the file naming formats, file path explanation, and how some of these are input to the code using filenames.csv in the [File Organization Wiki Page]().

Some of the input files are also output files, depending on what version of the code you are running (e.g., hry202003raw.txt).

The following table will outline each input file within this folder, an explanation of the file, and the generic file naming scheme. If you alter the naming scheme in both the code and `filenames.csv`, this will not be relevant; however, it will give you an idea of what is needed for input data to run the code (even if you have different file formatting). The first table will be the standard file format and usage. The second table will cover the different files needed for the tall tower version of the code. A rreadme (link) gives column/variable information for all of the files .

<img width="1000" height="610" alt="qc_file_workflow" src="https://github.com/user-attachments/assets/eba52d4f-d4ae-4f96-9658-e27eb3ccaea0" />

444.0 are missing data . different section to where peopne would need to edit the code if they dont want to match our input files. (line numbers, code definition). 
Example of standard AWS with Harry AWS (ID:08900) for November 2020.
## Standard AWS File List
| Input File  | Explanation | File Naming Format |
| ------------- | ------------- | ------------- |
| 089001120.r | Input data file with standard meteorological variables (temperature, pressure, wind speed, wind direction, and relative humidity). The file naming is station ID number, month, and year abbreviation - last two digits of the year. | #####MMYY.r |
| 089001120.10 | File that is similar in format and data content to the .r file previously defined, but has two additional variables: voltage and panel temperature. If you have different file formatting, you will need to edit the code where the data are read in to match your data. If you wish to remove the option to have a .10 file, you will need to edit the code appropriately. The file naming is station ID number, month, and year abbreviation - last two digits of the year. | #####MMYY.10 |
| hry202011raw.txt | Example of a raw output file that is created when you save your QC progress. It saves the normal data, the data that were removed during the QC process, and the data that qualified for any of the QC rules. The file naming is a lowercase abbreviation, year, and month. | aaaYYYYMMraw.txt |
| id.dat  | A csv or text file with all Automatic Weather Station (AWS) information that is read in that details the station name, station ID number, abbreviated station name (AAA), latitude (decimal degrees), longitude (decimal degrees), and elevation (meters). There are three different examples of file formatting that is supported by this code. Edit to replace with all of your station data.  | id.dat |
| filenames.csv | File that is read in by `cal_file_setup.py` that details all of the file path and names to the python code, output/input directories, and input/output file names. **Make sure that you edit this file and replace the text with your directories! Make sure your input files follow the formatting in this file or edit the file to match your file formatting.** | filenames.csv |

| | | |
| | | |
| | | |
| | | |

.10 
potential changes

filenames.csv

setting up for our .r files and their formatting. will need to be some changes depending on the input files, file type, please have id file that is the same. A rreadme (link) gives column/variable information.

explain tall tower file differences
Example of tall tower AWS with Elijah Tall Tower AWS (ID: 99616) for January 2025.
## Tall Tower File List
filenames.csv and id.dat are also used. if the data were previously QC'ed, the raw file detailed above will be used as defined above, but with additional variables. 
| Example Input File  | Explanation | File Naming Format |
| ------------- | ------------- | ------------- |
| ElijahTallTower.20250121.txt| Daily input files that are used in `tt_create_dotr_dot10.py` to create a csv file, along with standard and all variable .r, .10 files. A rreadme (link) gives column/variable information.  All the files for the month are read into the code to create one monthly file. | Name.YYYYMMDD.txt|
| 996160125.csv | Monthly csv file with input data. The file naming is station ID number, month, year abbreviation - last two digits of the year. | #####MMYY.csv |
