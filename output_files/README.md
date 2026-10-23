# Output File Package Readme

## Example Input Files
These are the files output after you successfully run the QC application, but these are just examples of AMRDC's AWS data.  Edit your AWS file formats to match these input file format or alter the code to read in your data format. Some of these files only need to have certain lines of the file altered (e.g., filenames.csv), where others need to be redone for your AWS information (id.dat) and data (e.g., 089001120.r)

There is further information on the file naming formats, file path explanation, and how some of these are input to the code using filenames.csv in the [File Organization Wiki Page]().

Some of the input files are also output files, depending on what version of the code you are running (e.g., hry202011raw.txt).

The following table will outline each input file within this folder, an explanation of the file, and the generic file naming scheme. If you alter the naming scheme in both the code and `filenames.csv`, this will not be relevant; however, it will give you an idea of what is needed for input data to run the code (even if you have different file formatting). The first table will be the standard file format and usage. The second table will cover the different files needed for the tall tower version of the code. A rreadme (link) gives column/variable information for all of the files. Example of standard AWS with Harry AWS (ID:08900) for November 2020.

<img width="1000" height="610" alt="qc_file_workflow" src="https://github.com/user-attachments/assets/eba52d4f-d4ae-4f96-9658-e27eb3ccaea0" />

Missing data are represented by 444.0 in AMRDC's files. 

## Standard AWS File List
| Input File  | Explanation | File Naming Format |
| ------------- | ------------- | ------------- |
| hry202011raw.txt | Monthly quality controlled data with all standard meteorological variables at one level. | aaaYYYYMMraw.txt |
| hry202011q10.txt | Monthly 10-minute quality (QC'ed) controlled data with all standard meteorological variables at one level. | aaaYYYYMMq10.txt |
| hry202011q1h.txt | Monthly 1-hourly QC'ed data with all standard meteorological variables at one level. | aaaYYYYMMq1h.txt |
| hry202011q3h.txt | Monthly 3-hourly QC'ed data with all standard meteorological variables at one level. | aaaYYYYMMq3h.txt |
| 089001120_qc_output.csv  | Backup csv file that outputs the QC'ed data. Since it is a backup, it is not formatted as well as the normal output data. | #####MMYY_qc_output.csv |
| 089001120_change_log.csv | Log file outputting all the data removed for one month during the QC process. Shows the date and time of the removed data, variable removed, the changed value, and the replaced value. | #####MMYY_change_log.csv |

setting up for our .r files and their formatting. will need to be some changes depending on the input files, file type, please have id file that is the same. A rreadme (link) gives column/variable information.

explain tall tower file differences
Example of tall tower AWS with Elijah Tall Tower AWS (ID: 99616) for January 2025.


## Tall Tower Generating Monthly Files List
These files will only be output if you run `tt_create_dotr_dot10.py` to match the standard formatting of AMRDC's data files. Only variables at 4m will be included in the standard .r files, but all standard meteorological variables at all heights are included in the files with `_all` included in the file name. The csv is a standard csv with all the standard meteorological variables at all levels. Refer to "  COLUMN README  " for further explanation  

| Example Input File  | Explanation | File Naming Format |
| ------------- | ------------- | ------------- |
| 996160125.r | Monthly .r file with one level of data with standard meteorological variables. The file naming is station ID number, month, year abbreviation - last two digits of the year. | #####MMYY.r |
| 996160125_all.r | Monthly .r file with ALL output data. The file naming is station ID number, month, year abbreviation - last two digits of the year. | #####MMYY.r |
| 996160125.10 | Monthly .10 file with output data. The file naming is station ID number, month, year abbreviation - last two digits of the year.| #####MMYY.10 |
| 996160125.csv | Monthly csv file with output data. The file naming is station ID number, month, year abbreviation - last two digits of the year. | #####MMYY.csv |


## Tall Tower QC App Additional File List
 if the data were previously QC'ed, the raw file detailed above will be used as defined above, but with additional variables. The files in the standard file output list will be output as well as the following files. 

| Example Output File  | Explanation | File Naming Format |
| ------------- | ------------- | ------------- |
| elj202501q10_all.txt | Monthly 10-minute QC data with all standard meteorological variables at all levels. | aaaYYYYMMq10_all.txt |
| elj202501q1h_all.txt | Monthly 1-hourly QC data with all standard meteorological variables at all levels. | aaaYYYYMMq1h_all.txt |
| elj202501q3h_all.txt | Monthly 3-hourly QC data with all standard meteorological variables at all levels. | aaaYYYYMMq3h_all.txt |

What each column is for each code. The files that have column names are not included.

| Column # | .r | .10 | .10 tall tower |   | raw.txt | q10, q1h, and q3h.txt | change log csv | qc change log csv | _all.r |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| 1 | Julian day | Station ID | Julian Day |  |  |  |  |  |  |  
| 2 | Observation number of the day  | Julian day | Observation Number |  |  |  |  |  |  |   
| 3 | Temperature | Time (HHMMSS) | Voltage |  |  |  |  |  |  |  
| 4 | Pressure | Temperature | Panel Temperature |  |  |  |  |  |  |  
| 5 | Wind Speed | Panel Temperature |  |  |  |  |  |  |  |  
| 6 | Wind Direction | Pressure |  |  |  |  |  |  |  |   
| 7 | Relative Humidity | Wind Direction |  |  |  |  |  |  |  |  
| 8 | deltaT | Wind Speed |  |  |  |  |  |  |  |  
| 9 |  | n/a |  |  |  |  |  |  |  |  
| 10 |  | Relative Humidity |  |  |  |  |  |  |  |   
| 11 |  |  Wind Gust? |  |  |  |  |  |  |  |  
| 12 |  | 1 |  |  |  |  |  |  |  |  
| 13 |  | 2 |  |  |  |  |  |  |  |  
| 14 |  | 3 |  |  |  |  |  |  |  |  
| 15 |  | 4 |  |  |  |  |  |  |  |  
| 16 |  |  |  |  |  |  |  |  |  |  
