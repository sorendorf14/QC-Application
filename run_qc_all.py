#!/usr/bin/python
#
#
########################################################################
# FILENAME: run_qc_all.py                                      Mar. 2026
#
# PURPOSE: 
#
# AUTHOR: Sophie Orendorf
#         Antarctic Meteorological Research and Data Center
#         Space Science and Engineering Center
#         University of Wisconsin-Madison
#
########################################################################
# MODIFICATION HISTORY
#
# Created
# S. Orendorf March 2026
#
########################################################################
from pathlib import Path
from cal_file_setup import cal_df, all_filenames
import pandas as pd
import numpy as np
import os, glob

#input file of base path
base_path = all_filenames.loc['base_path'].values[0] 
#base_path = all_filenames.loc['base_path'].values[0] %(year)

stn_name = input("Enter the station name: ")
argos_id = input("Enter the station ID (#####): ")
month = input("Enter the month (MM): ")
year = input("Enter the year (YYYY): ")
qc_type = input("Show previous month (prev), next month (next), both prev and next months (both), or neither (none): ")
reload_data = input("Are you reloading previously QC'ed data? (yes/no): ")
if reload_data == 'yes':
    short_name = input("What is the short code for the AWS you are QCing? (aaa): ")

tt = input('Are you QCing a tall tower? (yes/no): ')

if tt == 'yes':
    create_dotr = input("Create .r file? (yes/no): ")
else:
    create_dotr = 'no'

cal_df = cal_df.set_index('Name')
try:
    stn_info_row = cal_df.loc[stn_name]
    closest_date_row = cal_df.loc[stn_name]
    stn_info = cal_df.loc[stn_name]
    name=stn_name
    aws_abbreviation = closest_date_row['Short_Name'] 
    short_name = aws_abbreviation.lower()
    name = stn_name
    lat = closest_date_row['Lat'] 
    lon = closest_date_row['Lon'] 
    elev = closest_date_row['Elevation'] 
    print(type(closest_date_row))
except KeyError:
    print("No station found in id.dat! Please input the information in id.dat or input it in the following prompts: ")
    if reload_data == 'no':
        aws_abbreviation = input('Enter short three letter station code in uppercase (AAA): ')
        short_name = aws_abbreviation.lower()
    elif reload_data == 'yes':
        aws_abbreviation = short_name.upper()
    lat = input("Enter station latitude (decimal notation): ")
    lon = input("Enter station longitude  (decimal notation): ")
    elev = input("Enter station elevation (meters): ")
    name = stn_name
    closest_date_row = pd.Series(['ID','Name','Lat','Lon','Elevation','Short_Name'])
    closest_date_row['Name']= stn_name
    closest_date_row['Short_Name']= aws_abbreviation
    closest_date_row['ID'] = argos_id      
    closest_date_row['Lat'] = lat
    closest_date_row['Lon'] = lon
    closest_date_row['Elevation'] = elev

#code paths
std_run_py_path = Path(all_filenames.loc['std_run_py_path'].values[0])
std_run_reload_py_path = Path(all_filenames.loc['std_run_reload_py_path'].values[0])

tt_run_py_path =Path(all_filenames.loc['tt_run_py_path'].values[0])
tt_create_dotr_py_path = Path(all_filenames.loc['tt_create_dotr_py_path'].values[0])
tt_run_reload_py_path = Path(all_filenames.loc['tt_run_reload_py_path'].values[0])

# remove leading zero from the station ID
if argos_id[0] == '0':
    argos_id_input = argos_id[1:]
else:
    argos_id_input = argos_id
    
year_abv = year[-2:]
if month != '01':
    prev_month = str((int(month) - 1)).rjust(2,'0')
    prev_year = year
    prev_year_abv = year_abv
if month == '01':
    prev_month = '12'
    prev_year = str((int(year) - 1))
    prev_year_abv = prev_year[-2:]

if month == '12':
    next_month = '01'
    next_year = str((int(year) + 1))
    next_year_abv = next_year[-2:]
if month != '12':
    next_month = str((int(month) + 1)).rjust(2,'0')
    next_year_abv = year_abv
    next_year = year

#general csv output paths
qc_csv_output_path  = all_filenames.loc['qc_csv_output_path'].values[0] %(argos_id,month,year_abv)
change_log_output_path  =  all_filenames.loc['change_log_output_path'].values[0] %(argos_id,month,year_abv)

#create tall tower .r, .csv, and .10 file from the daily tall tower files
if tt == 'yes' and create_dotr == 'yes':
    #name=stn_name
    #input paths 
    tt_files =  sorted(glob.glob(str(base_path) + str(all_filenames.loc['tt_files'].values[0]) %(name, year, month) + '*'))
    #tt_prev_file = sorted(glob.glob(base_path+name+'.'+str(prev_year)+str(prev_month)+'*'))[-1]
    #tt_files = sorted(glob.glob(base_path+name+'.'+str(year)+str(month)+'*'))
    
    #output paths
    tt_all_dotr_output_path = base_path + all_filenames.loc['tt_all_dotr_path'].values[0]  %(argos_id,month,year_abv)
    tt_std_dotr_output_path = base_path + all_filenames.loc['dotr_path'].values[0]  %(argos_id,month,year_abv)
    tt_dot10_output_path = base_path + all_filenames.loc['dot10_path'].values[0]  %(argos_id,month,year_abv)
    tt_csv_output_path=  base_path + all_filenames.loc['tt_csv_output_path'].values[0]  %(argos_id,month,year_abv)
    
    #run the python code to create TT .r, .csv, and .10 files
    exec(open(tt_create_dotr_py_path).read())
    
# standard QC file set up - not Tall Tower   
if tt == 'no': #or niwc == 'n'
    #input paths
    dotr_path = base_path + all_filenames.loc['dotr_path'].values[0] %(argos_id,month,year_abv)
    dot10_path = base_path + all_filenames.loc['dot10_path'].values[0] %(argos_id,month,year_abv)

    prev_month_dotr_path =base_path + all_filenames.loc['dotr_path'].values[0] %(argos_id,prev_month,prev_year_abv)
    prev_month_dot10_path = base_path +all_filenames.loc['dot10_path'].values[0] %(argos_id,prev_month,prev_year_abv)
    
    next_month_dotr_path = base_path +all_filenames.loc['dotr_path'].values[0] %(argos_id,next_month,next_year_abv)
    next_month_dot10_path = base_path +all_filenames.loc['dot10_path'].values[0] %(argos_id,next_month,next_year_abv)
    
    if reload_data == 'yes':
        #raw file setup
        raw_dotr_path = base_path + all_filenames.loc['raw_dotr_path'].values[0] %(short_name,year,month)
        raw_prev_month_dotr_path = base_path + all_filenames.loc['raw_dotr_path'].values[0] %(short_name,prev_year,prev_month)
        raw_next_month_dotr_path =base_path + all_filenames.loc['raw_dotr_path'].values[0] %(short_name,next_year,next_month)
        exec( open(std_run_reload_py_path).read())
    if reload_data == 'no':
        #run the python code to QC standard AWS data 
        exec( open(std_run_py_path).read())

if tt == 'yes':
    #input paths
    tt_csv_path =  base_path + all_filenames.loc['tt_csv_input_path'].values[0] %(argos_id,month,year_abv)
    tt_prev_month_csv_path = base_path + all_filenames.loc['tt_csv_input_path'].values[0] %(argos_id,prev_month,prev_year_abv)
    tt_next_month_csv_path =  base_path + all_filenames.loc['tt_csv_input_path'].values[0] %(argos_id,next_month,next_year_abv)
    if reload_data == 'yes': 
        #raw file path setup
        tt_raw_dotr_path = base_path +  all_filenames.loc['raw_dotr_path'].values[0] %(short_name,year,month)
        tt_raw_prev_month_dotr_path = base_path +  all_filenames.loc['raw_dotr_path'].values[0] %(short_name,prev_year,prev_month)
        tt_raw_next_month_dotr_path =  base_path + all_filenames.loc['raw_dotr_path'].values[0] %(short_name,next_year,next_month)
        
        exec( open(tt_run_reload_py_path).read())
    if reload_data == 'no':
        exec( open(tt_run_py_path).read())

    
