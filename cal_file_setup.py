#!/usr/bin/python
#
########################################################################
# FILENAME: cal_file_setup.py                                  Nov. 2024
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
# S. Orendorf Nov 2024
#
########################################################################
import numpy as np
import os
import pandas as pd 
#all_filenames = pd.read_csv('/Users/sorendorf/Desktop/filenames_sophie_stable.csv',usecols=[0,1],index_col='var_name')
all_filenames = pd.read_csv('/Users/sorendorf/Desktop/filenames_notamrdc.csv',usecols=[0,1],index_col='var_name')

#id_file = '/Users/sorendorf/Desktop/id-c.dat'
#id_csv = '/Users/sorendorf/Desktop/id_dat.csv'

cal_file = all_filenames.loc['cal_file'].values[0] 
if os.path.exists(cal_file) and 'calib' in str(cal_file):
    id_list = []
    name_list = []
    lat_list = []
    lon_list = []
    el_list = []
    short_list = []
    date_list = []
    cal_df = pd.DataFrame(columns=['ID','Name','Short_Name','Date','Lat','Lon','Elevation'])
    final_cal_df = pd.DataFrame(columns=['ID','Name','Short_Name','Date','Lat','Lon','Elevation'])
    ird_stn_df = pd.DataFrame(columns=['ID','Name','Short_Name','Date','Lat','Lon','Elevation'])
    with open(cal_file, 'r') as f2:
        num_aws = int(f2.readline()[-4:].strip())
        print(num_aws)
        for line in f2:  
            if not line.startswith("C"):
                if len(line) == 84 :
                    stn_id = line[0:5].strip()
                    date=line[6:13]
                    stn_name=line[14:35].strip()
                    lat=line[37:44]
                    lon=line[45:53]
                    elevation = line[55:60].strip()
                    el_list.append(elevation)
                    date_list.append(date)
                    lon_list.append(lon)
                    lat_list.append(lat)
                    name_list.append(stn_name)
                    id_list.append(stn_id)
                    
                elif len(line) == 80 or len(line) == 81:
                    short_stn_name=line[-5:].strip()
                    if len(short_stn_name) == 0:
                        pass
                    else:
                        short_list.append(short_stn_name) 
                elif len(line) == 86 or len(line)==85:
                    short_stn_name=line[-10:-7]
                    short_list.append(short_stn_name)                   
        cal_df['Elevation'] = el_list
        cal_df["Lon"] = lon_list
        cal_df["Lat"] = lat_list
        cal_df["ID"]=id_list
        cal_df["Name"]=name_list
        cal_df["Date"]=date_list
        cal_df['Short_Name']= short_list    
    print('opened cal file')

elif os.path.exists(cal_file) and 'csv' in cal_file:
    cal_df = pd.read_csv(cal_file,sep=',',header=None,dtype=str)
    print('Loaded CSV')
elif os.path.exists(cal_file) and 'dat' in cal_file:
    cal_df = pd.read_csv(cal_file,sep='\s\s+', dtype='str',header=None,engine='python')
    
    print('Loaded text file')
    try:
        cal_df.columns = ['Name','ID','Short_Name','Lat','Lon','Elevation']
        print('Loaded id.dat with Station ID')
    except:
        cal_df.columns = ['Name','Short_Name','Lat','Lon','Elevation']
        #id_df = pd.read_csv(id_file,sep='\s\s+', dtype='str',names=['Name','Short_Name','Lat','Lon','Elevation'],engine='python')
        #id_df = pd.read_csv(id_file,sep='\s{2,}', names=['Name','Short_Name','Lat','Lon','Elevation'],engine='python')
        # You can comment the following out if you do not want any changes made to the lat/lon
        cal_df['Lon'] = np.where(cal_df['Lon'].str[0] == '-',cal_df['Lon'].str.strip('-')+'W', cal_df['Lon']+'E') 
        cal_df['Lat'] = np.where(cal_df['Lat'].str[0] == '-',cal_df['Lat'].str.strip('-')+'S', cal_df['Lat']+'N')
        print(cal_df)
        print('Loaded id.dat without Station ID and altered lat/lon to match formatting')
else:
    print('No ID file found. Check file path or id file. ')
