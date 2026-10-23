#!/usr/bin/python
#
########################################################################
# FILENAME: tt_create_dotr_dot10.py                            Mar. 2026
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

import numpy as np 
import pandas as pd 
import datetime as dt
from datetime import datetime, timedelta
import os, glob
import cal_file_setup
from cal_file_setup import cal_df, all_filenames

#base_path = all_filenames.loc['base_path'].values[0]
#base_path = all_filenames.loc['base_path'].values[0] %(year)

tt_dict = {'99601': {'Column_Names':['datetime','panel_temp','voltage', '30m temp' ,'15m temp','7m temp','4m temp','2m temp', '1m temp','pressure','1m wspd', '2m wspd', '30m wspd' ,'15m wspd'  ,'7m wspd', '4m wspd', '30m wdir','15m wdir','7m wdir' , '4m wdir', 'SW', 'LW', '30m RH', '7m RH', 'adg' ],'Columns':[1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,28] , 'Header':'STATION JulianDate Time(HHMMSS)       T1m(C)       T2m(C)       T4m(C)       T7m(C)      T15m(C)      T30m(C)        P(MB)   SPD1m(MPS)   SPD2m(MPS)   SPD4m(MPS)   DIR4m(DEG)   SPD7m(MPS)   DIR7m(DEG)  SPD15m(MPS)  DIR15m(DEG)  SPD30m(MPS)  DIR30m(DEG)      RH7m(%)     RH30m(%)       ADG(M)  SWnet(Wm^2)  LWnet(Wm^2)    LAT(deg)   LON(deg)','space':'------- ---------- ------------       ------       ------       ------       ------       ------       ------       ------   ----------   ----------   ----------   ----------   ----------   ----------  -----------  -----------  -----------  -----------      -------     --------       ------  -----------  -----------    --------   --------'},
'99616': {'Column_Names':['datetime','panel_temp','voltage', '1m temp', '2m temp', '4m temp', '7m temp', '15m temp', '30m temp', 'pressure', '1m wspd', '2m wspd', '4m wspd', '7m wspd', '15m wspd',  '30m wspd',  '1m wdir',  '2m wdir', '4m wdir', '7m wdir','15m wdir','30m wdir','4m RH', '7m RH', '15m RH', '30m RH', 'adg', 'sw_out',  'sw_in','lw_out', 'lw_in'],'Columns':[1,2,3,9,8,7,6,5,4,10,16,15,14,13,12,11,22,21,20,19,18,17, 30,28,26,24,33,38,39,44,45] , 'Header':'STATION JulianDate Time(HHMMSS)       T1m(C)       T2m(C)       T4m(C)       T7m(C)      T15m(C)      T30m(C)        P(MB)   SPD1m(MPS)   DIR1m(DEG)   SPD2m(MPS)   DIR2m(DEG)   SPD4m(MPS)   DIR4m(DEG)   SPD7m(MPS)   DIR7m(DEG)  SPD15m(MPS)  DIR15m(DEG)  SPD30m(MPS)  DIR30m(DEG)      RH4m(%)      RH7m(%)     RH15m(%)     RH30m(%)       ADG(M)  SWnet(Wm^2)  LWnet(Wm^2)    LAT(deg)   LON(deg)', 'space':'------- ---------- ------------       ------       ------       ------       ------      -------      -------        -----   ----------   ----------   ----------   ----------   ----------   ----------   ----------   ----------  -----------  -----------  -----------  -----------      -------      -------     --------     --------       ------  -----------  -----------    --------   --------'}}

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

year_abv = year[-2:]
col_names = tt_dict[argos_id]['Column_Names']
cols = tt_dict[argos_id]['Columns']

li = []
for filename in tt_files:
   
    df = pd.read_csv(filename,header=None, usecols=cols, names=col_names )
    df = df.set_index(pd.to_datetime(df['datetime']))
    li.append(df)

frame2 = pd.concat(li, axis=0, ignore_index=False)    
frame2['pressure'] = round((frame2['pressure'] + 600.), 1)

sw_dn = frame2['sw_in']
sw_up =  frame2['sw_out']
lw_dn = frame2['lw_in']
lw_up =  frame2['lw_out']
net_sw = sw_up - sw_dn
net_lw = lw_up - lw_dn
frame2['Net SW'] = net_sw
frame2['Net LW'] = net_lw
ob_num = list(range((145)))[1:]
sel_date = (frame2['datetime'].iloc[0])
grouped_byid = cal_df.groupby('ID', sort=False) 
keys = list(grouped_byid.groups.keys()) 
for key in keys:
    if key == argos_id_input or key == argos_id:
        id_group = grouped_byid.get_group(key)
        id_group['converted_date']=[pd.to_datetime(x, format='%Y%j') for x in id_group['Date']]
        
        id_group = id_group.set_index('converted_date')
        filtered_group = id_group[id_group.index <= sel_date]
        if not filtered_group.empty:
            closest_date_row = filtered_group.iloc[-1]  # Get the last row before sel_date
            print("Closest date row:", closest_date_row)
        else:
            print("No dates found before sel_date.")
aws_abbreviation = closest_date_row['Short_Name'] 
name = closest_date_row['Name'] 
lat = closest_date_row['Lat'] 
lon = closest_date_row['Lon'] 
elev = closest_date_row['Elevation'] 

frame2 = frame2[['1m temp', '2m temp', '4m temp', '7m temp', '15m temp', '30m temp', 'pressure', '1m wspd','1m wdir', '2m wspd', '2m wdir','4m wspd', '4m wdir', '7m wspd', '7m wdir', '15m wspd', '15m wdir', '30m wspd', '30m wdir', '4m RH','7m RH', '15m RH','30m RH', 'adg', 'Net SW', 'Net LW','panel_temp','voltage']]
timerange = pd.date_range(start=pd.Timestamp(year+'-'+month+'-01 00:00:00'), end=pd.Timestamp(year+'-'+month+'-01 23:50:00') + pd.offsets.MonthEnd(0),freq='10min')
reframe = frame2.reindex(timerange, fill_value='444.0')
reframe =reframe.astype(float).round(1)

jday = pd.to_datetime(reframe.index).strftime('%j')
reframe['jday'] = jday
reframe['year'] = year
dotr_df = reframe.copy()
len_df = len(reframe)
repeat_ob_num = (ob_num * int((len_df/144)))
dotr_df['ob_num'] = repeat_ob_num
dotr_df['ob_num'] = dotr_df['ob_num'].astype(int)
time = dotr_df.index
time_list = [str(x)[-8:-3].replace(':','') for x in time]
dotr_df['time'] = time_list
day_list = [x.day for x in dotr_df.index]
month_list = [x.month for x in dotr_df.index]
dotr_df['month']= month_list
dotr_df['day']= day_list
data = dotr_df[['year','jday','month','day','time','1m temp', '2m temp', '4m temp', '7m temp', '15m temp', '30m temp', 'pressure', '1m wspd', '1m wdir','2m wspd', '2m wdir', '4m wspd', '4m wdir', '7m wspd', '7m wdir', '15m wspd', '15m wdir', '30m wspd', '30m wdir','4m RH', '7m RH', '15m RH','30m RH', 'adg', 'Net SW', 'Net LW','panel_temp','voltage']]
data.round(1)
data.to_csv(tt_csv_output_path, index_label='datetime')

for var in dotr_df.columns:
    if var != 'time' and var != 'jday' and var != 'ob_num':
        
        dotr_df[var]=[round(float(x),2) for x in dotr_df[var]]
        if var == 'pressure':   
            dotr_df[var] = [str(x).rjust(7,' ') for x in dotr_df[var]]
        else:
            dotr_df[var] = [str(x).rjust(6,' ') for x in dotr_df[var]]
    if var == 'ob_num' or var == 'jday':
        dotr_df[var] = [str(x).rjust(5,' ') for x in dotr_df[var]]
dot10_df = dotr_df[['jday','ob_num','voltage','panel_temp']]
dotr_df = dotr_df[['jday','time','ob_num','1m temp', '2m temp', '4m temp', '7m temp', '15m temp', '30m temp', 'pressure', '1m wspd','1m wdir', '2m wspd','2m wdir', '4m wspd', '4m wdir', '7m wspd', '7m wdir', '15m wspd', '15m wdir', '30m wspd', '30m wdir', '4m RH','7m RH','15m RH' ,'30m RH']]
std_dotr_df = dotr_df[['jday','time','ob_num', '4m temp', 'pressure', '4m wspd', '4m wdir', '4m RH']]
dotr_header = "Year: "+str(year)+"  Month: "+str(month)+"  ID: "+aws_abbreviation+"  ARGOS: "+((str(argos_id_input).rjust(5, ' ')))+"  Name: "+name+"\nLat: "+str(lat)+"  Lon: "+str(lon)+"  Elev: "+str(elev)+"m"           

with open(tt_all_dotr_output_path, "w") as f:
    # Write the header
    f.write("".join(dotr_header) + "\n")
    # Write each row
    for row in dotr_df.itertuples( index=False,name=None):
        f.write(" ".join(map(str, row)) + "\n")
with open(tt_std_dotr_output_path, "w") as f:
    # Write the header
    f.write("".join(dotr_header) + "\n")
    # Write each row
    for row in std_dotr_df.itertuples( index=False,name=None):
        f.write(" ".join(map(str, row)) + "\n")
with open(tt_dot10_output_path, "w") as f:
    # Write the header
    f.write("".join(dotr_header) + "\n")
    # Write each row
    for row in dot10_df.itertuples( index=False,name=None):
        f.write(" ".join(map(str, row)) + "\n")
