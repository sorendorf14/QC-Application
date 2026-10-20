#!/usr/bin/python
#
#
########################################################################
# FILENAME: reload_raw_get_data_TT.py                          Mar. 2026
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
#
########################################################################
import plotly.graph_objects as go 
import plotly 
from pathlib import Path

from plotly.subplots import make_subplots 
import numpy as np 
import pandas as pd 
from dash import dcc, html, Input, Output, dash_table, callback, Dash, State 
import dash 
import plotly.express as px
import dash_ag_grid as dag
import datetime as dt
from datetime import datetime, timedelta 
from dash.exceptions import PreventUpdate
import os, glob
import cal_file_setup
from cal_file_setup import cal_df, all_filenames
#from cal_file_setup import cal_df, niwc_df, all_filenames, year 

base_path = all_filenames.loc['base_path'].values[0] 
#base_path = all_filenames.loc['base_path'].values[0] %(year)
#setting flask setting to only display output in terminal when there is an error
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

tt_dict = {'99601': {'Column_Names_10':['jday','ob_num','voltage','panel_temp'] ,'Column_Names_raw':['date','full_time','year','jday','month','day','time','1m temp','1m temp_man_qc','1m temp_rules','2m temp','2m temp_man_qc','2m temp_rules','4m temp','4m temp_man_qc','4m temp_rules','7m temp','7m temp_man_qc','7m temp_rules','15m temp','15m temp_man_qc','15m temp_rules','30m temp','30m temp_man_qc','30m temp_rules','pressure','pressure_man_qc','pressure_rules','1m wspd','1m wspd_man_qc','1m wspd_rules','2m wspd','2m wspd_man_qc','2m wspd_rules','4m wspd','4m wspd_man_qc','4m wspd_rules','7m wspd','7m wspd_man_qc','7m wspd_rules','15m wspd','15m wspd_man_qc','15m wspd_rules','30m wspd','30m wspd_man_qc','30m wspd_rules','4m wdir','4m wdir_man_qc','4m wdir_rules','7m wdir','7m wdir_man_qc','7m wdir_rules','15m wdir','15m wdir_man_qc','15m wdir_rules','30m wdir','30m wdir_man_qc','30m wdir_rules','7m RH','7m RH_man_qc','7m RH_rules','30m RH','30m RH_man_qc','30m RH_rules'], 'blank_cols':20},
'99616': {'Column_Names_10':['jday','ob_num','voltage','panel_temp'] ,'Column_Names_raw':['date','full_time','year','jday','month','day','time','1m temp','1m temp_man_qc','1m temp_rules','2m temp','2m temp_man_qc','2m temp_rules','4m temp','4m temp_man_qc','4m temp_rules','7m temp','7m temp_man_qc','7m temp_rules','15m temp','15m temp_man_qc','15m temp_rules','30m temp','30m temp_man_qc','30m temp_rules','pressure','pressure_man_qc','pressure_rules','1m wspd','1m wspd_man_qc','1m wspd_rules','2m wspd','2m wspd_man_qc','2m wspd_rules','4m wspd','4m wspd_man_qc','4m wspd_rules','7m wspd','7m wspd_man_qc','7m wspd_rules','15m wspd','15m wspd_man_qc','15m wspd_rules','30m wspd','30m wspd_man_qc','30m wspd_rules','1m wdir','1m wdir_man_qc','1m wdir_rules','2m wdir','2m wdir_man_qc','2m wdir_rules','4m wdir','4m wdir_man_qc','4m wdir_rules','7m wdir','7m wdir_man_qc','7m wdir_rules','15m wdir','15m wdir_man_qc','15m wdir_rules','30m wdir','30m wdir_man_qc','30m wdir_rules','4m RH','4m RH_man_qc','4m RH_rules','7m RH','7m RH_man_qc','7m RH_rules','15m RH','15m RH_man_qc','15m RH_rules','30m RH','30m RH_man_qc','30m RH_rules'], 'blank_cols':24}}

if argos_id == '99601':
    name = 'AlexanderTallTower'
elif argos_id  == '99616':
    name = 'ElijahTallTower'
    
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
    
df = pd.read_csv(tt_raw_dotr_path,sep='\s+',skiprows=tt_dict[argos_id]['blank_cols'],na_values=['444.0',444.0,444,'444',' 444.0'],names=tt_dict[argos_id]['Column_Names_raw']) #,dtype='str'
csv_df = pd.read_csv(tt_csv_path,sep=',',na_values=['444.0',444.0,444,' 444.0','444'],dtype='str',header=0) 

df['datetime'] = df['date']+' '+df['full_time']
df['datetime'] = pd.to_datetime(df['datetime'])

df = df.set_index('datetime')
csv_df['datetime']= pd.to_datetime(csv_df['datetime'])
csv_df = csv_df.set_index('datetime')

volt = csv_df['voltage']
ptemp = csv_df['panel_temp']

df['voltage'] = volt
df['panel_temp'] = ptemp    
if qc_type == 'prev' or qc_type == 'both':

    prev_month_df = pd.read_csv(tt_raw_prev_month_dotr_path,sep='\s+',skiprows=tt_dict[argos_id]['blank_cols'],na_values=['444.0',444.0,'444'],names=tt_dict[argos_id]['Column_Names_raw'])
    prev_month_csv_df = pd.read_csv(tt_prev_month_csv_path,dtype='str',sep=',',na_values=['444.0',444.0,'444'],header=0) 

    prev_month_csv_df['datetime']= pd.to_datetime(prev_month_csv_df['datetime'])
    prev_month_csv_df =prev_month_csv_df.set_index('datetime')
    prev_month_df['datetime']=prev_month_df['date']+ ' '+prev_month_df['full_time']
    prev_month_df['datetime'] = pd.to_datetime(prev_month_df['datetime'])
    prev_month_df = prev_month_df.set_index('datetime')
    prev_month_df['year'] = prev_year
    
    first_day = df.index[0]
    three_days_ago =df.index[0] - timedelta(days=3)
    
    prev_month_df['voltage'] = prev_month_csv_df['voltage']
    prev_month_df['panel_temp'] = prev_month_csv_df['panel_temp']
    last_days_df = prev_month_df.loc[three_days_ago:first_day]
    last_days_dot10_df = prev_month_csv_df.loc[three_days_ago:first_day]
    cat_df = pd.concat([ last_days_df, df])

if qc_type == 'next' or qc_type == 'both':

    next_month_df = pd.read_csv(tt_raw_next_month_dotr_path,sep='\s+',skiprows=tt_dict[argos_id]['blank_cols'],na_values=['444.0',444.0,'444'],names=tt_dict[argos_id]['Column_Names_raw'],dtype='str')
    next_month_csv_df = pd.read_csv(tt_next_month_csv_path,sep=',',na_values=['444.0',444.0,'444'],dtype='str',header=0) 
    
    next_month_csv_df['datetime']= pd.to_datetime(next_month_csv_df['datetime'])
    next_month_csv_df =next_month_csv_df.set_index('datetime')
    next_month_df['datetime']=next_month_df['date']+ ' '+next_month_df['full_time']
    next_month_df['datetime'] = pd.to_datetime(next_month_df['datetime'])
    next_month_df = next_month_df.set_index('datetime')
    next_month_df['year'] =next_year

    first_day = next_month_df.index[0]
    next_three_days = next_month_df.index[0] + timedelta(days=3)
    
    next_month_df['voltage'] = next_month_csv_df['voltage']
    next_month_df['panel_temp'] = next_month_csv_df['panel_temp']
    next_few_days_df = next_month_df.loc[first_day:next_three_days]
    next_few_days_dot10_df = next_month_csv_df.loc[first_day:next_three_days]
    
    if qc_type == 'both':
        cat_df = pd.concat([cat_df, next_few_days_df])
    if qc_type == 'next':
        cat_df = pd.concat([df, next_few_days_df])
noqc_df = df.copy()

noqc_df['1m temp'] = noqc_df['1m temp'].fillna(noqc_df['1m temp_man_qc'])
noqc_df['2m temp'] = noqc_df['2m temp'].fillna(noqc_df['2m temp_man_qc'])
noqc_df['4m temp'] = noqc_df['4m temp'].fillna(noqc_df['4m temp_man_qc'])
noqc_df['7m temp'] = noqc_df['7m temp'].fillna(noqc_df['7m temp_man_qc'])
noqc_df['15m temp'] = noqc_df['15m temp'].fillna(noqc_df['15m temp_man_qc'])
noqc_df['30m temp'] = noqc_df['30m temp'].fillna(noqc_df['30m temp_man_qc'])

noqc_df['1m wspd'] = noqc_df['1m wspd'].fillna(noqc_df['1m wspd_man_qc'])
noqc_df['2m wspd'] = noqc_df['2m wspd'].fillna(noqc_df['2m wspd_man_qc'])
noqc_df['4m wspd'] = noqc_df['4m wspd'].fillna(noqc_df['4m wspd_man_qc'])
noqc_df['7m wspd'] = noqc_df['7m wspd'].fillna(noqc_df['7m wspd_man_qc'])
noqc_df['15m wspd'] = noqc_df['15m wspd'].fillna(noqc_df['15m wspd_man_qc'])
noqc_df['30m wspd'] = noqc_df['30m wspd'].fillna(noqc_df['30m wspd_man_qc'])

noqc_df['4m wdir'] = noqc_df['4m wdir'].fillna(noqc_df['4m wdir_man_qc'])
noqc_df['7m wdir'] = noqc_df['7m wdir'].fillna(noqc_df['7m wdir_man_qc'])
noqc_df['15m wdir'] = noqc_df['15m wdir'].fillna(noqc_df['15m wdir_man_qc'])
noqc_df['30m wdir'] = noqc_df['30m wdir'].fillna(noqc_df['30m wdir_man_qc'])

noqc_df['7m RH'] = noqc_df['7m RH'].fillna(noqc_df['7m RH_man_qc'])
noqc_df['30m RH'] = noqc_df['30m RH'].fillna(noqc_df['30m RH_man_qc'])

if argos_id == '99616':
    noqc_df['4m RH'] = noqc_df['4m RH'].fillna(noqc_df['4m RH_man_qc'])
    noqc_df['15m RH'] = noqc_df['15m RH'].fillna(noqc_df['15m RH_man_qc'])
    noqc_df['1m wdir'] = noqc_df['1m wdir'].fillna(noqc_df['1m wdir_man_qc'])
    noqc_df['2m wdir'] = noqc_df['2m wdir'].fillna(noqc_df['2m wdir_man_qc'])

noqc_df['pressure'] = noqc_df['pressure'].fillna(noqc_df['pressure_man_qc'])
qc_df = df.copy()
if argos_id == '99601':
    qc_df = qc_df.drop(columns=['1m temp_man_qc','2m temp_man_qc','4m temp_man_qc','7m temp_man_qc','15m temp_man_qc','30m temp_man_qc','pressure_man_qc','1m wspd_man_qc','2m wspd_man_qc','4m wspd_man_qc','7m wspd_man_qc','15m wspd_man_qc','30m wspd_man_qc','4m wdir_man_qc','7m wdir_man_qc','15m wdir_man_qc','30m wdir_man_qc','7m RH_man_qc','30m RH_man_qc','1m temp_rules','2m temp_rules','4m temp_rules','7m temp_rules','15m temp_rules','30m temp_rules','pressure_rules','1m wspd_rules','2m wspd_rules','4m wspd_rules','7m wspd_rules','15m wspd_rules','30m wspd_rules','4m wdir_rules','7m wdir_rules','15m wdir_rules','30m wdir_rules','7m RH_rules','30m RH_rules'])
if argos_id == '99616':
    qc_df = qc_df.drop(columns=['1m temp_man_qc','2m temp_man_qc','4m temp_man_qc','7m temp_man_qc','15m temp_man_qc','30m temp_man_qc','pressure_man_qc','1m wspd_man_qc','2m wspd_man_qc','4m wspd_man_qc','7m wspd_man_qc','15m wspd_man_qc','30m wspd_man_qc','1m wdir_man_qc','2m wdir_man_qc','4m wdir_man_qc','7m wdir_man_qc','15m wdir_man_qc','30m wdir_man_qc','4m RH_man_qc','7m RH_man_qc','15m RH_man_qc','30m RH_man_qc','1m temp_rules','2m temp_rules','4m temp_rules','7m temp_rules','15m temp_rules','30m temp_rules','pressure_rules','1m wspd_rules','2m wspd_rules','4m wspd_rules','7m wspd_rules','15m wspd_rules','30m wspd_rules','1m wdir_rules','2m wdir_rules','4m wdir_rules','7m wdir_rules','15m wdir_rules','30m wdir_rules','4m RH_rules','7m RH_rules','15m RH_rules','30m RH_rules'])    
variables = qc_df.columns

color_1m = 'forestgreen' 
color_2m= 'black'
color_4m= 'blueviolet'
color_7m= 'brown'
color_15m= 'rebeccapurple'
color_30m= 'olivedrab'
error_1m = 'orange'
error_2m = 'magenta'
error_4m = 'goldenrod'
error_7m = 'palevioletred'
error_15m = 'darkkhaki'
error_30m = 'coral'
qc_1m = 'dodgerblue'
qc_2m = 'deepskyblue'
qc_4m = 'seagreen'
qc_7m = 'aquamarine'
qc_15m = 'cadetblue'
qc_30m = 'cornflowerblue'
solid_color_df = pd.DataFrame(index=df.index,columns=['1m temp_colors','2m temp_colors','4m temp_colors','7m temp_colors','15m temp_colors','30m temp_colors','pressure_colors','4m RH_colors','15m RH_colors','1m wspd_colors','2m wspd_colors','4m wspd_colors','7m wspd_colors','15m wspd_colors','30m wspd_colors','4m wdir_colors','7m wdir_colors','15m wdir_colors','30m wdir_colors','voltage_colors','panel_temp_colors']) 
for var in variables:
    #print(var)
    if var != 'panel_temp' and var != 'date' and var != 'voltage' and var != 'time' and var != 'full_time' and var != 'year' and var != 'jday' and var != 'month' and var != 'day':
        if var[0:2] == '1m':
            var_conditional = (qc_df[var].notna() & df[var+'_rules'].notna())
            var_colors =np.where( qc_df[var].isna(),qc_1m, np.where(var_conditional,error_1m,color_1m)).tolist()
            df[var+'_colors'] = var_colors
            qc_df[var+'_colors'] = var_colors
            df[var+'_noerrorcolor']=color_1m
            qc_norules_colors =np.where( qc_df[var].isna(),qc_1m,color_1m).tolist()
            solid_color_df[var+'_colors'] = qc_norules_colors
        elif var[0:2] == '2m':
            var_conditional = (qc_df[var].notna() & df[var+'_rules'].notna())
            var_colors = np.where( qc_df[var].isna(),qc_2m, np.where(var_conditional,error_2m,color_2m)).tolist()   
            qc_norules_colors =np.where( qc_df[var].isna(),qc_2m,color_2m).tolist()
            solid_color_df[var+'_colors'] = qc_norules_colors
            df[var+'_colors'] = var_colors
            qc_df[var+'_colors'] = var_colors
            df[var+'_noerrorcolor']=color_2m
        elif var[0:2] == '4m':
            var_conditional = (qc_df[var].notna() & df[var+'_rules'].notna())
            var_colors =np.where( qc_df[var].isna(),qc_4m, np.where(var_conditional,error_4m,color_4m)).tolist()
            df[var+'_colors'] = var_colors
            qc_df[var+'_colors'] = var_colors
            df[var+'_noerrorcolor']=color_4m
            qc_norules_colors = np.where( qc_df[var].isna(),qc_4m,color_4m).tolist()
            solid_color_df[var+'_colors'] = qc_norules_colors
        elif var[0:2] == '7m':
            var_conditional = (qc_df[var].notna() & df[var+'_rules'].notna())
            var_colors =np.where( qc_df[var].isna(),qc_7m, np.where(var_conditional,error_7m,color_7m)).tolist()
            qc_norules_colors =np.where( qc_df[var].isna(),qc_7m,color_7m).tolist()
            solid_color_df[var+'_colors'] = qc_norules_colors
            df[var+'_colors'] = var_colors
            qc_df[var+'_colors'] = var_colors
            df[var+'_noerrorcolor']=color_7m
        elif var[0:3] == '15m':
            var_conditional = (qc_df[var].notna() & df[var+'_rules'].notna())
            var_colors =np.where( qc_df[var].isna(),qc_15m, np.where(var_conditional,error_15m,color_15m)).tolist()
            qc_norules_colors =np.where( qc_df[var].isna(),qc_15m,color_15m).tolist()
            solid_color_df[var+'_colors'] = qc_norules_colors
            df[var+'_colors'] = var_colors
            qc_df[var+'_colors'] = var_colors
            df[var+'_noerrorcolor']=color_15m
        elif var[0:3] == '30m':
            var_conditional = (qc_df[var].notna() & df[var+'_rules'].notna())
            var_colors =np.where( qc_df[var].isna(),qc_30m, np.where(var_conditional,error_30m,color_30m)).tolist()
            qc_norules_colors =np.where( qc_df[var].isna(),qc_30m,color_30m).tolist()
            solid_color_df[var+'_colors'] = qc_norules_colors
            df[var+'_colors'] = var_colors
            qc_df[var+'_colors'] = var_colors
            df[var+'_noerrorcolor']=color_30m
        elif var == 'pressure':
            var_conditional = (qc_df[var].notna() & df[var+'_rules'].notna())
            var_colors =np.where( qc_df[var].isna(),qc_2m, np.where(var_conditional,error_2m,color_2m)).tolist()
            qc_norules_colors =np.where( qc_df[var].isna(),qc_2m,color_2m).tolist()
            solid_color_df[var+'_colors'] = qc_norules_colors
            df[var+'_colors'] = var_colors
            qc_df[var+'_colors'] = var_colors
            df[var+'_noerrorcolor']=color_2m

qc_df['panel_temp_colors'] = 'darkseagreen'
qc_df['voltage_colors'] = color_2m 
df['panel_temp_colors'] = 'darkseagreen'
df['voltage_colors'] = color_2m 
#print(df.columns)
solid_color_df['panel_temp_colors'] = 'darkseagreen' 
solid_color_df['voltage_colors']=color_2m  
#print(solid_color_df.columns)
copied_solid_color_df = solid_color_df.copy()  


app = Dash(__name__)
#df = df.replace([444.0,'444.0'], np.nan)
#qc_df.fillna(444.0,inplace=True)
copied_df = qc_df.copy()

if qc_type == 'none':
    cat_df = df

#cat_df = cat_df.replace([444.0,'444.0'], np.nan)
cat_copy_df = cat_df.copy()
change_log = []
#copied_df.drop(['voltage', 'panel_temp'], axis=1, inplace=True)

variables = ['temp','pressure','wspd','wdir','RH','panel_temp', 'voltage']
full_var = ['Temperature','Pressure','Wind Speed', 'Wind Direction', 'Relative Humidity','Panel Temperature', 'Voltage']
var_opt_list = []

for variable, full in zip(list(variables),full_var):
    temporary_dict = {'label':str(full), 'value':str(variable)}
    var_opt_list.append(temporary_dict)
    
app.layout = html.Div([
    html.H1(children="QC Test Platform - Reload (Tall Tower)"),
    dcc.Checklist(options=var_opt_list,value=['temp','pressure'],id='select-variables', inline=True),
    dcc.Checklist(options=['1m ','2m ','4m ','7m ','15m ','30m '],value=['1m '],id='select-level', inline=True),
    html.H2(children="   "+closest_date_row['Name']+" ("+str(argos_id)+")      "+str(month)+"    "+str(year)+"\n"),
    html.Label(['Select Marker Size:']),
    dcc.RadioItems(options=['2','4','6','8','10','12','14','16'],value='6',inline=True,id='marker-size'),
    html.Br(),
    html.Label(['Select X-Axis Limits: ']),
    html.Br(),
    dcc.Input(placeholder='Day range: ', type='number',value='',id='day-range', min=0, max=32, debounce=False, autoComplete='on',size='5'),
    dcc.Input(placeholder='Center Day: ', type='number',value='',id='center-day', min=0, max=32, debounce=False, autoComplete='on',size='5'),
    html.Br(),
    html.Label(['Select Y-Axis Limits: ']),
    html.Br(),
    dcc.Input(placeholder='Min Temp: ', type='number',value='',id='min-temp-ylim', min=-120, max=60, debounce=False, autoComplete='on',size='5'),
    dcc.Input(placeholder='Min Pres: ', type='number',value='',id='min-pres-ylim', min=0, max=1200, debounce=True, autoComplete='on',size='5'),
    dcc.Input(placeholder='Min WSpd: ', type='number',value='',id='min-wspd-ylim', min=-10, max=200, debounce=True, autoComplete='on',size='5'),
    dcc.Input(placeholder='Min WDir: ', type='number',value='',id='min-wdir-ylim', min=-10, max=400, debounce=True, autoComplete='on',size='5'),
    dcc.Input(placeholder='Min RH: ', type='number',value='',id='min-rh-ylim', min=-20, max=120, debounce=True, autoComplete='on',size='5'),
    html.Br(),
    dcc.Input(placeholder='Max Temp: ', type='number',value='',id='max-temp-ylim', min=-120, max=60, debounce=False, autoComplete='on',size='5'),
    dcc.Input(placeholder='Max Pres: ', type='number',value='',id='max-pres-ylim', min=0, max=1200, debounce=True, autoComplete='on',size='5'),
    dcc.Input(placeholder='Max WSpd: ', type='number',value='',id='max-wspd-ylim', min=-10, max=150, debounce=True, autoComplete='on',size='5'),
    dcc.Input(placeholder='Max WDir: ', type='number',value='',id='max-wdir-ylim', min=-10, max=400, debounce=True, autoComplete='on',size='5'),
    dcc.Input(placeholder='Max RH: ', type='number',value='',id='max-rh-ylim', min=-20, max=120, debounce=True, autoComplete='on',size='5'),
    html.Br(),
    html.Label(['Show Rules? ']),
    dcc.RadioItems(options=['Yes','No'],value='Yes',inline=True,id='rules-toggle'),
    html.Br(),
    dcc.Graph(figure={}, id='display-met-data-subplots',config={'displayModeBar': True,"doubleClick":False}),
    dcc.Textarea(id='display-hover-data1',style={'width':'15%', 'height':210}),
    dcc.Textarea(id='display-hover-data2',style={'width':'15%', 'height':210}),
    dcc.Textarea(id='display-hover-data4',style={'width':'15%', 'height':210}),
    dcc.Textarea(id='display-hover-data7',style={'width':'15%', 'height':210}),
    dcc.Textarea(id='display-hover-data15',style={'width':'15%', 'height':210}),
    dcc.Textarea(id='display-hover-data30',style={'width':'15%', 'height':210}),

    dcc.Textarea(id='display-click-data',value='select data point',style={'width':'25%', 'height':50}),
    html.Button('Undo', id='undo-button'),  
    html.Button('Reset', id='reset-button'),
    html.Button('Save Data', id='save-button'),
    dcc.Download(id="download-dataframe-csv"),
    dcc.Download(id="download-qc-log-csv"),
    dash_table.DataTable(
        id='change-log',
        columns=[
            {"name": "Date", "id": "date"},
            {"name": "Column", "id": "column"},
            {"name": "Original Value", "id": "original"},
            {"name": "New Value", "id": "new"}],data=[]  ),
    dash_table.DataTable(
        id='updated-data',
        columns=[{"name": col, "id": col} for col in copied_df.columns],
        data=copied_df.to_dict('records'))])

if argos_id == '99601':
    @callback(Output('display-met-data-subplots','figure'),
        Input('select-variables','value'),
        Input('select-level','value'),
        Input('marker-size','value'),
        Input('day-range','value'),
        Input('center-day','value'),
        Input('min-temp-ylim','value'),
        Input('max-temp-ylim','value'),
        Input('min-pres-ylim','value'),
        Input('max-pres-ylim','value'),
        Input('min-wspd-ylim','value'),
        Input('max-wspd-ylim','value'),
        Input('min-wdir-ylim','value'),
        Input('max-wdir-ylim','value'),
        Input('min-rh-ylim','value'),
        Input('max-rh-ylim','value'),
        Input('rules-toggle','value'),) 
    
    def update_graph(variables_selected,levels_selected,markersize,day_range,center_day,mintemp,maxtemp,minpres,maxpres,minwspd,maxwspd,minwdir,maxwdir,minrh,maxrh,rules):
        level_vars = [level + var for level in levels_selected for var in variables_selected if var != 'panel_temp' and var != 'voltage' and var != 'pressure' and var != 'RH' and var != 'wdir']
        for level in levels_selected:
            for var in variables_selected: 
                if var == 'wdir':
                    if level == '4m ' or level == '7m ' or level == '15m ' or level == '30m ':
                        level_vars.append(level+var)
                if var == 'RH':
                    if level == '7m ' or level == '30m ':
                        level_vars.append(level+var)
        
        if 'pressure' in variables_selected: level_vars.append('pressure')
        if 'panel_temp' in variables_selected: level_vars.append('panel_temp')
        if 'voltage' in variables_selected: level_vars.append('voltage')
    
        use_list_vars = level_vars 
        level_colors = [level+var for level in levels_selected for var in variables_selected if var != 'panel_temp' and var != 'voltage' and var != 'pressure' and var != 'wdir' and var != 'RH']
        for level in levels_selected:
            for var in variables_selected: 
                if var == 'wdir':
                    if level == '4m ' or level == '7m ' or level == '15m ' or level == '30m ':
                        level_colors.append(level+var)
                if var == 'RH':
                    if level == '7m ' or level == '30m ':
                        level_colors.append(level+var)
        
        if 'pressure' in variables_selected: level_colors.append('pressure')
        if 'panel_temp' in variables_selected: level_colors.append('panel_temp')
        if 'voltage' in variables_selected: level_colors.append('voltage')
    
        dff = noqc_df[use_list_vars]
        
        bounds_dict= {'mintemp':mintemp,'maxtemp':maxtemp,'minpres':minpres,'maxpres':maxpres,'minwspd':minwspd,'maxwspd':maxwspd,'minwdir':minwdir,'maxwdir':maxwdir,'minRH':minrh,'maxRH':maxrh}
        ind_dict = {}
        copy_dff = dff.copy()
        
        """
        if 'panel_temp' in dff.columns and 'RH' not in variables_selected and 'wdir' not in variables_selected:
            titles = variables_selected
            titles.remove('panel_temp')
        """


        if 'panel_temp' in dff.columns:
            titles = variables_selected
            titles.remove('panel_temp')

        elif 'RH' in variables_selected and '7m RH' not in dff.columns and '30m RH' not in dff.columns and 'panel_temp' not in dff.columns and 'wdir' not in variables_selected :
            titles = variables_selected
            titles.remove('RH')      
    
        elif 'panel_temp' not in dff.columns and 'RH' not in variables_selected and 'wdir' in variables_selected  and '4m wdir' not in dff.columns and '7m wdir' not in dff.columns and '15m wdir' not in dff.columns and '30m wdir' not in dff.columns: 
            titles = variables_selected
            titles.remove('wdir')  
            
        elif 'panel_temp' in dff.columns and 'RH' not in variables_selected and 'wdir' in variables_selected and '4m wdir' not in dff.columns and '7m wdir' not in dff.columns and '15m wdir' not in dff.columns and '30m wdir' not in dff.columns:
            titles = variables_selected
            titles.remove('panel_temp')    
            titles.remove('wdir')      
    
        elif 'panel_temp' not in dff.columns and 'RH' in variables_selected  and '7m RH' not in dff.columns and '30m RH' not in dff.columns and 'wdir' in variables_selected and '4m wdir' not in dff.columns and '7m wdir' not in dff.columns and '15m wdir' not in dff.columns and '30m wdir' not in dff.columns:
            titles = variables_selected
            titles.remove('RH')    
            titles.remove('wdir')  
        elif 'RH' in variables_selected and '7m RH' not in dff.columns and '30m RH' not in dff.columns and 'panel_temp' in dff.columns and 'wdir' not in variables_selected:
            titles = variables_selected
            titles.remove('RH') 
            titles.remove('panel_temp')
        
        elif 'RH' in variables_selected and '7m RH' not in dff.columns and '30m RH' not in dff.columns and 'panel_temp' in dff.columns and 'wdir' in variables_selected and '4m wdir' not in dff.columns and '7m wdir' not in dff.columns and '15m wdir' not in dff.columns and '30m wdir' not in dff.columns:
            titles = variables_selected
            titles.remove('RH') 
            titles.remove('panel_temp')
            titles.remove('wdir')  
        else:
            titles = variables_selected
        marker=False 
        fig = make_subplots(rows=len(titles), cols=1,subplot_titles=titles,
                            shared_xaxes=True, 
                            vertical_spacing=0.05, x_title='Date')
        for i, var in enumerate(variables_selected):
            i2 = i+1      
            if var != 'panel_temp':
                ind_dict[var+'_ind'] = i2
                #fig.add_trace(go.Scatter(),row=i2, col=1)
    
        for var, lev_color in zip(use_list_vars, level_colors):
            if var != 'panel_temp' and var != 'voltage' and var != 'pressure' and var[-2:] != 'RH':
                short_var = var[-4:]   
                row_num = ind_dict[short_var+'_ind']
            elif var == 'voltage' or var == 'pressure' :
                row_num = ind_dict[var+'_ind']
                short_var = 'test'
            elif var == 'panel_temp': 
                row_num = ind_dict['temp_ind']
                short_var = 'Panel Temp'
            elif var[-2:] == 'RH':
                row_num = ind_dict[var[-2:]+'_ind']
                short_var ='RH'
            if short_var == 'temp':
                fig.add_trace(go.Scatter(x=dff.index, y=dff[var].astype(float), mode='markers', name=var,marker=dict(color=copied_df[lev_color+'_colors']),selected_marker_color='grey'),
                                row=row_num, col=1)
                if qc_type == "prev":
                    last_days_dff = last_days_df[use_list_vars]
                    fig.add_trace(go.Scatter(x=last_days_dff.index, y=last_days_dff[var].astype(np.float64), mode='markers', name="prev"+var,marker_color='lightgrey',showlegend=False),
                                    row=row_num, col=1)
                if qc_type == "both":
                    next_few_days_dff = next_few_days_df[use_list_vars]
                    fig.add_trace(go.Scatter(x=next_few_days_dff.index, y=next_few_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="next"+var,marker_color='lightgrey'),
                                row=row_num, col=1)
                    last_days_dff = last_days_df[use_list_vars]
                    fig.add_trace(go.Scatter(x=last_days_dff.index, y=last_days_dff[var].astype(np.float64), mode='markers', name="prev"+var,marker_color='lightgrey',showlegend=False),
                                    row=row_num, col=1)
                if qc_type == "next":
                    next_few_days_dff = next_few_days_df[use_list_vars]
                    fig.add_trace(go.Scatter(x=next_few_days_dff.index, y=next_few_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="prev"+var,marker_color='lightgrey'),
                                row=row_num, col=1)            
            if var == 'panel_temp':
                marker=True
                fig.add_trace(go.Scatter(x=dff.index, y=csv_df['panel_temp'].astype(float), mode='markers', name='Panel Temp', marker_color='darkseagreen'),
                                    row=ind_dict['temp_ind'], col=1)
                if qc_type == "prev":
                    fig.add_trace(go.Scatter(x=last_days_df.index, y=last_days_df['panel_temp'].astype(np.float64),showlegend=False, name="prev"+var,mode='markers', marker_color='lightseagreen'),
                                    row=ind_dict['temp_ind'], col=1)
                if qc_type == "both":
                    fig.add_trace(go.Scatter(x=last_days_df.index, y=last_days_df['panel_temp'].astype(np.float64),showlegend=False, name="next"+var,mode='markers', marker_color='lightseagreen'),
                                    row=ind_dict['temp_ind'], col=1)
                    fig.add_trace(go.Scatter(x=next_few_days_df.index, y=next_few_days_df['panel_temp'].astype(np.float64),showlegend=False, mode='markers', name="next"+var,marker_color='lightseagreen'),
                            row=ind_dict['temp_ind'], col=1)
                if qc_type == "next":
                    fig.add_trace(go.Scatter(x=next_few_days_df.index, y=next_few_days_df['panel_temp'].astype(np.float64),showlegend=False, mode='markers', name="prev"+var,marker_color='lightseagreen'),
                            row=ind_dict['temp_ind'], col=1)
            
            if short_var != 'temp' and var != 'panel_temp' and var != '1m RH' and var != '1m wdir' and var != '2m RH' and var != '2m wdir' and var != '4m RH' and var != '15m RH' and marker == True:
                fig.add_trace(go.Scatter(x=dff.index, y=dff[var].astype(float), mode='markers', name=str(var),marker=dict(color=copied_df[lev_color+'_colors']),selected_marker_color='grey'),
                                row=row_num, col=1)
                if qc_type == "both" or qc_type == 'prev':
                    next_few_days_dff = next_few_days_df[use_list_vars]
                    last_days_dff = last_days_df[use_list_vars]
                    fig.add_trace(go.Scatter(x=next_few_days_dff.index, y=next_few_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="next"+var,marker_color='lightgrey'),
                                row=row_num, col=1)
                    fig.add_trace(go.Scatter(x=last_days_dff.index, y=last_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="prev"+var ,marker_color='lightgrey'),
                                row=row_num, col=1)  
                if qc_type == "next":
                    next_few_days_dff = next_few_days_df[use_list_vars]
                    fig.add_trace(go.Scatter(x=next_few_days_dff.index, y=next_few_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="next"+var,marker_color='lightgrey'),
                                row=row_num, col=1)    
                if qc_type == 'prev':
                    last_days_dff = last_days_df[use_list_vars]
                    fig.add_trace(go.Scatter(x=last_days_dff.index, y=last_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="prev"+var ,marker_color='lightgrey'),
                                row=row_num, col=1)  
      
    
            if short_var != 'temp' and var != 'panel_temp' and var != '1m RH' and var != '1m wdir' and var != '2m RH' and var != '4m RH' and var != '15m RH' and var != '2m wdir' and marker == False:
                fig.add_trace(go.Scatter(x=dff.index, y=dff[var].astype(float), mode='markers', name=str(var),marker=dict(color=copied_df[lev_color+'_colors']),selected_marker_color='grey'),
                                row=row_num, col=1)
                if qc_type == "next" :
                    next_few_days_dff = next_few_days_df[use_list_vars]
                    fig.add_trace(go.Scatter(x=next_few_days_dff.index, y=next_few_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="next"+var,marker_color='grey'),
                                row=row_num, col=1)
                              
                if qc_type == "both" or qc_type == 'prev':
                    next_few_days_dff = next_few_days_df[use_list_vars]
                    last_days_dff = last_days_df[use_list_vars]
                    fig.add_trace(go.Scatter(x=next_few_days_dff.index, y=next_few_days_dff[var].astype(float), mode='markers',showlegend=False, name="next"+var,marker_color='lightgrey'),
                                row=row_num, col=1)
                    fig.add_trace(go.Scatter(x=last_days_dff.index, y=last_days_dff[var].astype(float), mode='markers',showlegend=False, name="prev"+var ,marker_color='lightgrey'),
                                row=row_num, col=1)  
                    
                if qc_type == 'prev':
                    last_days_dff = last_days_df[use_list_vars]
                    fig.add_trace(go.Scatter(x=last_days_dff.index, y=last_days_dff[var].astype(float), mode='markers',showlegend=False, name="prev"+var ,marker_color='lightgrey'),
                                row=row_num, col=1)  
      
        fig.update_traces(mode="markers", hovertemplate=None)
        fig.update_layout(hovermode="x")
        fig.update_layout(clickmode='event+select',dragmode='pan')
        fig.update_traces(marker=dict(size=int(markersize)))
        fig.update_layout(autosize=True,height=700,margin=dict(l=20, r=20, t=50, b=50))
        
        for i3, x in enumerate(fig.data):
            varname = x['name']
            if varname != 'panel_temp' and varname != 'voltage' and varname != 'pressure' and varname != '7m RH' and varname != '30m RH' and varname != None:
                varname1 = varname[-4:]   
            if varname == 'pressure' and varname in dff.columns:
                varname1 = varname[0:4]
            if varname == '7m RH' or varname == '30m RH' and varname in dff.columns:
                varname1 = varname[-2:]
            if varname in dff.columns and varname != 'voltage' and varname != 'panel_temp' and varname != 'pressure':
                fig.update_yaxes(range=(bounds_dict['min'+varname1], bounds_dict['max'+varname1]), row=ind_dict[varname1+'_ind'], col=1) 
            if varname == 'pressure':
                fig.update_yaxes(range=(bounds_dict['min'+varname1], bounds_dict['max'+varname1]), row=ind_dict[varname+'_ind'], col=1) 
        if isinstance(day_range, int):
            if isinstance(center_day, int) == True:
                half_day_range = day_range/2
                input_center_date = pd.to_datetime(str(year)+'/'+str(month)+'/'+str(center_day), format='%Y/%m/%d')
                prev_date_range = input_center_date - timedelta(days=half_day_range)
                next_date_range = input_center_date + timedelta(days=half_day_range)
                fig.update_xaxes(range=(prev_date_range, next_date_range))
    
            else:
                input_center_date = pd.to_datetime(str(year)+'/'+str(month)+'/01', format='%Y/%m/%d')
                prev_date_range = input_center_date
                next_date_range = input_center_date + timedelta(days=day_range)
                
                fig.update_xaxes(range=(prev_date_range, next_date_range))
        if rules == 'No':
            for i3, x in enumerate(fig['data']):
                varname = fig['data'][i3]['name']
                if varname[0:4] != 'prev' and varname[0:4] != 'next':
                    fig['data'][i3]['marker']['color'] = solid_color_df[varname+'_colors'].values
        if rules == 'Yes':        
            for i3, x in enumerate(fig['data']):
                varname = fig['data'][i3]['name']
                if varname[0:4] != 'prev' and varname[0:4] != 'next':
                    fig['data'][i3]['marker']['color'] = copied_df[varname+'_colors'].values   
    
        return(fig)
    """
    @callback(Output('display-met-data-subplots','figure',allow_duplicate=True),
                  Input('rules-toggle','value'),
                  State('display-met-data-subplots','figure'), prevent_initial_call=True) 
    
    def update_rule_markers(rules,fig):
       
        return(fig) 
    """
    @callback(Output('display-hover-data1', 'value'),
              Output('display-hover-data2', 'value'),
              Output('display-hover-data4', 'value'),
              Output('display-hover-data7', 'value'),
              Output('display-hover-data15', 'value'),
              Output('display-hover-data30', 'value'),
              Input('display-met-data-subplots', 'hoverData'),
              [State('display-met-data-subplots', 'figure')],prevent_initial_call=True)
    
    def display_hover_data(hoverData, figure):
        datetime = pd.to_datetime(hoverData['points'][0]['x'])
        #datetime = hoverData['points'][0]['x'] 
        hover_values = cat_copy_df.loc[datetime]  
        hover_date = str(datetime)[:10]
        hover_time =str(datetime)[12:]
    
        hover_temp1 =hover_values['1m temp']
        hover_temp2 =hover_values['2m temp']
        hover_temp4 =hover_values['4m temp']
        hover_temp7 =hover_values['7m temp']
        hover_temp15 =hover_values['15m temp']
        hover_temp30 =hover_values['30m temp']
        hover_pres =hover_values['pressure']
        hover_rh7 =hover_values['7m RH']
        hover_rh30 =hover_values['30m RH']
        hover_wspd1 =hover_values['1m wspd']
        hover_wspd2 =hover_values['2m wspd']
        hover_wspd4 =hover_values['4m wspd']
        hover_wspd7 =hover_values['7m wspd']
        hover_wspd15 =hover_values['15m wspd']
        hover_wspd30 =hover_values['30m wspd']
        hover_wdir4 =hover_values['4m wdir']
        hover_wdir7 =hover_values['7m wdir']
        hover_wdir15 =hover_values['15m wdir']
        hover_wdir30 =hover_values['30m wdir']
        
        ob_num = len(copied_df.loc[:datetime]) -1
        info_str1 = 'Date: '+str(hover_date)[:10]+'\nTime: '+str(hover_time)+'\nTemperature: '+str(hover_temp1)+'\nPressure: '+str(hover_pres)+'\nWind Speed: '+str(hover_wspd1)+'\nObs ID: '+str(ob_num)     
        info_str2 = 'Date: '+str(hover_date)[:10]+'\nTime: '+str(hover_time)+'\nTemperature: '+str(hover_temp2)+'\nPressure: '+str(hover_pres)+'\nWind Speed: '+str(hover_wspd2)+'\nObs ID: '+str(ob_num)     
        info_str4 = 'Date: '+str(hover_date)[:10]+'\nTime: '+str(hover_time)+'\nTemperature: '+str(hover_temp4)+'\nPressure: '+str(hover_pres)+'\nWind Speed: '+str(hover_wspd4)+'\nWind Direction: '+str(hover_wdir4)+'\nObs ID: '+str(ob_num)
        info_str7 = 'Date: '+str(hover_date)[:10]+'\nTime: '+str(hover_time)+'\nTemperature: '+str(hover_temp7)+'\nPressure: '+str(hover_pres)+'\nWind Speed: '+str(hover_wspd7)+'\nWind Direction: '+str(hover_wdir7)+'\nRelative Humidity: '+str(hover_rh7)+'\nObs ID: '+str(ob_num)     
        info_str15 = 'Date: '+str(hover_date)[:10]+'\nTime: '+str(hover_time)+'\nTemperature: '+str(hover_temp15)+'\nPressure: '+str(hover_pres)+'\nWind Speed: '+str(hover_wspd15)+'\nWind Direction: '+str(hover_wdir15)+'\nObs ID: '+str(ob_num)     
        info_str30 = 'Date: '+str(hover_date)[:10]+'\nTime: '+str(hover_time)+'\nTemperature: '+str(hover_temp30)+'\nPressure: '+str(hover_pres)+'\nWind Speed: '+str(hover_wspd30)+'\nWind Direction: '+str(hover_wdir30)+'\nRelative Humidity: '+str(hover_rh30)+'\nObs ID: '+str(ob_num)     
    
        return(info_str1, info_str2, info_str4, info_str7, info_str15, info_str30)

    @callback([Output('display-click-data', 'value'), 
              Output('updated-data', 'data'),
              Output('change-log', 'data'),
              Output('display-met-data-subplots','figure',allow_duplicate=True)],
              [Input('display-met-data-subplots','clickData'),
              Input('display-met-data-subplots', 'selectedData'),
              Input('undo-button', 'n_clicks'),
              Input('reset-button', 'n_clicks')],
              [State('display-met-data-subplots', 'figure'),
               State('rules-toggle','value')],prevent_initial_call='initial_duplicate')

    def display_clickdata(clickData1, selectData1, undo_clicks,reset_clicks,figure,rules):
        global copied_df, change_log, solid_color_df  # Ensure global reference
        ind_dict = {}
        ctx = dash.callback_context
        if ctx.triggered_id == 'undo-button' and change_log:
            for i in range(len(figure['data'])):
                ind_dict[figure['data'][i]['name']] = i
            last_change = change_log.pop()  # Revert the last change
            date = pd.to_datetime(last_change['date'])
            column = last_change['column']
            original_value = last_change['original']
            copied_df.at[date, column] = original_value
            color_pre_change_value = df.at[date,column+'_colors']
            copied_df.at[date, column+'_colors'] = color_pre_change_value
            solid_pre_change_value = copied_solid_color_df.at[date,column+'_colors']
            solid_color_df.at[date, column+'_colors'] = solid_pre_change_value
            if column in ind_dict.keys() and rules == 'Yes':
                figure['data'][ind_dict[column]]['marker']['color'] = copied_df[column+'_colors'].values
            if column in ind_dict.keys() and rules == 'No':
                figure['data'][ind_dict[column]]['marker']['color'] = solid_color_df[column+'_colors'].values
            
            return (f"Undo: {date} - {column} reverted to {original_value}", copied_df.to_dict('records'), change_log,figure)
        
        if ctx.triggered_id == 'reset-button':
            copied_df = qc_df.copy()  # Reset to original
            change_log = []  # Clear the change log
            for i in range(len(figure['data'])):
                ind_dict[figure['data'][i]['name']] = i
            solid_color_df = copied_solid_color_df.copy()
            for column in ind_dict.keys():
                if column[0:4] != 'next' and column [0:4] != 'prev' and rules == 'Yes':
                    figure['data'][ind_dict[column]]['marker']['color'] = copied_df[column+'_colors']
                if column[0:4] != 'next' and column [0:4] != 'prev' and rules == 'No':
                    figure['data'][ind_dict[column]]['marker']['color'] = solid_color_df[column+'_colors']
            return("Data reset", copied_df.to_dict('records'), change_log,figure)

        # Use a set to track all selected points (date, column)
        selected_points = set()
        if selectData1 is None and clickData1 is None:
            raise PreventUpdate
        
        elif selectData1 is not None:
            for i in range(len(figure['data'])):
                ind_dict[figure['data'][i]['name']] = i
            box_points = {}
            new_box_points = [[pt['x'], figure['data'][pt['curveNumber']]['name']] for pt in selectData1.get('points', []) ]
            #  Update box_points with the current selection
            box_points = new_box_points
            for sel_data in new_box_points:
                date=pd.to_datetime(sel_data[0])
                column=sel_data[1]
                point = (date, column)
                #original_value = copied_df.at[date, column]
                original_value = np.float64(copied_df.at[date, column])
                new_value = np.float64(444.0)
                if point not in selected_points:
                    # Add new selection
                    selected_points.add(point)
                    
                    if original_value != new_value and np.isnan(original_value)==False: #elif original_value != new_value and original_value != np.nan:
                        copied_df.at[date, column] = new_value
                        copied_df.at[date, column+'_colors'] = 'grey'
                        solid_color_df.at[date, column+'_colors'] = 'grey'
                        if rules == 'Yes':
                            figure['data'][ind_dict[column]]['marker']['color'] = copied_df[column+'_colors'].values
                        elif rules == 'No':
                            figure['data'][ind_dict[column]]['marker']['color'] = solid_color_df[column+'_colors'].values
                        change_log.append({
                            "date": date,
                            "column": column,
                            "original": original_value,
                            "new": new_value})
                        if column == '4m wspd':
                            wd_original_value = copied_df.at[date, '4m wdir']
                            copied_df.at[date, '4m wdir'] = new_value
                            copied_df.at[date, '4m wdir_colors'] = 'grey'
                            solid_color_df.at[date,'4m wdir_colors'] = 'grey'
                            if '4m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['4m wdir']]['marker']['color'] = copied_df['4m wdir_colors'].values
                            if '4m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['4m wdir']]['marker']['color'] = solid_color_df['4m wdir_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '4m wdir',
                                "original": wd_original_value,
                                "new": new_value})
                        if column == '4m wdir':
                            ws_original_value = copied_df.at[date, '4m wspd']
                            copied_df.at[date, '4m wspd'] = new_value
                            copied_df.at[date,'4m wspd_colors'] = 'grey'
                            solid_color_df.at[date, '4m wspd_colors'] = 'grey'
                            if '4m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['4m wspd']]['marker']['color'] = copied_df['4m wspd_colors'].values
                            if '4m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['4m wspd']]['marker']['color'] = solid_color_df['4m wspd_colors'].values 
                            change_log.append({
                                "date": date,
                                "column": '4m wspd',
                                "original": ws_original_value,
                                "new": new_value})
                        if column == '7m wspd':
                            wd_original_value = copied_df.at[date, '7m wdir']
                            copied_df.at[date, '7m wdir'] = new_value
                            copied_df.at[date, '7m wdir_colors'] = 'grey'
                            solid_color_df.at[date,'7m wdir_colors'] = 'grey'
                            if '7m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['7m wdir']]['marker']['color'] = copied_df['7m wdir_colors'].values
                            if '7m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['7m wdir']]['marker']['color'] = solid_color_df['7m wdir_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '7m wdir',
                                "original": wd_original_value,
                                "new": new_value})
                        if column == '7m wdir':
                            ws_original_value = copied_df.at[date, '7m wspd']
                            copied_df.at[date, '7m wspd'] = new_value
                            copied_df.at[date,'7m wspd_colors'] = 'grey'
                            solid_color_df.at[date, '7m wspd_colors'] = 'grey'
                            if '7m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['7m wspd']]['marker']['color'] = copied_df['7m wspd_colors'].values
                            if '7m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['7m wspd']]['marker']['color'] = solid_color_df['7m wspd_colors'].values 
                            change_log.append({
                                "date": date,
                                "column": '7m wspd',
                                "original": ws_original_value,
                                "new": new_value})
                        if column == '15m wspd':
                            wd_original_value = copied_df.at[date, '15m wdir']
                            copied_df.at[date, '15m wdir'] = new_value
                            copied_df.at[date, '15m wdir_colors'] = 'grey'
                            solid_color_df.at[date,'15m wdir_colors'] = 'grey'
                            if '15m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['15m wdir']]['marker']['color'] = copied_df['15m wdir_colors'].values
                            if '15m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['15m wdir']]['marker']['color'] = solid_color_df['15m wdir_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '15m wdir',
                                "original": wd_original_value,
                                "new": new_value})
                        if column == '15m wdir':
                            ws_original_value = copied_df.at[date, '15m wspd']
                            copied_df.at[date, '15m wspd'] = new_value
                            copied_df.at[date,'15m wspd_colors'] = 'grey'
                            solid_color_df.at[date, '15m wspd_colors'] = 'grey'
                            if '15m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['15m wspd']]['marker']['color'] = copied_df['15m wspd_colors'].values
                            if '15m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['15m wspd']]['marker']['color'] = solid_color_df['15m wspd_colors'].values 
                            change_log.append({
                                "date": date,
                                "column": '15m wspd',
                                "original": ws_original_value,
                                "new": new_value})
                        if column == '30m wspd':
                            wd_original_value = copied_df.at[date, '30m wdir']
                            copied_df.at[date, '30m wdir'] = new_value
                            copied_df.at[date, '30m wdir_colors'] = 'grey'
                            solid_color_df.at[date,'30m wdir_colors'] = 'grey'
                            if '30m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['30m wdir']]['marker']['color'] = copied_df['30m wdir_colors'].values
                            if '30m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['30m wdir']]['marker']['color'] = solid_color_df['30m wdir_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '30m wdir',
                                "original": wd_original_value,
                                "new": new_value})
                        if column == '30m wdir':
                            ws_original_value = copied_df.at[date, '30m wspd']
                            copied_df.at[date, '30m wspd'] = new_value
                            copied_df.at[date,'30m wspd_colors'] = 'grey'
                            solid_color_df.at[date, '30m wspd_colors'] = 'grey'
                            if '30m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['30m wspd']]['marker']['color'] = copied_df['30m wspd_colors'].values
                            if '30m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['30m wspd']]['marker']['color'] = solid_color_df['30m wspd_colors'].values 
                            change_log.append({
                                "date": date,
                                "column": '30m wspd',
                                "original": ws_original_value,
                                "new": new_value})
                    
                    if np.isnan(original_value) == True: #elif original_value != new_value and original_value != np.nan:
                        noqc_original_value = noqc_df.at[date, column]
                        copied_df.at[date, column] = noqc_original_value
                        color_pre_change_value = df.at[date, column+'_noerrorcolor']
                        copied_df.at[date, column+'_colors'] = color_pre_change_value
                        solid_color_df.at[date, column+'_colors'] = df.at[date, column+'_noerrorcolor']
                        if rules == 'Yes':
                            figure['data'][ind_dict[column]]['marker']['color'] = copied_df[column+'_colors'].values
                        elif rules == 'No':
                            figure['data'][ind_dict[column]]['marker']['color'] = solid_color_df[column+'_colors'].values
                        
                        change_log.append({
                            "date": date,
                            "column": column,
                            "original": original_value,
                            "new": noqc_original_value})
                        if column == '4m wspd':
                            wd_original_value = copied_df.at[date, '4m wdir']
                            wd_noqc_original_value =  noqc_df.at[date, '4m wdir']
                            copied_df.at[date, '4m wdir'] = wd_noqc_original_value
                            copied_df.at[date, '4m wdir_colors'] = df.at[date, '4m wdir_noerrorcolor']
                            solid_color_df.at[date, '4m wdir_colors'] = df.at[date, '4m wdir_noerrorcolor']
                            if '4m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['4m wdir']]['marker']['color'] = copied_df['4m wdir_colors'].values
                            if '4m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['4m wdir']]['marker']['color'] = solid_color_df['4m wdir_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '4m wdir',
                                "original": wd_original_value,
                                "new": wd_noqc_original_value})
                        if column == '4m wdir':
                            ws_original_value = copied_df.at[date, '4m wspd']
                            ws_noqc_original_value =  noqc_df.at[date, '4m wspd']
                            copied_df.at[date, '4m wspd'] = ws_noqc_original_value
                            copied_df.at[date, '4m wspd_colors'] = df.at[date, '4m wspd_noerrorcolor']
                            solid_color_df.at[date, '4m wspd_colors'] = df.at[date, '4m wspd_noerrorcolor']
                            if '4m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['4m wspd']]['marker']['color'] = copied_df['4m wspd_colors'].values
                            if '4m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['4m wspd']]['marker']['color'] = solid_color_df['4m wspd_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '4m wspd',
                                "original": ws_original_value,
                                "new": ws_noqc_original_value})
                        if column == '7m wspd':
                            wd_original_value = copied_df.at[date, '7m wdir']
                            wd_noqc_original_value =  noqc_df.at[date, '7m wdir']
                            copied_df.at[date, '7m wdir'] = wd_noqc_original_value
                            copied_df.at[date, '7m wdir_colors'] = df.at[date, '7m wdir_noerrorcolor']
                            solid_color_df.at[date, '7m wdir_colors'] = df.at[date, '7m wdir_noerrorcolor']
                            if '7m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['7m wdir']]['marker']['color'] = copied_df['7m wdir_colors'].values
                            if '7m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['7m wdir']]['marker']['color'] = solid_color_df['7m wdir_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '7m wdir',
                                "original": wd_original_value,
                                "new": wd_noqc_original_value})
                        if column == '7m wdir':
                            ws_original_value = copied_df.at[date, '7m wspd']
                            ws_noqc_original_value =  noqc_df.at[date, '7m wspd']
                            copied_df.at[date, '7m wspd'] = ws_noqc_original_value
                            copied_df.at[date, '7m wspd_colors'] = df.at[date, '7m wspd_noerrorcolor']
                            solid_color_df.at[date, '7m wspd_colors'] = df.at[date, '7m wspd_noerrorcolor']
                            if '7m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['7m wspd']]['marker']['color'] = copied_df['7m wspd_colors'].values
                            if '7m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['7m wspd']]['marker']['color'] = solid_color_df['7m wspd_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '7m wspd',
                                "original": ws_original_value,
                                "new": ws_noqc_original_value})
                        if column == '15m wspd':
                            wd_original_value = copied_df.at[date, '15m wdir']
                            wd_noqc_original_value =  noqc_df.at[date, '15m wdir']
                            copied_df.at[date, '15m wdir'] = wd_noqc_original_value
                            copied_df.at[date, '15m wdir_colors'] = df.at[date, '15m wdir_noerrorcolor']
                            solid_color_df.at[date, '15m wdir_colors'] = df.at[date, '15m wdir_noerrorcolor']
                            if '15m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['15m wdir']]['marker']['color'] = copied_df['15m wdir_colors'].values
                            if '15m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['15m wdir']]['marker']['color'] = solid_color_df['15m wdir_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '15m wdir',
                                "original": wd_original_value,
                                "new": wd_noqc_original_value})
                        if column == '15m wdir':
                            ws_original_value = copied_df.at[date, '15m wspd']
                            ws_noqc_original_value =  noqc_df.at[date, '15m wspd']
                            copied_df.at[date, '15m wspd'] = ws_noqc_original_value
                            copied_df.at[date, '15m wspd_colors'] = df.at[date, '15m wspd_noerrorcolor']
                            solid_color_df.at[date, '15m wspd_colors'] = df.at[date, '15m wspd_noerrorcolor']
                            if '15m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['15m wspd']]['marker']['color'] = copied_df['15m wspd_colors'].values
                            if '15m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['15m wspd']]['marker']['color'] = solid_color_df['15m wspd_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '15m wspd',
                                "original": ws_original_value,
                                "new": ws_noqc_original_value})
                        if column == '30m wspd':
                            wd_original_value = copied_df.at[date, '30m wdir']
                            wd_noqc_original_value =  noqc_df.at[date, '30m wdir']
                            copied_df.at[date, '30m wdir'] = wd_noqc_original_value
                            copied_df.at[date, '30m wdir_colors'] = df.at[date, '30m wdir_noerrorcolor']
                            solid_color_df.at[date, '30m wdir_colors'] = df.at[date, '30m wdir_noerrorcolor']
                            if '30m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['30m wdir']]['marker']['color'] = copied_df['30m wdir_colors'].values
                            if '30m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['30m wdir']]['marker']['color'] = solid_color_df['30m wdir_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '30m wdir',
                                "original": wd_original_value,
                                "new": wd_noqc_original_value})
                        if column == '30m wdir':
                            ws_original_value = copied_df.at[date, '30m wspd']
                            ws_noqc_original_value =  noqc_df.at[date, '30m wspd']
                            copied_df.at[date, '30m wspd'] = ws_noqc_original_value
                            copied_df.at[date, '30m wspd_colors'] = df.at[date, '30m wspd_noerrorcolor']
                            solid_color_df.at[date, '30m wspd_colors'] = df.at[date, '30m wspd_noerrorcolor']
                            if '30m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['30m wspd']]['marker']['color'] = copied_df['30m wspd_colors'].values
                            if '30m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['30m wspd']]['marker']['color'] = solid_color_df['30m wspd_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '30m wspd',
                                "original": ws_original_value,
                                "new": ws_noqc_original_value})
                    
                    if original_value == new_value:
                        selected_points.discard(point)

                        noqc_original_value = noqc_df.at[date, column]
                        copied_df.at[date, column] = noqc_original_value
                        copied_df.at[date, column+'_colors'] = df.at[date, column+'_colors']
                        solid_pre_change_value = copied_solid_color_df.at[date,column+'_colors']
                        solid_color_df.at[date,column+'_colors'] = solid_pre_change_value
                        if rules == 'Yes':
                            figure['data'][ind_dict[column]]['marker']['color'] = copied_df[column+'_colors'].values
                        elif rules == 'No':
                            figure['data'][ind_dict[column]]['marker']['color'] = solid_color_df[column+'_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']== column:
                                del change_log[i]
                        if column == '4m wspd' :
                            wd_original_value = copied_df.at[date, '4m wdir']
                            noqc_original_value =  noqc_df.at[date, '4m wdir']
                            copied_df.at[date, '4m wdir'] = noqc_original_value
                            copied_df.at[date,'4m wdir_colors'] = df.at[date, '4m wdir_colors']
                            wd_solid_pre_change_value = copied_solid_color_df.at[date,'4m wdir_colors']
                            solid_color_df.at[date,'4m wdir_colors'] = wd_solid_pre_change_value
                            if '4m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['4m wdir']]['marker']['color'] = copied_df['4m wdir_colors'].values
                            if '4m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['4m wdir']]['marker']['color'] = solid_color_df['4m wdir_colors'].values
                            for i,test in enumerate(change_log):
                                if change_log[i]['date'] == date and change_log[i]['column']== '4m wdir':
                                    del change_log[i]
                        if column == '4m wdir':
                            ws_original_value = copied_df.at[date, '4m wspd']
                            noqc_original_value =  noqc_df.at[date, '4m wspd']
                            copied_df.at[date, '4m wspd'] = noqc_original_value
                            copied_df.at[date,'4m wspd_colors'] = df.at[date, '4m wspd_colors']
                            ws_solid_pre_change_value = copied_solid_color_df.at[date,'4m wspd_colors']
                            solid_color_df.at[date,'4m wspd_colors'] = ws_solid_pre_change_value
                            if '4m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['4m wspd']]['marker']['color'] = copied_df['4m wspd_colors'].values
                            if '4m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['4m wspd']]['marker']['color'] = solid_color_df['4m wspd_colors'].values
                            for i,test in enumerate(change_log):
                                if change_log[i]['date'] == date and change_log[i]['column']== '4m wspd':
                                    del change_log[i]
                        if column == '7m wspd':
                            wd_original_value = copied_df.at[date, '7m wdir']
                            noqc_original_value =  noqc_df.at[date, '7m wdir']
                            copied_df.at[date, '7m wdir'] = noqc_original_value
                            copied_df.at[date,'7m wdir_colors'] = df.at[date, '7m wdir_colors']
                            wd_solid_pre_change_value = copied_solid_color_df.at[date,'7m wdir_colors']
                            solid_color_df.at[date,'7m wdir_colors'] = wd_solid_pre_change_value
                            if '7m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['7m wdir']]['marker']['color'] = copied_df['7m wdir_colors'].values
                            if '7m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['7m wdir']]['marker']['color'] = solid_color_df['7m wdir_colors'].values
                            for i,test in enumerate(change_log):
                                if change_log[i]['date'] == date and change_log[i]['column']== '7m wdir':
                                    del change_log[i]
                        if column == '7m wdir':
                            ws_original_value = copied_df.at[date, '7m wspd']
                            noqc_original_value =  noqc_df.at[date, '7m wspd']
                            copied_df.at[date, '7m wspd'] = noqc_original_value
                            copied_df.at[date,'7m wspd_colors'] = df.at[date, '7m wspd_colors']
                            ws_solid_pre_change_value = copied_solid_color_df.at[date,'7m wspd_colors']
                            solid_color_df.at[date,'7m wspd_colors'] = ws_solid_pre_change_value
                            if '7m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['7m wspd']]['marker']['color'] = copied_df['7m wspd_colors'].values
                            if '7m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['7m wspd']]['marker']['color'] = solid_color_df['7m wspd_colors'].values
                            for i,test in enumerate(change_log):
                                if change_log[i]['date'] == date and change_log[i]['column']== '7m wspd':
                                    del change_log[i]
                        if column == '15m wspd':
                            wd_original_value = copied_df.at[date, '15m wdir']
                            noqc_original_value =  noqc_df.at[date, '15m wdir']
                            copied_df.at[date, '15m wdir'] = noqc_original_value
                            copied_df.at[date,'15m wdir_colors'] = df.at[date, '15m wdir_colors']
                            wd_solid_pre_change_value = copied_solid_color_df.at[date,'15m wdir_colors']
                            solid_color_df.at[date,'15m wdir_colors'] = wd_solid_pre_change_value
                            if '15m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['15m wdir']]['marker']['color'] = copied_df['15m wdir_colors'].values
                            if '15m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['15m wdir']]['marker']['color'] = solid_color_df['15m wdir_colors'].values
                            for i,test in enumerate(change_log):
                                if change_log[i]['date'] == date and change_log[i]['column']== '15m wdir':
                                    del change_log[i]
                        if column == '15m wdir':
                            ws_original_value = copied_df.at[date, '15m wspd']
                            noqc_original_value =  noqc_df.at[date, '15m wspd']
                            copied_df.at[date, '15m wspd'] = noqc_original_value
                            copied_df.at[date,'15m wspd_colors'] = df.at[date, '15m wspd_colors']
                            ws_solid_pre_change_value = copied_solid_color_df.at[date,'15m wspd_colors']
                            solid_color_df.at[date,'15m wspd_colors'] = ws_solid_pre_change_value
                            if '15m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['15m wspd']]['marker']['color'] = copied_df['15m wspd_colors'].values
                            if '15m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['15m wspd']]['marker']['color'] = solid_color_df['15m wspd_colors'].values
                            for i,test in enumerate(change_log):
                                if change_log[i]['date'] == date and change_log[i]['column']== '15m wspd':
                                    del change_log[i]
                        if column == '30m wspd':
                            wd_original_value = copied_df.at[date, '30m wdir']
                            noqc_original_value =  noqc_df.at[date, '30m wdir']
                            copied_df.at[date, '30m wdir'] = noqc_original_value
                            copied_df.at[date,'30m wdir_colors'] = df.at[date, '30m wdir_colors']
                            wd_solid_pre_change_value = copied_solid_color_df.at[date,'30m wdir_colors']
                            solid_color_df.at[date,'30m wdir_colors'] = wd_solid_pre_change_value
                            if '30m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['30m wdir']]['marker']['color'] = copied_df['30m wdir_colors'].values
                            if '30m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['30m wdir']]['marker']['color'] = solid_color_df['30m wdir_colors'].values
                            for i,test in enumerate(change_log):
                                if change_log[i]['date'] == date and change_log[i]['column']== '30m wdir':
                                    del change_log[i]
                        if column == '30m wdir':
                            ws_original_value = copied_df.at[date, '30m wspd']
                            noqc_original_value =  noqc_df.at[date, '30m wspd']
                            copied_df.at[date, '30m wspd'] = noqc_original_value
                            copied_df.at[date,'30m wspd_colors'] = df.at[date, '30m wspd_colors']
                            ws_solid_pre_change_value = copied_solid_color_df.at[date,'30m wspd_colors']
                            solid_color_df.at[date,'30m wspd_colors'] = ws_solid_pre_change_value
                            if '30m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['30m wspd']]['marker']['color'] = copied_df['30m wspd_colors'].values
                            if '30m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['30m wspd']]['marker']['color'] = solid_color_df['30m wspd_colors'].values
                            for i,test in enumerate(change_log):
                                if change_log[i]['date'] == date and change_log[i]['column']== '30m wspd':
                                    del change_log[i]
                    
                elif point in selected_points:
                    selected_points.discard(point)
                    pre_change_value = qc_df.at[date, column]
                    copied_df.at[date, column] = pre_change_value
                    color_pre_change_value = df.at[date,column+'_colors']
                    copied_df.at[date,column+'_colors'] = color_pre_change_value
                    solid_pre_change_value = copied_solid_color_df.at[date,column+'_colors']
                    solid_color_df.at[date,column+'_colors'] = solid_pre_change_value
                    if rules == 'Yes':
                        figure['data'][ind_dict[column]]['marker']['color'] = copied_df[column+'_colors'].values
                    elif rules == 'No':
                        figure['data'][ind_dict[column]]['marker']['color'] = solid_color_df[column+'_colors'].values
                    for i,test in enumerate(change_log):
                        if change_log[i]['date'] == date and change_log[i]['column']== column:
                            del change_log[i]

                    if column == '4m wspd':
                        selected_points.discard(date, '4m wdir')
                        wd_pre_change_value = qc_df.at[date, '4m wdir']
                        copied_df.at[date, '4m wdir'] = wd_pre_change_value
                        wd_color_pre_change_value = df.at[date,'4m wdir_colors']
                        copied_df.at[date,'4m wdir_colors'] = wd_color_pre_change_value
                        solid_pre_change_value = copied_solid_color_df.at[date,'4m wdir_colors']
                        solid_color_df.at[date,'4m wdir_colors'] = solid_pre_change_value
                        if rules == 'No' and '4m wdir' in ind_dict.keys():
                            figure['data'][ind_dict['4m wdir']]['marker']['color'] = solid_color_df['4m wdir_colors'].values
                        if '4m wdir' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['4m wdir']]['marker']['color'] = copied_df['4m wdir_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']=='4m wdir':
                                del change_log[i]
                    if column == '4m wdir':
                        selected_points.discard((date, '4m wspd'))
                        ws_pre_change_value = qc_df.at[date, '4m wspd']
                        copied_df.at[date, '4m wspd'] = ws_pre_change_value
                        ws_color_pre_change_value = df.at[date,'4m wspd_colors']
                        copied_df.at[date,'4m wspd_colors'] = ws_color_pre_change_value
                        solid_pre_change_value = copied_solid_color_df.at[date,'4m wspd_colors']
                        solid_color_df.at[date,'4m wspd_colors'] = solid_pre_change_value
                        
                        if '4m wspd' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['4m wspd']]['marker']['color'] = copied_df['4m wspd_colors'].values
                        if rules == 'No' and '4m wspd' in ind_dict.keys():
                            figure['data'][ind_dict['4m wspd']]['marker']['color'] = solid_color_df['4m wspd_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']== '4m wspd':
                                del change_log[i]
                    if column == '7m wspd':
                        selected_points.discard((date, '7m wdir'))
                        wd_pre_change_value = qc_df.at[date, '7m wdir']
                        copied_df.at[date, '7m wdir'] = wd_pre_change_value
                        wd_color_pre_change_value = df.at[date,'7m wdir_colors']
                        copied_df.at[date,'7m wdir_colors'] = wd_color_pre_change_value
                        solid_pre_change_value = copied_solid_color_df.at[date,'7m wdir_colors']
                        solid_color_df.at[date,'7m wdir_colors'] = solid_pre_change_value
                        if '7m wdir' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['7m wdir']]['marker']['color'] = copied_df['7m wdir_colors'].values
                        if rules == 'No' and '7m wdir' in ind_dict.keys():
                            figure['data'][ind_dict['7m wdir']]['marker']['color'] = solid_color_df['7m wdir_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']=='7m wdir':
                                del change_log[i]
                    if column == '7m wdir':
                        selected_points.discard(date, '7m wspd')
                        ws_pre_change_value = qc_df.at[date, '7m wspd']
                        copied_df.at[date, '7m wspd'] = ws_pre_change_value
                        ws_color_pre_change_value = df.at[date,'7m wspd_colors']
                        copied_df.at[date,'7m wspd_colors'] = ws_color_pre_change_value
                        solid_pre_change_value = copied_solid_color_df.at[date,'7m wspd_colors']
                        solid_color_df.at[date,'7m wspd_colors'] = solid_pre_change_value
                        if '7m wspd' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['7m wspd']]['marker']['color'] = copied_df['7m wspd_colors'].values
                        if rules == 'No' and '7m wspd' in ind_dict.keys():
                            figure['data'][ind_dict['7m wspd']]['marker']['color'] = solid_color_df['7m wspd_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']== '7m wspd':
                                del change_log[i]
                    if column == '15m wspd':
                        selected_points.discard(date, '15m wdir')
                        wd_pre_change_value = qc_df.at[date, '15m wdir']
                        copied_df.at[date, '15m wdir'] = wd_pre_change_value
                        wd_color_pre_change_value = df.at[date,'15m wdir_colors']
                        copied_df.at[date,'15m wdir_colors'] = wd_color_pre_change_value
                        solid_pre_change_value = copied_solid_color_df.at[date,'15m wdir_colors']
                        solid_color_df.at[date,'15m wdir_colors'] = solid_pre_change_value
                        if '15m wdir' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['15m wdir']]['marker']['color'] = copied_df['15m wdir_colors'].values
                        if rules == 'No' and '15m wdir' in ind_dict.keys():
                            figure['data'][ind_dict['15m wdir']]['marker']['color'] = solid_color_df['15m wdir_colors'].values    
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']=='15m wdir':
                                del change_log[i]
                    if column == '15m wdir':
                        selected_points.discard(date, '15m wspd')
                        ws_pre_change_value = qc_df.at[date, '15m wspd']
                        copied_df.at[date, '15m wspd'] = ws_pre_change_value
                        ws_color_pre_change_value = df.at[date,'15m wspd_colors']
                        copied_df.at[date,'15m wspd_colors'] = ws_color_pre_change_value
                        solid_pre_change_value = copied_solid_color_df.at[date,'15m wspd_colors']
                        solid_color_df.at[date,'15m wspd_colors'] = solid_pre_change_value
                        if '15m wspd' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['15m wspd']]['marker']['color'] = copied_df['15m wspd_colors'].values
                        if rules == 'No' and '15m wspd' in ind_dict.keys():
                            figure['data'][ind_dict['15m wspd']]['marker']['color'] = solid_color_df['15m wspd_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']== '15m wspd':
                                del change_log[i]
                    if column == '30m wspd':
                        selected_points.discard(date, '30m wdir')
                        wd_pre_change_value = qc_df.at[date, '30m wdir']
                        copied_df.at[date, '30m wdir'] = wd_pre_change_value
                        wd_color_pre_change_value = df.at[date,'30m wdir_colors']
                        copied_df.at[date,'30m wdir_colors'] = wd_color_pre_change_value
                        solid_pre_change_value = copied_solid_color_df.at[date,'30m wdir_colors']
                        solid_color_df.at[date,'30m wdir_colors'] = solid_pre_change_value
                        if '30m wdir' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['30m wdir']]['marker']['color'] = copied_df['30m wdir_colors'].values
                        if rules == 'No' and '30m wdir' in ind_dict.keys():
                            figure['data'][ind_dict['30m wdir']]['marker']['color'] = solid_color_df['30m wdir_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']=='30m wdir':
                                del change_log[i]
                    if column == '30m wdir':
                        selected_points.discard(date, '30m wspd')
                        ws_pre_change_value = qc_df.at[date, '30m wspd']
                        copied_df.at[date, '30m wspd'] = ws_pre_change_value
                        ws_color_pre_change_value = df.at[date,'30m wspd_colors']
                        copied_df.at[date,'30m wspd_colors'] = ws_color_pre_change_value
                        solid_pre_change_value = copied_solid_color_df.at[date,'30m wspd_colors']
                        solid_color_df.at[date,'30m wspd_colors'] = solid_pre_change_value
                        if '30m wspd' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['30m wspd']]['marker']['color'] = copied_df['30m wspd_colors'].values
                        if rules == 'No' and '30m wspd' in ind_dict.keys():
                            figure['data'][ind_dict['30m wspd']]['marker']['color'] = solid_color_df['30m wspd_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']== '30m wspd':
                                del change_log[i]
    
            return ( f"{len(selected_points)} total selected points. ",copied_df.to_dict('records'),change_log,figure)
            
        #return(f"De-select: {date} - {column} reverted to {pre_change_value}", copied_df.to_dict('records'), change_log,figure)
        return("No click data", copied_df.to_dict('records'), change_log,figure)
    @callback(
        [Output("download-dataframe-csv", "data"),    Output("download-qc-log-csv", "data")],
        Input("save-button", "n_clicks"), allow_duplicate=True,
        prevent_initial_call=True)
    def save_data_csv(n_clicks):
        change_log_df = pd.DataFrame(change_log)  
        aws_abbreviation = closest_date_row['Short_Name'] 
        name = closest_date_row['Name'] 
        
        qc_10min = (copied_df.drop(columns=['date','time']))
        q10_bf = qc_10min.bfill(limit=1)   #look at 1 data points before (10min)
        q10_bfff = q10_bf.ffill(limit=1)   #10min after one data point after if there isnt a data point
    
        q10_bfff2 = q10_bfff.bfill(limit=1)     #look at 2 data points before (40min)
        q10_bfff3 = q10_bfff2.ffill(limit=1)   #20min  after (2 data points)
        
        q10_bfff4 = q10_bfff3.bfill(limit=1)    #look at 3 data points before (40min)
        q10_bfff5 = q10_bfff4.ffill(limit=1)   #30min  after (3 data points)
        
        q10_bfff6 = q10_bfff5.bfill(limit=1)    # look at 4 data points before  (40min)
        q10_bfff7 = q10_bfff6.ffill(limit=1)   #40 min  after  (4 data points)
        qc_3hr =q10_bfff7.asfreq('3h')
        qc_1hr =q10_bfff.asfreq('1h')

        
        qc_10min = qc_10min.fillna(444.0)
        qc_1hr = qc_1hr.fillna(444.0)
        qc_3hr = qc_3hr.fillna(444.0)
        
        change_log_df = pd.DataFrame(change_log)  
    
        lat1 = closest_date_row['Lat'] 
        lon1 = closest_date_row['Lon'] 
        
        elev = (closest_date_row['Elevation']).rjust(4, " ")
        lat2 = str(round(float(lat1[:-1]),2)).ljust(5, '0')
        lon2 = str(round(float(lon1[:-1]),2))
        
        lat3 = lat1[-1]
        lon3 = lon1[-1]
        
        lat = (lat2+lat3).rjust(6, ' ') 
        lon = (lon2+lon3).rjust(7, ' ')  
        
        qc_header = "Year: "+str(year)+"  Month: "+str(month)+"  ID: "+aws_abbreviation+"  ARGOS: "+((str(argos_id_input).rjust(5, ' ')))+"  Name: "+name+"\nLat: "+str(lat)+"  Lon: "+str(lon)+"  Elev: "+str(elev)+"m"           
        
        qc_10min['year'] = qc_10min['year'].astype(int)
        qc_10min['month']= qc_10min['month'].astype(int)
        qc_10min['day']= qc_10min['day'].astype(int)
        qc_10min['jday']= qc_10min['jday'].astype(int)
        
        qc_3hr['year'] = qc_3hr['year'].astype(int)
        qc_3hr['month']= qc_3hr['month'].astype(int)
        qc_3hr['day']= qc_3hr['day'].astype(int)
        qc_3hr['jday']= qc_3hr['jday'].astype(int)
        
        qc_1hr['year'] = qc_1hr['year'].astype(int)
        qc_1hr['month']= qc_1hr['month'].astype(int)
        qc_1hr['day']= qc_1hr['day'].astype(int)
        qc_1hr['jday']= qc_1hr['jday'].astype(int)
        
        time_10min = qc_10min.index.astype(str)
        qc_10min['time']  = [x[-8:-3].replace(':','') for x in time_10min]
        
        time_1hr= qc_1hr.index.astype(str)
        qc_1hr['time']  = [x[-8:-3].replace(':','') for x in time_1hr]
        
        time_3hr= qc_3hr.index.astype(str)
        qc_3hr['time']  = [x[-8:-3].replace(':','') for x in time_3hr]
        
        qc_10min = qc_10min[['year','jday','month','day','time','1m temp','2m temp','4m temp','7m temp','15m temp','30m temp','pressure','1m wspd','2m wspd','4m wspd','7m wspd','15m wspd','30m wspd','4m wdir','7m wdir','15m wdir','30m wdir','7m RH','30m RH']]
        qc_1hr = qc_1hr[['year','jday','month','day','time','1m temp','2m temp','4m temp','7m temp','15m temp','30m temp','pressure','1m wspd','2m wspd','4m wspd','7m wspd','15m wspd','30m wspd','4m wdir','7m wdir','15m wdir','30m wdir','7m RH','30m RH']]
        qc_3hr = qc_3hr[['year','jday','month','day','time','1m temp','2m temp','4m temp','7m temp','15m temp','30m temp','pressure','1m wspd','2m wspd','4m wspd','7m wspd','15m wspd','30m wspd','4m wdir','7m wdir','15m wdir','30m wdir','7m RH','30m RH']]
        
        qc_10min = qc_10min.fillna(444.0)
        qc_1hr = qc_1hr.fillna(444.0)
        qc_3hr = qc_3hr.fillna(444.0)
        
        qc_10min['month'] = [str(x).rjust(2,' ') for x in qc_10min['month']]
        qc_10min['day'] = [str(x).rjust(2,' ') for x in qc_10min['day']]
        qc_10min['jday'] = [str(x).rjust(3,' ') for x in qc_10min['jday']]
        qc_10min['time']= [str(x).rjust(4,' ') for x in qc_10min['time']]
        
        qc_10min['1m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['1m temp']]
        qc_10min['2m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['2m temp']]
        qc_10min['4m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['4m temp']]
        qc_10min['7m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['7m temp']]
        qc_10min['15m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['15m temp']]
        qc_10min['30m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['30m temp']]
        qc_10min['pressure']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['pressure']]
        qc_10min['1m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['1m wspd']]
        qc_10min['2m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['2m wspd']]
        qc_10min['4m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['4m wspd']]
        qc_10min['7m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['7m wspd']]
        qc_10min['15m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['15m wspd']]
        qc_10min['30m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['30m wspd']]
        qc_10min['4m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['4m wdir']]
        qc_10min['7m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['7m wdir']]
        qc_10min['15m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['15m wdir']]
        qc_10min['30m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['30m wdir']]
        qc_10min['7m RH']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['7m RH']]
        qc_10min['30m RH']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['30m RH']]
    
        qc_1hr['month'] = [str(x).rjust(2,' ') for x in qc_1hr['month']]
        qc_1hr['day'] = [str(x).rjust(2,' ') for x in qc_1hr['day']]
        qc_1hr['jday'] = [str(x).rjust(3,' ') for x in qc_1hr['jday']]
        qc_1hr['time']= [str(x).rjust(4,' ') for x in qc_1hr['time']]
        
        qc_1hr['1m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['1m temp']]
        qc_1hr['2m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['2m temp']]
        qc_1hr['4m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['4m temp']]
        qc_1hr['7m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['7m temp']]
        qc_1hr['15m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['15m temp']]
        qc_1hr['30m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['30m temp']]
        qc_1hr['pressure']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['pressure']]
        qc_1hr['1m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['1m wspd']]
        qc_1hr['2m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['2m wspd']]
        qc_1hr['4m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['4m wspd']]
        qc_1hr['7m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['7m wspd']]
        qc_1hr['15m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['15m wspd']]
        qc_1hr['30m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['30m wspd']]
        qc_1hr['4m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['4m wdir']]
        qc_1hr['7m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['7m wdir']]
        qc_1hr['15m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['15m wdir']]
        qc_1hr['30m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['30m wdir']]
        qc_1hr['7m RH']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['7m RH']]
        qc_1hr['30m RH']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['30m RH']]
        
        qc_3hr['month'] = [str(x).rjust(2,' ') for x in qc_3hr['month']]
        qc_3hr['day'] = [str(x).rjust(2,' ') for x in qc_3hr['day']]
        qc_3hr['jday'] = [str(x).rjust(3,' ') for x in qc_3hr['jday']]
        qc_3hr['time']= [str(x).rjust(4,' ') for x in qc_3hr['time']]
        
        qc_3hr['1m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['1m temp']]
        qc_3hr['2m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['2m temp']]
        qc_3hr['4m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['4m temp']]
        qc_3hr['7m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['7m temp']]
        qc_3hr['15m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['15m temp']]
        qc_3hr['30m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['30m temp']]
        qc_3hr['pressure']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['pressure']]
        qc_3hr['1m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['1m wspd']]
        qc_3hr['2m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['2m wspd']]
        qc_3hr['4m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['4m wspd']]
        qc_3hr['7m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['7m wspd']]
        qc_3hr['15m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['15m wspd']]
        qc_3hr['30m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['30m wspd']]
        qc_3hr['4m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['4m wdir']]
        qc_3hr['7m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['7m wdir']]
        qc_3hr['15m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['15m wdir']]
        qc_3hr['30m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['30m wdir']]
        qc_3hr['7m RH']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['7m RH']]
        qc_3hr['30m RH']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['30m RH']]

        deltaT_3hr = (round((qc_3hr['4m temp'].astype(float) -  qc_3hr['1m temp'].astype(float)),1)).astype(str)
        deltaT_1hr = (round((qc_1hr['4m temp'].astype(float) -  qc_1hr['1m temp'].astype(float)),1)).astype(str)
        deltaT_10min = (round((qc_10min['4m temp'].astype(float) -  qc_10min['1m temp'].astype(float)),1)).astype(str)

        deltaT_10min = [str(x).rjust(6,' ') for x in deltaT_10min]
        deltaT_1hr = [str(x).rjust(6,' ') for x in deltaT_1hr]
        deltaT_3hr = [str(x).rjust(6,' ') for x in deltaT_3hr]

        qc_3hr_std = qc_3hr[['year','jday','month','day','time','4m temp','pressure','4m wspd','4m wdir','7m RH']]
        qc_3hr_std['deltaT'] = deltaT_3hr
        qc_1hr_std = qc_1hr[['year','jday','month','day','time','4m temp','pressure','4m wspd','4m wdir','7m RH']]
        qc_1hr_std['deltaT'] = deltaT_1hr
        qc_10min_std = qc_10min[['year','jday','month','day','time','4m temp','pressure','4m wspd','4m wdir','7m RH']]
        qc_10min_std['deltaT'] = deltaT_10min
        
        number_of_rows = len(qc_10min)
        number_of_days = qc_10min['day'].iloc[-1]
        raw_header = aws_abbreviation+"  "+str(argos_id)+"  "+str(name)+"                "+str(lat)+"   "+str(lon)+"    "+str(elev)+"  "+str(year)+"   "+str(month)+"  "+str(number_of_days)+"  "+str(number_of_rows)+"            RH       delta-T"
        dat_header = '  '+str(month)+'  '+str(year_abv)+'   Station : '+str(argos_id)+'  '+str(name)+'\n  Lat : '+str(lat)+'  Long : '+str(lon)+'  Elev : '+str(elev)+' M'
  
        raw_file_df = qc_10min.copy()
    
        raw_file_df['1m temp_man_qc'] = df['1m temp_man_qc']
        raw_file_df['2m temp_man_qc'] = df['2m temp_man_qc']
        raw_file_df['4m temp_man_qc'] = df['4m temp_man_qc']
        raw_file_df['7m temp_man_qc'] = df['7m temp_man_qc']
        raw_file_df['15m temp_man_qc'] = df['15m temp_man_qc']
        raw_file_df['30m temp_man_qc'] = df['30m temp_man_qc']
        
        raw_file_df['pressure_man_qc'] = df['pressure_man_qc']
        raw_file_df['4m wdir_man_qc'] = df['4m wdir_man_qc']
        raw_file_df['7m wdir_man_qc'] = df['7m wdir_man_qc']
        raw_file_df['15m wdir_man_qc'] = df['15m wdir_man_qc']
        raw_file_df['30m wdir_man_qc'] = df['30m wdir_man_qc']
        
        raw_file_df['1m wspd_man_qc'] = df['1m wspd_man_qc']
        raw_file_df['2m wspd_man_qc'] = df['2m wspd_man_qc']
        raw_file_df['7m wspd_man_qc'] = df['7m wspd_man_qc']
        raw_file_df['15m wspd_man_qc'] = df['15m wspd_man_qc']
        raw_file_df['4m wspd_man_qc'] = df['4m wspd_man_qc']
        raw_file_df['30m wspd_man_qc'] = df['30m wspd_man_qc']
        raw_file_df['7m RH_man_qc'] = df['7m RH_man_qc']
        raw_file_df['30m RH_man_qc'] = df['30m RH_man_qc']
        
        for row in change_log_df.itertuples():
            datetime = row[1]
            variable = row[2]
            value = row[3]
            raw_file_df.loc[datetime,variable+'_man_qc'] = value 
        
        q1h_output_path = base_path + all_filenames.loc['q1h_output_path'].values[0] %(short_name,year,month)
        q3h_output_path = base_path + all_filenames.loc['q3h_output_path'].values[0] %(short_name,year,month)
        q10_output_path = base_path + all_filenames.loc['q10_output_path'].values[0] %(short_name,year,month)
        raw_output_path = base_path + all_filenames.loc['raw_output_path'].values[0] %(short_name,year,month)
        dat_output_path = base_path + all_filenames.loc['dat_output_path'].values[0] %(argos_id[2:],month,year_abv)
        
        tt_q1h_all_output_path = base_path + all_filenames.loc['tt_q1h_all_output_path'].values[0] %(short_name,year,month)
        tt_q3h_all_output_path = base_path + all_filenames.loc['tt_q3h_all_output_path'].values[0] %(short_name,year,month)
        tt_q10_all_output_path = base_path + all_filenames.loc['tt_q10_all_output_path'].values[0] %(short_name,year,month)
        tt_dat_all_output_path = base_path + all_filenames.loc['tt_dat_all_output_path'].values[0] %(argos_id[2:],month,year_abv)
         
        len_temp1_qc = len(raw_file_df['1m temp_man_qc'].dropna())
        len_temp2_qc = len(raw_file_df['2m temp_man_qc'].dropna())
        len_temp4_qc = len(raw_file_df['4m temp_man_qc'].dropna())
        len_temp7_qc = len(raw_file_df['7m temp_man_qc'].dropna())
        len_temp15_qc = len(raw_file_df['15m temp_man_qc'].dropna())
        len_temp30_qc = len(raw_file_df['30m temp_man_qc'].dropna())
        len_pres_qc =len(raw_file_df['pressure_man_qc'].dropna())
        len_wspd1_qc = len(raw_file_df['1m wspd_man_qc'].dropna())
        len_wspd2_qc = len(raw_file_df['2m wspd_man_qc'].dropna())
        len_wspd4_qc = len(raw_file_df['4m wspd_man_qc'].dropna())
        len_wspd7_qc = len(raw_file_df['7m wspd_man_qc'].dropna())
        len_wspd15_qc = len(raw_file_df['15m wspd_man_qc'].dropna())
        len_wspd30_qc = len(raw_file_df['30m wspd_man_qc'].dropna())
        len_wdir4_qc =len(raw_file_df['4m wdir_man_qc'].dropna())
        len_wdir7_qc =len(raw_file_df['7m wdir_man_qc'].dropna())
        len_wdir15_qc =len(raw_file_df['15m wdir_man_qc'].dropna())
        len_wdir30_qc =len(raw_file_df['30m wdir_man_qc'].dropna())
        len_rh7_qc =len(raw_file_df['7m RH_man_qc'].dropna())
        len_rh30_qc =len(raw_file_df['30m RH_man_qc'].dropna())
        
        raw_file_df['1m temp_rules'] = df['1m temp_rules']
        raw_file_df['2m temp_rules'] = df['2m temp_rules']
        raw_file_df['4m temp_rules'] = df['4m temp_rules']
        raw_file_df['7m temp_rules'] = df['7m temp_rules']
        raw_file_df['15m temp_rules'] = df['15m temp_rules']
        raw_file_df['30m temp_rules'] = df['30m temp_rules']
        raw_file_df['pressure_rules'] = df['pressure_rules']
        raw_file_df['1m wspd_rules'] = df['1m wspd_rules']
        raw_file_df['2m wspd_rules'] = df['2m wspd_rules']
        raw_file_df['4m wspd_rules'] =df['4m wspd_rules']
        raw_file_df['7m wspd_rules'] = df['7m wspd_rules']
        raw_file_df['15m wspd_rules'] = df['15m wspd_rules']
        raw_file_df['30m wspd_rules'] = df['30m wspd_rules']
        raw_file_df['4m wdir_rules'] = df['4m wdir_rules']
        raw_file_df['7m wdir_rules'] = df['7m wdir_rules']
        raw_file_df['15m wdir_rules'] = df['15m wdir_rules']
        raw_file_df['30m wdir_rules'] = df['30m wdir_rules']
        raw_file_df['7m RH_rules'] = df['7m RH_rules']
        raw_file_df['30m RH_rules'] = df['30m RH_rules']

        len_temp1_rules = len(raw_file_df['1m temp_rules'].dropna())
        len_temp2_rules = len(raw_file_df['2m temp_rules'].dropna())
        len_temp4_rules = len(raw_file_df['4m temp_rules'].dropna())
        len_temp7_rules = len(raw_file_df['7m temp_rules'].dropna())
        len_temp15_rules = len(raw_file_df['15m temp_rules'].dropna())
        len_temp30_rules = len(raw_file_df['30m temp_rules'].dropna())
        len_pres_rules =len(raw_file_df['pressure_rules'].dropna())
        len_wspd1_rules = len(raw_file_df['1m wspd_rules'].dropna())
        len_wspd2_rules = len(raw_file_df['2m wspd_rules'].dropna())
        len_wspd4_rules = len(raw_file_df['4m wspd_rules'].dropna())
        len_wspd7_rules = len(raw_file_df['7m wspd_rules'].dropna())
        len_wspd15_rules = len(raw_file_df['15m wspd_rules'].dropna())
        len_wspd30_rules = len(raw_file_df['30m wspd_rules'].dropna())
        len_wdir4_rules =len(raw_file_df['4m wdir_rules'].dropna())
        len_wdir7_rules =len(raw_file_df['7m wdir_rules'].dropna())
        len_wdir15_rules =len(raw_file_df['15m wdir_rules'].dropna())
        len_wdir30_rules =len(raw_file_df['30m wdir_rules'].dropna())
        len_rh7_rules =len(raw_file_df['7m RH_rules'].dropna())
        len_rh30_rules =len(raw_file_df['30m RH_rules'].dropna())
       
        raw_file_df =raw_file_df.fillna(444.0)
        for col in raw_file_df.columns:
            if col[-6:] == 'man_qc':
                raw_file_df[col] = raw_file_df[col].astype(str).str.rjust(6,' ')
            if col[-5:] == 'rules':
                raw_file_df[col] = raw_file_df[col].astype(str).str.rjust(6,' ')
        raw_header_counter =str(len_temp1_qc).rjust(6,' ')+str(len_temp1_rules).rjust(6,' ')+'\n'+str(len_temp2_qc).rjust(6,' ')+str(len_temp2_rules).rjust(6,' ')+'\n'+str(len_temp4_qc).rjust(6,' ')+str(len_temp4_rules).rjust(6,' ')+'\n'+str(len_temp7_qc).rjust(6,' ')+str(len_temp7_rules).rjust(6,' ')+'\n'+str(len_temp15_qc).rjust(6,' ')+str(len_temp15_rules).rjust(6,' ')+'\n'+str(len_temp30_qc).rjust(6,' ')+str(len_temp30_rules).rjust(6,' ')+'\n'+str(len_pres_qc).rjust(6,' ')+str(len_pres_rules).rjust(6,' ')+'\n'+str(len_wspd1_qc).rjust(6,' ')+str(len_wspd1_rules).rjust(6,' ')+'\n'+str(len_wspd2_qc).rjust(6,' ')+str(len_wspd2_rules).rjust(6,' ')+'\n'+str(len_wspd4_qc).rjust(6,' ')+str(len_wspd4_rules).rjust(6,' ')+'\n'+str(len_wspd7_qc).rjust(6,' ')+str(len_wspd7_rules).rjust(6,' ')+'\n'+str(len_wspd15_qc).rjust(6,' ')+str(len_wspd15_rules).rjust(6,' ')+'\n'+str(len_wspd30_qc).rjust(6,' ')+str(len_wspd30_rules).rjust(6,' ')+'\n'+str(len_wdir4_qc).rjust(6,' ')+str(len_wdir4_rules).rjust(6,' ')+'\n'+str(len_wdir7_qc).rjust(6,' ')+str(len_wdir7_rules).rjust(6,' ')+'\n'+str(len_wdir15_qc).rjust(6,' ')+str(len_wdir15_rules).rjust(6,' ')+'\n'+str(len_wdir30_qc).rjust(6,' ')+str(len_wdir30_rules).rjust(6,' ')+'\n'+str(len_rh7_qc).rjust(6,' ')+str(len_rh7_rules).rjust(6,' ')+'\n'+str(len_rh30_qc).rjust(6,' ')+str(len_rh30_rules).rjust(6,' ')          
        raw_file_df=raw_file_df[['year','jday','month','day','time','1m temp','1m temp_man_qc','1m temp_rules','2m temp','2m temp_man_qc','2m temp_rules','4m temp','4m temp_man_qc','4m temp_rules','7m temp','7m temp_man_qc','7m temp_rules','15m temp','15m temp_man_qc','15m temp_rules','30m temp','30m temp_man_qc','30m temp_rules','pressure','pressure_man_qc','pressure_rules','1m wspd','1m wspd_man_qc','1m wspd_rules','2m wspd','2m wspd_man_qc','2m wspd_rules','4m wspd','4m wspd_man_qc','4m wspd_rules','7m wspd','7m wspd_man_qc','7m wspd_rules','15m wspd','15m wspd_man_qc','15m wspd_rules','30m wspd','30m wspd_man_qc','30m wspd_rules','4m wdir','4m wdir_man_qc','4m wdir_rules','7m wdir','7m wdir_man_qc','7m wdir_rules','15m wdir','15m wdir_man_qc','15m wdir_rules','30m wdir','30m wdir_man_qc','30m wdir_rules','7m RH','7m RH_man_qc','7m RH_rules','30m RH','30m RH_man_qc','30m RH_rules']]
        dat_file_df_std = (qc_3hr.copy())[['4m temp','pressure','4m wspd','4m wdir','7m RH']]
        dat_file_df = (qc_3hr.copy())[['1m temp','2m temp','4m temp','7m temp','15m temp','30m temp','pressure','1m wspd','2m wspd','4m wspd','7m wspd','15m wspd','30m wspd','4m wdir','7m wdir','15m wdir','30m wdir','7m RH','30m RH']]
        #raw_file_df=raw_file_df[['year','jday','month','day','time','1m temp','1m temp_man_qc','1m temp_rules','2m temp','2m temp_man_qc','2m temp_rules','4m temp','4m temp_man_qc','4m temp_rules','7m temp','7m temp_man_qc','7m temp_rules','15m temp','15m temp_man_qc','15m temp_rules','30m temp','30m temp_man_qc','30m temp_rules','pressure','pressure_man_qc','pressure_rules','1m wspd','1m wspd_man_qc','1m wspd_rules','2m wspd','2m wspd_man_qc','2m wspd_rules','4m wspd','4m wspd_man_qc','4m wspd_rules','7m wspd','7m wspd_man_qc','7m wspd_rules','15m wspd','15m wspd_man_qc','15m wspd_rules','30m wspd','30m wspd_man_qc','30m wspd_rules','4m wdir','4m wdir_man_qc','4m wdir_rules','7m wdir','7m wdir_man_qc','7m wdir_rules','15m wdir','15m wdir_man_qc','15m wdir_rules','30m wdir','30m wdir_man_qc','30m wdir_rules','7m RH','7m RH_man_qc','7m RH_rules','30m RH','30m RH_man_qc','30m RH_rules']]
        #with open(raw_output_path.iloc[0], "w") as f:
        with open(raw_output_path, "w") as f:
            # Write the header
            f.write("".join(raw_header) + "\n")
            f.write("".join(raw_header_counter) + "\n")
            # Write each row
            for row in raw_file_df.itertuples(index=True, name=None):
                f.write(" ".join(map(str, row)) + "\n")
        #with open(q3h_output_path.iloc[0], "w") as f:
        with open(q3h_output_path, "w") as f:
            # Write the header
            f.write("".join(qc_header) + "\n")
            # Write each row
            for row in qc_3hr_std.itertuples(index=False, name=None):
                f.write(" ".join(map(str, row)) + "\n")
        #with open(q1h_output_path.iloc[0], "w") as f:
        with open(q1h_output_path, "w") as f:
            # Write the header
            f.write("".join(qc_header) + "\n")
            # Write each row
            for row in qc_1hr_std.itertuples(index=False, name=None):
                f.write(" ".join(map(str, row)) + "\n")
        #with open(q10_output_path.iloc[0], "w") as f:
        with open(q10_output_path, "w") as f:
            # Write the header
            f.write("".join(qc_header) + "\n")
            # Write each row
            for row in qc_10min_std.itertuples(index=False, name=None):
                f.write(" ".join(map(str, row)) + "\n")
        #with open(tt_q3h_all_output_path.iloc[0], "w") as f:
        with open(tt_q3h_all_output_path, "w") as f:
            # Write the header
            f.write("".join(qc_header) + "\n")
            # Write each row
            for row in qc_3hr.itertuples(index=False, name=None):
                f.write(" ".join(map(str, row)) + "\n")
        #with open(tt_q1h_all_output_path.iloc[0], "w") as f:
        with open(tt_q1h_all_output_path, "w") as f:
            # Write the header
            f.write("".join(qc_header) + "\n")
            # Write each row
            for row in qc_1hr.itertuples(index=False, name=None):
                f.write(" ".join(map(str, row)) + "\n")
        #with open(tt_q10_all_output_path.iloc[0], "w") as f:
        with open(tt_q10_all_output_path, "w") as f:
            # Write the header
            f.write("".join(qc_header) + "\n")
            # Write each row
            for row in qc_10min.itertuples(index=False, name=None):
                f.write(" ".join(map(str, row)) + "\n")    
        #with open(dat_output_path.iloc[0], "w") as f:
        with open(dat_output_path, "w") as f:
            # Write the header
            f.write("".join(dat_header) + "\n")
            # Write each row
            for row in dat_file_df.itertuples(index=True, name=None):
                f.write(" ".join(map(str, row)) + "\n")
        #with open(tt_dat_all_output_path.iloc[0], "w") as f:
        with open(tt_dat_all_output_path, "w") as f:
            # Write the header
            f.write("".join(dat_header) + "\n")
            # Write each row
            for row in dat_file_df_std.itertuples(index=True, name=None):
                f.write(" ".join(map(str, row)) + "\n")                
        return(dcc.send_data_frame(copied_df.to_csv , qc_csv_output_path),
            dcc.send_data_frame(change_log_df.to_csv, change_log_output_path))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if argos_id == '99616':
    @app.callback(Output('display-met-data-subplots','figure'), #allow_duplicate=True
          [Input('select-variables','value'),
          Input('select-level','value'),
          Input('marker-size','value'),
          Input('day-range','value'),
          Input('center-day','value'),
          Input('min-temp-ylim','value'),
          Input('max-temp-ylim','value'),
          Input('min-pres-ylim','value'),
          Input('max-pres-ylim','value'),
          Input('min-wspd-ylim','value'),
          Input('max-wspd-ylim','value'),
          Input('min-wdir-ylim','value'),
          Input('max-wdir-ylim','value'),
          Input('min-rh-ylim','value'),
          Input('max-rh-ylim','value'),
          Input('rules-toggle','value')],)  #,prevent_initial_call=True 
    
    def update_graph(variables_selected,levels_selected,markersize,day_range,center_day,mintemp,maxtemp,minpres,maxpres,minwspd,maxwspd,minwdir,maxwdir,minrh,maxrh,rules):
        level_vars = [level + var for level in levels_selected for var in variables_selected if var != 'panel_temp' and var != 'voltage' and var != 'pressure' and var != 'RH']
        for level in levels_selected:
            for var in variables_selected: 
                if var == 'RH':
                    if level == '4m ' or level == '7m ' or level == '15m ' or level == '30m ':
                        level_vars.append(level+var)
                
        if 'pressure' in variables_selected: level_vars.append('pressure')
        if 'panel_temp' in variables_selected: level_vars.append('panel_temp')
        if 'voltage' in variables_selected: level_vars.append('voltage')
        use_list_vars = level_vars 
        dff = noqc_df[use_list_vars]

        level_colors = [level+var for level in levels_selected for var in variables_selected if var != 'panel_temp' and var != 'voltage' and var != 'pressure' and var != 'RH']
        for level in levels_selected:
            for var in variables_selected: 
                if var == 'RH':
                    if level == '4m ' or level == '7m ' or level == '15m ' or level == '30m ':
                        level_colors.append(level+var)
                        
        if 'pressure' in variables_selected: level_colors.append('pressure')
        if 'panel_temp' in variables_selected: level_colors.append('panel_temp')
        if 'voltage' in variables_selected: level_colors.append('voltage')
   
        bounds_dict= {'mintemp':mintemp,'maxtemp':maxtemp,'minpres':minpres,'maxpres':maxpres,'minwspd':minwspd,'maxwspd':maxwspd,'minwdir':minwdir,'maxwdir':maxwdir,'minRH':minrh,'maxRH':maxrh}
        ind_dict = {}
        copy_dff = dff.copy()
        if 'panel_temp' in dff.columns and 'RH' not in variables_selected :
            titles = variables_selected
            titles.remove('panel_temp')
        elif 'RH' in variables_selected and '4m RH' not in dff.columns and '7m RH' not in dff.columns and '15m RH' not in dff.columns and '30m RH' not in dff.columns and 'panel_temp' not in dff.columns:
            titles = variables_selected
            titles.remove('RH')          
        elif 'RH' in variables_selected and '4m RH' not in dff.columns and '7m RH' not in dff.columns and '15m RH' not in dff.columns and '30m RH' not in dff.columns and 'panel_temp' in dff.columns:
            titles = variables_selected
            titles.remove('RH') 
            titles.remove('panel_temp')
        else:
            titles = variables_selected             
        marker=False 
        
        fig = make_subplots(rows=len(titles), cols=1,subplot_titles=titles,
                            shared_xaxes=True, 
                            vertical_spacing=0.05, x_title='Date')
        for i, var in enumerate(variables_selected):
            i2 = i+1   
            if var != 'panel_temp':
                ind_dict[var+'_ind'] = i2
        
        for var, lev_color in zip(use_list_vars, level_colors):
            if var != 'panel_temp' and var != 'voltage' and var != 'pressure' and var[-2:] != 'RH':
                short_var = var[-4:]   
                row_num = ind_dict[short_var+'_ind']
            elif var == 'voltage' or var == 'pressure' :
                row_num = ind_dict[var+'_ind']
                short_var = 'test'
            elif var == 'panel_temp': 
                row_num = ind_dict['temp_ind']
                short_var='Panel Temp'
            elif var[-2:] == 'RH':
                short_var= 'RH'
                row_num = ind_dict[var[-2:]+'_ind']
        
            if short_var == 'temp':
                fig.add_trace(go.Scatter(x=dff.index, y=dff[var].astype(np.float64), mode='markers', name=var,marker=dict(color=copied_df[lev_color+'_colors']),selected_marker_color='grey'),
                                row=row_num, col=1)
                if qc_type == "prev":
                    last_days_dff = last_days_df[use_list_vars]
                    fig.add_trace(go.Scatter(x=last_days_dff.index, y=last_days_dff[var].astype(np.float64), mode='markers', name="prev"+var,marker_color='lightgrey',showlegend=False),
                                    row=row_num, col=1)
                if qc_type == "both":
                    next_few_days_dff = next_few_days_df[use_list_vars]
                    fig.add_trace(go.Scatter(x=next_few_days_dff.index, y=next_few_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="next"+var,marker_color='lightgrey'),
                                row=row_num, col=1)
                    last_days_dff = last_days_df[use_list_vars]
                    fig.add_trace(go.Scatter(x=last_days_dff.index, y=last_days_dff[var].astype(np.float64), mode='markers', name="pres"+var,marker_color='lightgrey',showlegend=False),
                                    row=row_num, col=1)
                if qc_type == "next":
                    next_few_days_dff = next_few_days_df[use_list_vars]
                    fig.add_trace(go.Scatter(x=next_few_days_dff.index, y=next_few_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="next"+var,marker_color='lightgrey'),
                                row=row_num, col=1)   
           
            if var == 'panel_temp':
                marker=True
                fig.add_trace(go.Scatter(x=dff.index, y=dff['panel_temp'].astype(np.float64), mode='markers', name='Panel Temp', marker_color='darkseagreen'),
                                    row=ind_dict['temp_ind'], col=1)
                if qc_type == "prev":
                    fig.add_trace(go.Scatter(x=last_days_df.index, y=last_days_df['panel_temp'].astype(np.float64),showlegend=False, name="prev"+var,mode='markers', marker_color='lightseagreen'),
                                    row=ind_dict['temp_ind'], col=1)
                if qc_type == "both":
                    fig.add_trace(go.Scatter(x=last_days_df.index, y=last_days_df['panel_temp'].astype(np.float64),showlegend=False, name="prev"+var,mode='markers', marker_color='lightseagreen'),
                                    row=ind_dict['temp_ind'], col=1)
                    fig.add_trace(go.Scatter(x=next_few_days_df.index, y=next_few_days_df['panel_temp'].astype(np.float64),showlegend=False, mode='markers', name="net"+var,marker_color='lightseagreen'),
                            row=ind_dict['temp_ind'], col=1)
                if qc_type == "next":
                    fig.add_trace(go.Scatter(x=next_few_days_df.index, y=next_few_days_df['panel_temp'].astype(np.float64),showlegend=False, mode='markers', name="next"+var,marker_color='lightseagreen'),
                            row=ind_dict['temp_ind'], col=1)
               
            if short_var != 'temp' and var != 'panel_temp' and var != '1m RH' and var != '2m RH' and marker == True:
                fig.add_trace(go.Scatter(x=dff.index, y=dff[var].astype(np.float64), mode='markers', name=str(var),marker=dict(color=copied_df[lev_color+'_colors']),selected_marker_color='lightseagreen'),
                                row=row_num, col=1)
                if qc_type == "both" or qc_type == 'prev':
                    next_few_days_dff = next_few_days_df[use_list_vars]
                    last_days_dff = last_days_df[use_list_vars]
                    fig.add_trace(go.Scatter(x=next_few_days_dff.index, y=next_few_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="next"+var,marker_color='lightgrey'),
                                row=row_num, col=1)
                    fig.add_trace(go.Scatter(x=last_days_dff.index, y=last_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="prev"+var ,marker_color='lightgrey'),
                                row=row_num, col=1)  
                if qc_type == "next":
                    next_few_days_dff = next_few_days_df[use_list_vars]
                    fig.add_trace(go.Scatter(x=next_few_days_dff.index, y=next_few_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="next"+var,marker_color='lightgrey'),
                                row=row_num, col=1)    
                if qc_type == 'prev':
                    last_days_dff = last_days_df[use_list_vars]
                    fig.add_trace(go.Scatter(x=last_days_dff.index, y=last_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="prev"+var ,marker_color='lightgrey'),
                                row=row_num, col=1)  
      
            if short_var != 'temp' and var != 'panel_temp' and var != '1m RH' and var != '2m RH' and marker == False:
                fig.add_trace(go.Scatter(x=dff.index, y=dff[var].astype(np.float64), mode='markers', name=str(var),marker=dict(color=copied_df[lev_color+'_colors']),selected_marker_color='grey'),
                                row=row_num, col=1)
                if qc_type == "next" :
                    next_few_days_dff = next_few_days_df[use_list_vars]
                    fig.add_trace(go.Scatter(x=next_few_days_dff.index, y=next_few_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="next"+var,marker_color='lightgrey'),
                                row=row_num, col=1)
                if qc_type == "both":
                    next_few_days_dff = next_few_days_df[use_list_vars]
                    last_days_dff = last_days_df[use_list_vars]
                    fig.add_trace(go.Scatter(x=next_few_days_dff.index, y=next_few_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="next"+var,marker_color='lightgrey'),
                                row=row_num, col=1)
                    fig.add_trace(go.Scatter(x=last_days_dff.index, y=last_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="prev"+var ,marker_color='lightgrey'),
                                row=row_num, col=1)  
                if qc_type == 'prev':
                    last_days_dff = last_days_df[use_list_vars]
                    fig.add_trace(go.Scatter(x=last_days_dff.index, y=last_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="prev"+var ,marker_color='lightgrey'),
                                row=row_num, col=1)  
       
        fig.update_traces(mode="markers", hovertemplate=None)
        fig.update_layout(hovermode="x")
        fig.update_layout(clickmode='event+select',dragmode='pan')
        fig.update_traces(marker=dict(size=int(markersize)))
        fig.update_layout(autosize=True,height=700,margin=dict(l=20, r=20, t=50, b=50))
        
        for i3, x in enumerate(fig.data):
            varname = x['name']
            if varname != 'panel_temp' and varname != 'voltage' and varname != 'pressure' and varname != '4m RH' and varname != '7m RH' and varname != '15m RH' and varname != '30m RH' and varname != None:
                varname1 = varname[-4:]   
            if varname == 'pressure' and varname in dff.columns:
                varname1 = varname[0:4]
            if varname == '4m RH' or varname == '7m RH' or varname == '15m RH' or varname == '30m RH' and varname in dff.columns:
                varname1 = varname[-2:]
            if varname in dff.columns and varname != 'voltage' and varname != 'panel_temp' and varname != 'pressure':
                fig.update_yaxes(range=(bounds_dict['min'+varname1], bounds_dict['max'+varname1]), row=ind_dict[varname1+'_ind'], col=1) 
            if varname == 'pressure':
                fig.update_yaxes(range=(bounds_dict['min'+varname1], bounds_dict['max'+varname1]), row=ind_dict[varname+'_ind'], col=1) 
        if isinstance(day_range, int):
            if isinstance(center_day, int) == True:
                half_day_range = day_range/2
                input_center_date = pd.to_datetime(str(year)+'/'+str(month)+'/'+str(center_day), format='%Y/%m/%d')
                prev_date_range = input_center_date - timedelta(days=half_day_range)
                next_date_range = input_center_date + timedelta(days=half_day_range)
                fig.update_xaxes(range=(prev_date_range, next_date_range))
            else:
                input_center_date = pd.to_datetime(str(year)+'/'+str(month)+'/01', format='%Y/%m/%d')
                prev_date_range = input_center_date
                next_date_range = input_center_date + timedelta(days=day_range)
                
                fig.update_xaxes(range=(prev_date_range, next_date_range))
                
        if rules == 'No':
            for i3, x in enumerate(fig['data']):
                varname = fig['data'][i3]['name']
                if varname[0:4] != 'prev' and varname[0:4] != 'next':
                    fig['data'][i3]['marker']['color'] = solid_color_df[varname+'_colors'].values
        else:        
            for i3, x in enumerate(fig['data']):
                varname = fig['data'][i3]['name']
                if varname[0:4] != 'prev' and varname[0:4] != 'next':
                    fig['data'][i3]['marker']['color'] = copied_df[varname+'_colors'].values
        return(fig)

    @app.callback([Output('display-hover-data1', 'value'),
        Output('display-hover-data2', 'value'),
        Output('display-hover-data4', 'value'),
        Output('display-hover-data7', 'value'),
        Output('display-hover-data15', 'value'),
        Output('display-hover-data30', 'value')],
        Input('display-met-data-subplots', 'hoverData'),
        [State('display-met-data-subplots', 'figure')],prevent_initial_call=True)
    
    def display_hover_data(hoverData, figure):
        datetime = pd.to_datetime(hoverData['points'][0]['x'])
        hover_values = noqc_df.loc[datetime]  
        hover_date = str(datetime)[:10]
        hover_time =str(datetime)[12:]
    
        hover_temp1 =hover_values['1m temp']
        hover_temp2 =hover_values['2m temp']
        hover_temp4 =hover_values['4m temp']
        hover_temp7 =hover_values['7m temp']
        hover_temp15 =hover_values['15m temp']
        hover_temp30 =hover_values['30m temp']
        
        hover_pres =hover_values['pressure']
        hover_rh4 =hover_values['4m RH']
        hover_rh7 =hover_values['7m RH']
        hover_rh15 =hover_values['15m RH']
        hover_rh30 =hover_values['30m RH']
        hover_wspd1 =hover_values['1m wspd']
        hover_wspd2 =hover_values['2m wspd']
        hover_wspd4 =hover_values['4m wspd']
        hover_wspd7 =hover_values['7m wspd']
        hover_wspd15 =hover_values['15m wspd']
        hover_wspd30 =hover_values['30m wspd']
        hover_wdir1 =hover_values['1m wdir']
        hover_wdir2 =hover_values['2m wdir']
        hover_wdir4 =hover_values['4m wdir']
        hover_wdir7 =hover_values['7m wdir']
        hover_wdir15 =hover_values['15m wdir']
        hover_wdir30 =hover_values['30m wdir']
        ob_num = len(copied_df.loc[:datetime]) -1
        info_str1 = 'Date: '+str(hover_date)[:10]+'\nTime: '+str(hover_time)+'\nTemperature: '+str(hover_temp1)+'\nPressure: '+str(hover_pres)+'\nWind Speed: '+str(hover_wspd1)+'\nWind Direction: '+str(hover_wdir1)+'\nObs ID: '+str(ob_num)     
        info_str2 = 'Date: '+str(hover_date)[:10]+'\nTime: '+str(hover_time)+'\nTemperature: '+str(hover_temp2)+'\nPressure: '+str(hover_pres)+'\nWind Speed: '+str(hover_wspd2)+'\nWind Direction: '+str(hover_wdir2)+'\nObs ID: '+str(ob_num)     
        info_str4 = 'Date: '+str(hover_date)[:10]+'\nTime: '+str(hover_time)+'\nTemperature: '+str(hover_temp4)+'\nPressure: '+str(hover_pres)+'\nWind Speed: '+str(hover_wspd4)+'\nWind Direction: '+str(hover_wdir4)+'\nRelative Humidity: '+str(hover_rh4)+'\nObs ID: '+str(ob_num)
        info_str7 = 'Date: '+str(hover_date)[:10]+'\nTime: '+str(hover_time)+'\nTemperature: '+str(hover_temp7)+'\nPressure: '+str(hover_pres)+'\nWind Speed: '+str(hover_wspd7)+'\nWind Direction: '+str(hover_wdir7)+'\nRelative Humidity: '+str(hover_rh7)+'\nObs ID: '+str(ob_num)     
        info_str15 = 'Date: '+str(hover_date)[:10]+'\nTime: '+str(hover_time)+'\nTemperature: '+str(hover_temp15)+'\nPressure: '+str(hover_pres)+'\nWind Speed: '+str(hover_wspd15)+'\nWind Direction: '+str(hover_wdir15)+'\nRelative Humidity: '+str(hover_rh15)+'\nObs ID: '+str(ob_num)     
        info_str30 = 'Date: '+str(hover_date)[:10]+'\nTime: '+str(hover_time)+'\nTemperature: '+str(hover_temp30)+'\nPressure: '+str(hover_pres)+'\nWind Speed: '+str(hover_wspd30)+'\nWind Direction: '+str(hover_wdir30)+'\nRelative Humidity: '+str(hover_rh30)+'\nObs ID: '+str(ob_num)     
    
        return(info_str1, info_str2, info_str4, info_str7, info_str15, info_str30)
        
    @app.callback([Output('display-click-data', 'value'), 
                  Output('updated-data', 'data'),
                  Output('change-log', 'data'),
                  Output('display-met-data-subplots','figure',allow_duplicate=True)],
                  [Input('display-met-data-subplots','clickData'),
                  Input('display-met-data-subplots', 'selectedData'),
                  Input('undo-button', 'n_clicks'),
                  Input('reset-button', 'n_clicks')],
                  [State('display-met-data-subplots', 'figure'),
                   State('rules-toggle','value')],prevent_initial_call='initial_duplicate')

    def display_clickdata(clickData1, selectData1, undo_clicks,reset_clicks, figure,rules):
        global copied_df, change_log, solid_color_df  # Ensure global reference
        ctx = dash.callback_context
        ind_dict = {}
        if ctx.triggered_id == 'undo-button' and change_log:
            for i in range(len(figure['data'])):
                ind_dict[figure['data'][i]['name']] = i
            last_change = change_log.pop()  # Revert the last change
            date = pd.to_datetime(last_change['date'])
            column = last_change['column']
            original_value = last_change['original']
            copied_df.at[date, column] = original_value
            color_pre_change_value = df.at[date,column+'_colors']
            copied_df.at[date, column+'_colors'] = color_pre_change_value
            solid_pre_change_value = copied_solid_color_df.at[date,column+'_colors']
            solid_color_df.at[date, column+'_colors'] = solid_pre_change_value
            if column in ind_dict.keys() and rules == 'Yes':
                figure['data'][ind_dict[column]]['marker']['color'] = copied_df[column+'_colors'].values
            if column in ind_dict.keys() and rules == 'No':
                figure['data'][ind_dict[column]]['marker']['color'] = solid_color_df[column+'_colors'].values
            return (f"Undo: {date} - {column} reverted to {original_value}", copied_df.to_dict('records'), change_log,figure)
        
        if ctx.triggered_id == 'reset-button':
            
            for i in range(len(figure['data'])):
                ind_dict[figure['data'][i]['name']] = i
            copied_df = df.copy()
            solid_color_df = copied_solid_color_df.copy()
            for column in ind_dict.keys():
                if column[0:4] != 'next' and column [0:4] != 'prev' and rules == 'Yes':
                    figure['data'][ind_dict[column]]['marker']['color'] = copied_df[column+'_colors']
                if column[0:4] != 'next' and column [0:4] != 'prev' and rules == 'No':
                    figure['data'][ind_dict[column]]['marker']['color'] = solid_color_df[column+'_colors']
            change_log = []  # Clear the change log
            return("Data reset", copied_df.to_dict('records'), change_log)
        # Use a set to track all selected points (date, column)
        selected_points = set()
        if selectData1 is None and clickData1 is None:
            raise PreventUpdate
        elif selectData1 is not None:
            for i in range(len(figure['data'])):
                ind_dict[figure['data'][i]['name']] = i
            box_points = {}
            new_box_points = [[pt['x'], figure['data'][pt['curveNumber']]['name']] for pt in selectData1.get('points', []) ]
            #  Update box_points with the current selection
            box_points = new_box_points
            for sel_data in new_box_points:
                date=pd.to_datetime(sel_data[0])
                column=sel_data[1]
                point = (date, column)
                #original_value = no.float(copied_df.at[date, column])
                original_value = copied_df.at[date, column]
                new_value = np.float64(444.0)
                if point not in selected_points:
                    # Add new selection
                    selected_points.add(point)
                    if original_value != new_value and np.isnan(original_value)==False:
                        copied_df.at[date, column] = new_value
                        copied_df.at[date, column+'_colors'] = 'grey'
                        solid_color_df.at[date, column+'_colors'] = 'grey'
                        if rules == 'Yes':
                            figure['data'][ind_dict[column]]['marker']['color'] = copied_df[column+'_colors'].values
                        elif rules == 'No':
                            figure['data'][ind_dict[column]]['marker']['color'] = solid_color_df[column+'_colors'].values
                        change_log.append({
                            "date": date,
                            "column": column,
                            "original": original_value,
                            "new": new_value})
                        if column == '1m wspd':
                            wd_original_value = copied_df.at[date, '1m wdir']
                            copied_df.at[date, '1m wdir'] = new_value
                            copied_df.at[date, '1m wdir_colors'] = 'grey'
                            solid_color_df.at[date,'1m wdir_colors'] = 'grey'
                            if '1m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['1m wdir']]['marker']['color'] = copied_df['1m wdir_colors'].values
                            if '1m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['1m wdir']]['marker']['color'] = solid_color_df['1m wdir_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '1m wdir',
                                "original": wd_original_value,
                                "new": new_value})
                        if column == '1m wdir':
                            ws_original_value = copied_df.at[date, '1m wspd']
                            copied_df.at[date, '1m wspd'] = new_value
                            copied_df.at[date,'1m wspd_colors'] = 'grey'
                            solid_color_df.at[date, '1m wspd_colors'] = 'grey'
                            if '1m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['1m wspd']]['marker']['color'] = copied_df['1m wspd_colors'].values
                            if '1m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['1m wspd']]['marker']['color'] = solid_color_df['1m wspd_colors'].values 
                            change_log.append({
                                "date": date,
                                "column": '1m wspd',
                                "original": ws_original_value,
                                "new": new_value})
                        if column == '2m wspd':
                            wd_original_value = copied_df.at[date, '2m wdir']
                            copied_df.at[date, '2m wdir'] = new_value
                            copied_df.at[date, '2m wdir_colors'] = 'grey'
                            solid_color_df.at[date,'2m wdir_colors'] = 'grey'
                            if '2m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['2m wdir']]['marker']['color'] = copied_df['2m wdir_colors'].values
                            if '2m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['2m wdir']]['marker']['color'] = solid_color_df['2m wdir_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '2m wdir',
                                "original": wd_original_value,
                                "new": new_value})
                        if column == '2m wdir':
                            ws_original_value = copied_df.at[date, '2m wspd']
                            copied_df.at[date, '2m wspd'] = new_value
                            copied_df.at[date,'2m wspd_colors'] = 'grey'
                            solid_color_df.at[date, '2m wspd_colors'] = 'grey'
                            if '2m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['2m wspd']]['marker']['color'] = copied_df['2m wspd_colors'].values
                            if '2m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['2m wspd']]['marker']['color'] = solid_color_df['2m wspd_colors'].values 
                            change_log.append({
                                "date": date,
                                "column": '2m wspd',
                                "original": ws_original_value,
                                "new": new_value})
                        if column == '4m wspd':
                            wd_original_value = copied_df.at[date, '4m wdir']
                            copied_df.at[date, '4m wdir'] = new_value
                            copied_df.at[date, '4m wdir_colors'] = 'grey'
                            solid_color_df.at[date,'4m wdir_colors'] = 'grey'
                            if '4m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['4m wdir']]['marker']['color'] = copied_df['4m wdir_colors'].values
                            if '4m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['4m wdir']]['marker']['color'] = solid_color_df['4m wdir_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '4m wdir',
                                "original": wd_original_value,
                                "new": new_value})
                        if column == '4m wdir':
                            ws_original_value = copied_df.at[date, '4m wspd']
                            copied_df.at[date, '4m wspd'] = new_value
                            copied_df.at[date,'4m wspd_colors'] = 'grey'
                            solid_color_df.at[date, '4m wspd_colors'] = 'grey'
                            if '4m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['4m wspd']]['marker']['color'] = copied_df['4m wspd_colors'].values
                            if '4m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['4m wspd']]['marker']['color'] = solid_color_df['4m wspd_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '4m wspd',
                                "original": ws_original_value,
                                "new": new_value})
                        if column == '7m wspd':
                            wd_original_value = copied_df.at[date, '7m wdir']
                            copied_df.at[date, '7m wdir'] = new_value
                            copied_df.at[date, '7m wdir_colors'] = 'grey'
                            solid_color_df.at[date,'7m wdir_colors'] = 'grey'
                            if '7m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['7m wdir']]['marker']['color'] = copied_df['7m wdir_colors'].values
                            if '7m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['7m wdir']]['marker']['color'] = solid_color_df['7m wdir_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '7m wdir',
                                "original": wd_original_value,
                                "new": new_value})
                        if column == '7m wdir':
                            ws_original_value = copied_df.at[date, '7m wspd']
                            copied_df.at[date, '7m wspd'] = new_value
                            copied_df.at[date,'7m wspd_colors'] = 'grey'
                            solid_color_df.at[date, '7m wspd_colors'] = 'grey'
                            if '7m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['7m wspd']]['marker']['color'] = copied_df['7m wspd_colors'].values
                            if '7m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['7m wspd']]['marker']['color'] = solid_color_df['7m wspd_colors'].values 
                            change_log.append({
                                "date": date,
                                "column": '7m wspd',
                                "original": ws_original_value,
                                "new": new_value})
                        if column == '15m wspd':
                            wd_original_value = copied_df.at[date, '15m wdir']
                            copied_df.at[date, '15m wdir'] = new_value
                            copied_df.at[date, '15m wdir_colors'] = 'grey'
                            solid_color_df.at[date,'15m wdir_colors'] = 'grey'
                            if '15m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['15m wdir']]['marker']['color'] = copied_df['15m wdir_colors'].values
                            if '15m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['15m wdir']]['marker']['color'] = solid_color_df['15m wdir_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '15m wdir',
                                "original": wd_original_value,
                                "new": new_value})
                        if column == '15m wdir':
                            ws_original_value = copied_df.at[date, '15m wspd']
                            copied_df.at[date, '15m wspd'] = new_value
                            copied_df.at[date,'15m wspd_colors'] = 'grey'
                            solid_color_df.at[date, '15m wspd_colors'] = 'grey'
                            if '15m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['15m wspd']]['marker']['color'] = copied_df['15m wspd_colors'].values
                            if '15m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['15m wspd']]['marker']['color'] = solid_color_df['15m wspd_colors'].values 
                            change_log.append({
                                "date": date,
                                "column": '15m wspd',
                                "original": ws_original_value,
                                "new": new_value})
                        if column == '30m wspd':
                            wd_original_value = copied_df.at[date, '30m wdir']
                            copied_df.at[date, '30m wdir'] = new_value
                            copied_df.at[date, '30m wdir_colors'] = 'grey'
                            solid_color_df.at[date,'30m wdir_colors'] = 'grey'
                            if '30m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['30m wdir']]['marker']['color'] = copied_df['30m wdir_colors'].values
                            if '30m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['30m wdir']]['marker']['color'] = solid_color_df['30m wdir_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '30m wdir',
                                "original": wd_original_value,
                                "new": new_value})
                        if column == '30m wdir':
                            ws_original_value = copied_df.at[date, '30m wspd']
                            copied_df.at[date, '30m wspd'] = new_value
                            copied_df.at[date,'30m wspd_colors'] = 'grey'
                            solid_color_df.at[date, '30m wspd_colors'] = 'grey'
                            if '30m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['30m wspd']]['marker']['color'] = copied_df['30m wspd_colors'].values
                            if '30m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['30m wspd']]['marker']['color'] = solid_color_df['30m wspd_colors'].values 
                            change_log.append({
                                "date": date,
                                "column": '30m wspd',
                                "original": ws_original_value,
                                "new": new_value})
                                
                    if original_value == new_value:
                        selected_points.discard(point)
                        noqc_original_value = noqc_df.at[date, column]
                        copied_df.at[date, column] = noqc_original_value
                        copied_df.at[date, column+'_colors'] = df.at[date, column+'_colors']
                        solid_pre_change_value = copied_solid_color_df.at[date,column+'_colors']
                        solid_color_df.at[date,column+'_colors'] = solid_pre_change_value
                        if rules == 'Yes':
                            figure['data'][ind_dict[column]]['marker']['color'] = copied_df[column+'_colors'].values
                        elif rules == 'No':
                            figure['data'][ind_dict[column]]['marker']['color'] = solid_color_df[column+'_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']== column:
                                del change_log[i]
                        if column == '1m wspd' :
                            wd_original_value = copied_df.at[date, '1m wdir']
                            noqc_original_value =  noqc_df.at[date, '1m wdir']
                            copied_df.at[date, '1m wdir'] = noqc_original_value
                            copied_df.at[date,'1m wdir_colors'] = df.at[date, '1m wdir_colors']
                            wd_solid_pre_change_value = copied_solid_color_df.at[date,'1m wdir_colors']
                            solid_color_df.at[date,'1m wdir_colors'] = wd_solid_pre_change_value
                            if '1m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['1m wdir']]['marker']['color'] = copied_df['1m wdir_colors'].values
                            elif '1m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['1m wdir']]['marker']['color'] = solid_color_df['1m wdir_colors'].values
                            for i,test in enumerate(change_log):
                                if change_log[i]['date'] == date and change_log[i]['column']== '1m wdir':
                                    del change_log[i]
                        if column == '1m wdir':
                            ws_original_value = copied_df.at[date, '1m wspd']
                            noqc_original_value =  noqc_df.at[date, '1m wspd']
                            copied_df.at[date, '1m wspd'] = noqc_original_value
                            copied_df.at[date,'1m wspd_colors'] = df.at[date, '1m wspd_colors']
                            ws_solid_pre_change_value = copied_solid_color_df.at[date,'1m wspd_colors']
                            solid_color_df.at[date,'1m wspd_colors'] = ws_solid_pre_change_value
                            if '1m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['1m wspd']]['marker']['color'] = copied_df['1m wspd_colors'].values
                            if '1m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['1m wspd']]['marker']['color'] = solid_color_df['1m wspd_colors'].values
                            for i,test in enumerate(change_log):
                                if change_log[i]['date'] == date and change_log[i]['column']== '1m wspd':
                                    del change_log[i]

                        if column == '2m wspd' :
                            wd_original_value = copied_df.at[date, '2m wdir']
                            noqc_original_value =  noqc_df.at[date, '2m wdir']
                            copied_df.at[date, '2m wdir'] = noqc_original_value
                            copied_df.at[date,'2m wdir_colors'] = df.at[date, '2m wdir_colors']
                            wd_solid_pre_change_value = copied_solid_color_df.at[date,'2m wdir_colors']
                            solid_color_df.at[date,'2m wdir_colors'] = wd_solid_pre_change_value
                            if '2m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['2m wdir']]['marker']['color'] = copied_df['2m wdir_colors'].values
                            if '2m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['2m wdir']]['marker']['color'] = solid_color_df['2m wdir_colors'].values
                            for i,test in enumerate(change_log):
                                if change_log[i]['date'] == date and change_log[i]['column']== '2m wdir':
                                    del change_log[i]
                        if column == '2m wdir':
                            ws_original_value = copied_df.at[date, '2m wspd']
                            noqc_original_value =  noqc_df.at[date, '2m wspd']
                            copied_df.at[date, '2m wspd'] = noqc_original_value
                            copied_df.at[date,'2m wspd_colors'] = df.at[date, '2m wspd_colors']
                            ws_solid_pre_change_value = copied_solid_color_df.at[date,'2m wspd_colors']
                            solid_color_df.at[date,'2m wspd_colors'] = ws_solid_pre_change_value
                            if '2m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['2m wspd']]['marker']['color'] = copied_df['2m wspd_colors'].values
                            if '2m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['2m wspd']]['marker']['color'] = solid_color_df['2m wspd_colors'].values
                            for i,test in enumerate(change_log):
                                if change_log[i]['date'] == date and change_log[i]['column']== '2m wspd':
                                    del change_log[i]

                        if column == '4m wspd' :
                            wd_original_value = copied_df.at[date, '4m wdir']
                            noqc_original_value =  noqc_df.at[date, '4m wdir']
                            copied_df.at[date, '4m wdir'] = noqc_original_value
                            copied_df.at[date,'4m wdir_colors'] = df.at[date, '4m wdir_colors']
                            wd_solid_pre_change_value = copied_solid_color_df.at[date,'4m wdir_colors']
                            solid_color_df.at[date,'4m wdir_colors'] = wd_solid_pre_change_value
                            if '4m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['4m wdir']]['marker']['color'] = copied_df['4m wdir_colors'].values
                            if '4m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['4m wdir']]['marker']['color'] = solid_color_df['4m wdir_colors'].values
                            for i,test in enumerate(change_log):
                                if change_log[i]['date'] == date and change_log[i]['column']== '4m wdir':
                                    del change_log[i]
                        if column == '4m wdir':
                            ws_original_value = copied_df.at[date, '4m wspd']
                            noqc_original_value =  noqc_df.at[date, '4m wspd']
                            copied_df.at[date, '4m wspd'] = noqc_original_value
                            copied_df.at[date,'4m wspd_colors'] = df.at[date, '4m wspd_colors']
                            ws_solid_pre_change_value = copied_solid_color_df.at[date,'4m wspd_colors']
                            solid_color_df.at[date,'4m wspd_colors'] = ws_solid_pre_change_value
                            if '4m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['4m wspd']]['marker']['color'] = copied_df['4m wspd_colors'].values
                            if '4m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['4m wspd']]['marker']['color'] = solid_color_df['4m wspd_colors'].values
                            for i,test in enumerate(change_log):
                                if change_log[i]['date'] == date and change_log[i]['column']== '4m wspd':
                                    del change_log[i]
                        if column == '7m wspd':
                            wd_original_value = copied_df.at[date, '7m wdir']
                            noqc_original_value =  noqc_df.at[date, '7m wdir']
                            copied_df.at[date, '7m wdir'] = noqc_original_value
                            copied_df.at[date,'7m wdir_colors'] = df.at[date, '7m wdir_colors']
                            wd_solid_pre_change_value = copied_solid_color_df.at[date,'7m wdir_colors']
                            solid_color_df.at[date,'7m wdir_colors'] = wd_solid_pre_change_value
                            if '7m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['7m wdir']]['marker']['color'] = copied_df['7m wdir_colors'].values
                            if '7m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['7m wdir']]['marker']['color'] = solid_color_df['7m wdir_colors'].values
                            for i,test in enumerate(change_log):
                                if change_log[i]['date'] == date and change_log[i]['column']== '7m wdir':
                                    del change_log[i]
                        if column == '7m wdir':
                            ws_original_value = copied_df.at[date, '7m wspd']
                            noqc_original_value =  noqc_df.at[date, '7m wspd']
                            copied_df.at[date, '7m wspd'] = noqc_original_value
                            copied_df.at[date,'7m wspd_colors'] = df.at[date, '7m wspd_colors']
                            ws_solid_pre_change_value = copied_solid_color_df.at[date,'7m wspd_colors']
                            solid_color_df.at[date,'7m wspd_colors'] = ws_solid_pre_change_value
                            if '7m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['7m wspd']]['marker']['color'] = copied_df['7m wspd_colors'].values
                            if '7m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['7m wspd']]['marker']['color'] = solid_color_df['7m wspd_colors'].values
                            for i,test in enumerate(change_log):
                                if change_log[i]['date'] == date and change_log[i]['column']== '7m wspd':
                                    del change_log[i]
                        if column == '15m wspd':
                            wd_original_value = copied_df.at[date, '15m wdir']
                            noqc_original_value =  noqc_df.at[date, '15m wdir']
                            copied_df.at[date, '15m wdir'] = noqc_original_value
                            copied_df.at[date,'15m wdir_colors'] = df.at[date, '15m wdir_colors']
                            wd_solid_pre_change_value = copied_solid_color_df.at[date,'15m wdir_colors']
                            solid_color_df.at[date,'15m wdir_colors'] = wd_solid_pre_change_value
                            if '15m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['15m wdir']]['marker']['color'] = copied_df['15m wdir_colors'].values
                            if '15m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['15m wdir']]['marker']['color'] = solid_color_df['15m wdir_colors'].values
                            for i,test in enumerate(change_log):
                                if change_log[i]['date'] == date and change_log[i]['column']== '15m wdir':
                                    del change_log[i]
                        if column == '15m wdir':
                            ws_original_value = copied_df.at[date, '15m wspd']
                            noqc_original_value =  noqc_df.at[date, '15m wspd']
                            copied_df.at[date, '15m wspd'] = noqc_original_value
                            copied_df.at[date,'15m wspd_colors'] = df.at[date, '15m wspd_colors']
                            ws_solid_pre_change_value = copied_solid_color_df.at[date,'15m wspd_colors']
                            solid_color_df.at[date,'15m wspd_colors'] = ws_solid_pre_change_value
                            if '15m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['15m wspd']]['marker']['color'] = copied_df['15m wspd_colors'].values
                            if '15m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['15m wspd']]['marker']['color'] = solid_color_df['15m wspd_colors'].values
                            for i,test in enumerate(change_log):
                                if change_log[i]['date'] == date and change_log[i]['column']== '15m wspd':
                                    del change_log[i]
                        if column == '30m wspd':
                            wd_original_value = copied_df.at[date, '30m wdir']
                            noqc_original_value =  noqc_df.at[date, '30m wdir']
                            copied_df.at[date, '30m wdir'] = noqc_original_value
                            copied_df.at[date,'30m wdir_colors'] = df.at[date, '30m wdir_colors']
                            wd_solid_pre_change_value = copied_solid_color_df.at[date,'30m wdir_colors']
                            solid_color_df.at[date,'30m wdir_colors'] = wd_solid_pre_change_value
                            if '30m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['30m wdir']]['marker']['color'] = copied_df['30m wdir_colors'].values
                            if '30m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['30m wdir']]['marker']['color'] = solid_color_df['30m wdir_colors'].values
                            for i,test in enumerate(change_log):
                                if change_log[i]['date'] == date and change_log[i]['column']== '30m wdir':
                                    del change_log[i]
                        if column == '30m wdir':
                            ws_original_value = copied_df.at[date, '30m wspd']
                            noqc_original_value =  noqc_df.at[date, '30m wspd']
                            copied_df.at[date, '30m wspd'] = noqc_original_value
                            copied_df.at[date,'30m wspd_colors'] = df.at[date, '30m wspd_colors']
                            ws_solid_pre_change_value = copied_solid_color_df.at[date,'30m wspd_colors']
                            solid_color_df.at[date,'30m wspd_colors'] = ws_solid_pre_change_value
                            if '30m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['30m wspd']]['marker']['color'] = copied_df['30m wspd_colors'].values
                            if '30m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['30m wspd']]['marker']['color'] = solid_color_df['30m wspd_colors'].values
                            for i,test in enumerate(change_log):
                                if change_log[i]['date'] == date and change_log[i]['column']== '30m wspd':
                                    del change_log[i]
                    
                    if np.isnan(original_value) == True: 
                        noqc_original_value = noqc_df.at[date, column]
                        copied_df.at[date, column] = noqc_original_value
                        color_pre_change_value = df.at[date, column+'_noerrorcolor']
                        copied_df.at[date, column+'_colors'] = color_pre_change_value
                        solid_color_df.at[date, column+'_colors'] = df.at[date, column+'_noerrorcolor']
                        if rules == 'Yes':
                            figure['data'][ind_dict[column]]['marker']['color'] = copied_df[column+'_colors'].values
                        elif rules == 'No':
                            figure['data'][ind_dict[column]]['marker']['color'] = solid_color_df[column+'_colors'].values
                        
                        change_log.append({
                            "date": date,
                            "column": column,
                            "original": original_value,
                            "new": noqc_original_value})
                        
                        if column == '1m wspd':
                            wd_original_value = copied_df.at[date, '1m wdir']
                            wd_noqc_original_value =  noqc_df.at[date, '1m wdir']
                            copied_df.at[date, '1m wdir'] = wd_noqc_original_value
                            copied_df.at[date, '1m wdir_colors'] = df.at[date, '1m wdir_noerrorcolor']
                            solid_color_df.at[date, '1m wdir_colors'] = df.at[date, '1m wdir_noerrorcolor']
                            if '1m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['1m wdir']]['marker']['color'] = copied_df['1m wdir_colors'].values
                            if '1m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['1m wdir']]['marker']['color'] = solid_color_df['1m wdir_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '1m wdir',
                                "original": wd_original_value,
                                "new": wd_noqc_original_value})
                        if column == '1m wdir':
                            ws_original_value = copied_df.at[date, '1m wspd']
                            ws_noqc_original_value =  noqc_df.at[date, '1m wspd']
                            copied_df.at[date, '1m wspd'] = ws_noqc_original_value
                            copied_df.at[date, '1m wspd_colors'] = df.at[date, '1m wspd_noerrorcolor']
                            solid_color_df.at[date, '1m wspd_colors'] = df.at[date, '1m wspd_noerrorcolor']
                            if '1m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['1m wspd']]['marker']['color'] = copied_df['1m wspd_colors'].values
                            if '1m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['1m wspd']]['marker']['color'] = solid_color_df['1m wspd_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '1m wspd',
                                "original": ws_original_value,
                                "new": ws_noqc_original_value})
                        if column == '2m wspd':
                            wd_original_value = copied_df.at[date, '2m wdir']
                            wd_noqc_original_value =  noqc_df.at[date, '2m wdir']
                            copied_df.at[date, '2m wdir'] = wd_noqc_original_value
                            copied_df.at[date, '2m wdir_colors'] = df.at[date, '2m wdir_noerrorcolor']
                            solid_color_df.at[date, '2m wdir_colors'] = df.at[date, '2m wdir_noerrorcolor']
                            if '2m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['2m wdir']]['marker']['color'] = copied_df['2m wdir_colors'].values
                            if '2m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['2m wdir']]['marker']['color'] = solid_color_df['2m wdir_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '2m wdir',
                                "original": wd_original_value,
                                "new": wd_noqc_original_value})
                        if column == '2m wdir':
                            ws_original_value = copied_df.at[date, '2m wspd']
                            ws_noqc_original_value =  noqc_df.at[date, '2m wspd']
                            copied_df.at[date, '2m wspd'] = ws_noqc_original_value
                            copied_df.at[date, '2m wspd_colors'] = df.at[date, '2m wspd_noerrorcolor']
                            solid_color_df.at[date, '2m wspd_colors'] = df.at[date, '2m wspd_noerrorcolor']
                            if '2m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['2m wspd']]['marker']['color'] = copied_df['2m wspd_colors'].values
                            if '2m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['2m wspd']]['marker']['color'] = solid_color_df['2m wspd_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '2m wspd',
                                "original": ws_original_value,
                                "new": ws_noqc_original_value})

                        if column == '4m wspd':
                            wd_original_value = copied_df.at[date, '4m wdir']
                            wd_noqc_original_value =  noqc_df.at[date, '4m wdir']
                            copied_df.at[date, '4m wdir'] = wd_noqc_original_value
                            copied_df.at[date, '4m wdir_colors'] = df.at[date, '4m wdir_noerrorcolor']
                            solid_color_df.at[date, '4m wdir_colors'] = df.at[date, '4m wdir_noerrorcolor']
                            if '4m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['4m wdir']]['marker']['color'] = copied_df['4m wdir_colors'].values
                            if '4m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['4m wdir']]['marker']['color'] = solid_color_df['4m wdir_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '4m wdir',
                                "original": wd_original_value,
                                "new": wd_noqc_original_value})
                        if column == '4m wdir':
                            ws_original_value = copied_df.at[date, '4m wspd']
                            ws_noqc_original_value =  noqc_df.at[date, '4m wspd']
                            copied_df.at[date, '4m wspd'] = ws_noqc_original_value
                            copied_df.at[date, '4m wspd_colors'] = df.at[date, '4m wspd_noerrorcolor']
                            solid_color_df.at[date, '4m wspd_colors'] = df.at[date, '4m wspd_noerrorcolor']
                            if '4m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['4m wspd']]['marker']['color'] = copied_df['4m wspd_colors'].values
                            if '4m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['4m wspd']]['marker']['color'] = solid_color_df['4m wspd_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '4m wspd',
                                "original": ws_original_value,
                                "new": ws_noqc_original_value})
                        if column == '7m wspd':
                            wd_original_value = copied_df.at[date, '7m wdir']
                            wd_noqc_original_value =  noqc_df.at[date, '7m wdir']
                            copied_df.at[date, '7m wdir'] = wd_noqc_original_value
                            copied_df.at[date, '7m wdir_colors'] = df.at[date, '7m wdir_noerrorcolor']
                            solid_color_df.at[date, '7m wdir_colors'] = df.at[date, '7m wdir_noerrorcolor']
                            if '7m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['7m wdir']]['marker']['color'] = copied_df['7m wdir_colors'].values
                            if '7m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['7m wdir']]['marker']['color'] = solid_color_df['7m wdir_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '7m wdir',
                                "original": wd_original_value,
                                "new": wd_noqc_original_value})
                        if column == '7m wdir':
                            ws_original_value = copied_df.at[date, '7m wspd']
                            ws_noqc_original_value =  noqc_df.at[date, '7m wspd']
                            copied_df.at[date, '7m wspd'] = ws_noqc_original_value
                            copied_df.at[date, '7m wspd_colors'] = df.at[date, '7m wspd_noerrorcolor']
                            solid_color_df.at[date, '7m wspd_colors'] = df.at[date, '7m wspd_noerrorcolor']
                            if '7m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['7m wspd']]['marker']['color'] = copied_df['7m wspd_colors'].values
                            if '7m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['7m wspd']]['marker']['color'] = solid_color_df['7m wspd_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '7m wspd',
                                "original": ws_original_value,
                                "new": ws_noqc_original_value})
                        if column == '15m wspd':
                            wd_original_value = copied_df.at[date, '15m wdir']
                            wd_noqc_original_value =  noqc_df.at[date, '15m wdir']
                            copied_df.at[date, '15m wdir'] = wd_noqc_original_value
                            copied_df.at[date, '15m wdir_colors'] = df.at[date, '15m wdir_noerrorcolor']
                            solid_color_df.at[date, '15m wdir_colors'] = df.at[date, '15m wdir_noerrorcolor']
                            if '15m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['15m wdir']]['marker']['color'] = copied_df['15m wdir_colors'].values
                            if '15m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['15m wdir']]['marker']['color'] = solid_color_df['15m wdir_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '15m wdir',
                                "original": wd_original_value,
                                "new": wd_noqc_original_value})
                        if column == '15m wdir':
                            ws_original_value = copied_df.at[date, '15m wspd']
                            ws_noqc_original_value =  noqc_df.at[date, '15m wspd']
                            copied_df.at[date, '15m wspd'] = ws_noqc_original_value
                            copied_df.at[date, '15m wspd_colors'] = df.at[date, '15m wspd_noerrorcolor']
                            solid_color_df.at[date, '15m wspd_colors'] = df.at[date, '15m wspd_noerrorcolor']
                            if '15m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['15m wspd']]['marker']['color'] = copied_df['15m wspd_colors'].values
                            if '15m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['15m wspd']]['marker']['color'] = solid_color_df['15m wspd_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '15m wspd',
                                "original": ws_original_value,
                                "new": ws_noqc_original_value})
                        if column == '30m wspd':
                            wd_original_value = copied_df.at[date, '30m wdir']
                            wd_noqc_original_value =  noqc_df.at[date, '30m wdir']
                            copied_df.at[date, '30m wdir'] = wd_noqc_original_value
                            copied_df.at[date, '30m wdir_colors'] = df.at[date, '30m wdir_noerrorcolor']
                            solid_color_df.at[date, '30m wdir_colors'] = df.at[date, '30m wdir_noerrorcolor']
                            if '30m wdir' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['30m wdir']]['marker']['color'] = copied_df['30m wdir_colors'].values
                            if '30m wdir' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['30m wdir']]['marker']['color'] = solid_color_df['30m wdir_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '30m wdir',
                                "original": wd_original_value,
                                "new": wd_noqc_original_value})
                        if column == '30m wdir':
                            ws_original_value = copied_df.at[date, '30m wspd']
                            ws_noqc_original_value =  noqc_df.at[date, '30m wspd']
                            copied_df.at[date, '30m wspd'] = ws_noqc_original_value
                            copied_df.at[date, '30m wspd_colors'] = df.at[date, '30m wspd_noerrorcolor']
                            solid_color_df.at[date, '30m wspd_colors'] = df.at[date, '30m wspd_noerrorcolor']
                            if '30m wspd' in ind_dict.keys() and rules == 'Yes':
                                figure['data'][ind_dict['30m wspd']]['marker']['color'] = copied_df['30m wspd_colors'].values
                            if '30m wspd' in ind_dict.keys() and rules == 'No':
                                figure['data'][ind_dict['30m wspd']]['marker']['color'] = solid_color_df['30m wspd_colors'].values
                            change_log.append({
                                "date": date,
                                "column": '30m wspd',
                                "original": ws_original_value,
                                "new": ws_noqc_original_value})
                    
                elif point in selected_points:
                    selected_points.discard(point)
                    pre_change_value = qc_df.at[date, column]
                    copied_df.at[date, column] = pre_change_value
                    color_pre_change_value = df.at[date,column+'_colors']
                    copied_df.at[date,column+'_colors'] = color_pre_change_value
                    solid_pre_change_value = copied_solid_color_df.at[date,column+'_colors']
                    solid_color_df.at[date,column+'_colors'] = solid_pre_change_value
                    if rules == 'Yes':
                        figure['data'][ind_dict[column]]['marker']['color'] = copied_df[column+'_colors'].values
                    elif rules == 'No':
                        figure['data'][ind_dict[column]]['marker']['color'] = solid_color_df[column+'_colors'].values
                    for i,test in enumerate(change_log):
                        if change_log[i]['date'] == date and change_log[i]['column']== column:
                            del change_log[i]
                    if column == '1m wspd':
                        selected_points.discard(date, '1m wdir')
                        wd_pre_change_value = qc_df.at[date, '1m wdir']
                        copied_df.at[date, '1m wdir'] = wd_pre_change_value
                        wd_color_pre_change_value = df.at[date,'1m wdir_colors']
                        copied_df.at[date,'1m wdir_colors'] = wd_color_pre_change_value
                        solid_pre_change_value = copied_solid_color_df.at[date,'1m wdir_colors']
                        solid_color_df.at[date,'1m wdir_colors'] = solid_pre_change_value
                        if rules == 'No' and '1m wdir' in ind_dict.keys():
                            figure['data'][ind_dict['1m wdir']]['marker']['color'] = solid_color_df['1m wdir_colors'].values
                        if '1m wdir' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['1m wdir']]['marker']['color'] = copied_df['1m wdir_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']=='1m wdir':
                                del change_log[i]
                    if column == '1m wdir':
                        selected_points.discard((date, '1m wspd'))
                        ws_pre_change_value = qc_df.at[date, '1m wspd']
                        copied_df.at[date, '1m wspd'] = ws_pre_change_value
                        ws_color_pre_change_value = df.at[date,'1m wspd_colors']
                        copied_df.at[date,'1m wspd_colors'] = ws_color_pre_change_value
                        solid_pre_change_value = copied_solid_color_df.at[date,'1m wspd_colors']
                        solid_color_df.at[date,'1m wspd_colors'] = solid_pre_change_value
                        
                        if '1m wspd' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['1m wspd']]['marker']['color'] = copied_df['1m wspd_colors'].values
                        if rules == 'No' and '1m wspd' in ind_dict.keys():
                            figure['data'][ind_dict['1m wspd']]['marker']['color'] = solid_color_df['1m wspd_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']== '1m wspd':
                                del change_log[i]

                    if column == '2m wspd':
                        selected_points.discard(date, '2m wdir')
                        wd_pre_change_value = qc_df.at[date, '2m wdir']
                        copied_df.at[date, '2m wdir'] = wd_pre_change_value
                        wd_color_pre_change_value = df.at[date,'2m wdir_colors']
                        copied_df.at[date,'2m wdir_colors'] = wd_color_pre_change_value
                        solid_pre_change_value = copied_solid_color_df.at[date,'2m wdir_colors']
                        solid_color_df.at[date,'2m wdir_colors'] = solid_pre_change_value
                        if rules == 'No' and '2m wdir' in ind_dict.keys():
                            figure['data'][ind_dict['2m wdir']]['marker']['color'] = solid_color_df['2m wdir_colors'].values
                        if '2m wdir' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['2m wdir']]['marker']['color'] = copied_df['2m wdir_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']=='2m wdir':
                                del change_log[i]
                    if column == '2m wdir':
                        selected_points.discard((date, '2m wspd'))
                        ws_pre_change_value = qc_df.at[date, '2m wspd']
                        copied_df.at[date, '2m wspd'] = ws_pre_change_value
                        ws_color_pre_change_value = df.at[date,'2m wspd_colors']
                        copied_df.at[date,'2m wspd_colors'] = ws_color_pre_change_value
                        solid_pre_change_value = copied_solid_color_df.at[date,'2m wspd_colors']
                        solid_color_df.at[date,'2m wspd_colors'] = solid_pre_change_value
                        
                        if '2m wspd' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['2m wspd']]['marker']['color'] = copied_df['2m wspd_colors'].values
                        if rules == 'No' and '2m wspd' in ind_dict.keys():
                            figure['data'][ind_dict['2m wspd']]['marker']['color'] = solid_color_df['2m wspd_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']== '2m wspd':
                                del change_log[i]

                    if column == '4m wspd':
                        selected_points.discard(date, '4m wdir')
                        wd_pre_change_value = qc_df.at[date, '4m wdir']
                        copied_df.at[date, '4m wdir'] = wd_pre_change_value
                        wd_color_pre_change_value = df.at[date,'4m wdir_colors']
                        copied_df.at[date,'4m wdir_colors'] = wd_color_pre_change_value
                        solid_pre_change_value = copied_solid_color_df.at[date,'4m wdir_colors']
                        solid_color_df.at[date,'4m wdir_colors'] = solid_pre_change_value
                        if rules == 'No' and '4m wdir' in ind_dict.keys():
                            figure['data'][ind_dict['4m wdir']]['marker']['color'] = solid_color_df['4m wdir_colors'].values
                        if '4m wdir' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['4m wdir']]['marker']['color'] = copied_df['4m wdir_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']=='4m wdir':
                                del change_log[i]
                    if column == '4m wdir':
                        selected_points.discard((date, '4m wspd'))
                        ws_pre_change_value = qc_df.at[date, '4m wspd']
                        copied_df.at[date, '4m wspd'] = ws_pre_change_value
                        ws_color_pre_change_value = df.at[date,'4m wspd_colors']
                        copied_df.at[date,'4m wspd_colors'] = ws_color_pre_change_value
                        solid_pre_change_value = copied_solid_color_df.at[date,'4m wspd_colors']
                        solid_color_df.at[date,'4m wspd_colors'] = solid_pre_change_value
                        
                        if '4m wspd' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['4m wspd']]['marker']['color'] = copied_df['4m wspd_colors'].values
                        if rules == 'No' and '4m wspd' in ind_dict.keys():
                            figure['data'][ind_dict['4m wspd']]['marker']['color'] = solid_color_df['4m wspd_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']== '4m wspd':
                                del change_log[i]
                    if column == '7m wspd':
                        selected_points.discard((date, '7m wdir'))
                        wd_pre_change_value = qc_df.at[date, '7m wdir']
                        copied_df.at[date, '7m wdir'] = wd_pre_change_value
                        wd_color_pre_change_value = df.at[date,'7m wdir_colors']
                        copied_df.at[date,'7m wdir_colors'] = wd_color_pre_change_value
                        solid_pre_change_value = copied_solid_color_df.at[date,'7m wdir_colors']
                        solid_color_df.at[date,'7m wdir_colors'] = solid_pre_change_value
                        if '7m wdir' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['7m wdir']]['marker']['color'] = copied_df['7m wdir_colors'].values
                        if rules == 'No' and '7m wdir' in ind_dict.keys():
                            figure['data'][ind_dict['7m wdir']]['marker']['color'] = solid_color_df['7m wdir_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']=='7m wdir':
                                del change_log[i]
                    if column == '7m wdir':
                        selected_points.discard(date, '7m wspd')
                        ws_pre_change_value = qc_df.at[date, '7m wspd']
                        copied_df.at[date, '7m wspd'] = ws_pre_change_value
                        ws_color_pre_change_value = df.at[date,'7m wspd_colors']
                        copied_df.at[date,'7m wspd_colors'] = ws_color_pre_change_value
                        solid_pre_change_value = copied_solid_color_df.at[date,'7m wspd_colors']
                        solid_color_df.at[date,'7m wspd_colors'] = solid_pre_change_value
                        if '7m wspd' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['7m wspd']]['marker']['color'] = copied_df['7m wspd_colors'].values
                        if rules == 'No' and '7m wspd' in ind_dict.keys():
                            figure['data'][ind_dict['7m wspd']]['marker']['color'] = solid_color_df['7m wspd_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']== '7m wspd':
                                del change_log[i]
                    if column == '15m wspd':
                        selected_points.discard(date, '15m wdir')
                        wd_pre_change_value = qc_df.at[date, '15m wdir']
                        copied_df.at[date, '15m wdir'] = wd_pre_change_value
                        wd_color_pre_change_value = df.at[date,'15m wdir_colors']
                        copied_df.at[date,'15m wdir_colors'] = wd_color_pre_change_value
                        solid_pre_change_value = copied_solid_color_df.at[date,'15m wdir_colors']
                        solid_color_df.at[date,'15m wdir_colors'] = solid_pre_change_value
                        if '15m wdir' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['15m wdir']]['marker']['color'] = copied_df['15m wdir_colors'].values
                        if rules == 'No' and '15m wdir' in ind_dict.keys():
                            figure['data'][ind_dict['15m wdir']]['marker']['color'] = solid_color_df['15m wdir_colors'].values    
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']=='15m wdir':
                                del change_log[i]
                    if column == '15m wdir':
                        selected_points.discard(date, '15m wspd')
                        ws_pre_change_value = qc_df.at[date, '15m wspd']
                        copied_df.at[date, '15m wspd'] = ws_pre_change_value
                        ws_color_pre_change_value = df.at[date,'15m wspd_colors']
                        copied_df.at[date,'15m wspd_colors'] = ws_color_pre_change_value
                        solid_pre_change_value = copied_solid_color_df.at[date,'15m wspd_colors']
                        solid_color_df.at[date,'15m wspd_colors'] = solid_pre_change_value
                        if '15m wspd' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['15m wspd']]['marker']['color'] = copied_df['15m wspd_colors'].values
                        if rules == 'No' and '15m wspd' in ind_dict.keys():
                            figure['data'][ind_dict['15m wspd']]['marker']['color'] = solid_color_df['15m wspd_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']== '15m wspd':
                                del change_log[i]
                    if column == '30m wspd':
                        selected_points.discard(date, '30m wdir')
                        wd_pre_change_value = qc_df.at[date, '30m wdir']
                        copied_df.at[date, '30m wdir'] = wd_pre_change_value
                        wd_color_pre_change_value = df.at[date,'30m wdir_colors']
                        copied_df.at[date,'30m wdir_colors'] = wd_color_pre_change_value
                        solid_pre_change_value = copied_solid_color_df.at[date,'30m wdir_colors']
                        solid_color_df.at[date,'30m wdir_colors'] = solid_pre_change_value
                        if '30m wdir' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['30m wdir']]['marker']['color'] = copied_df['30m wdir_colors'].values
                        if rules == 'No' and '30m wdir' in ind_dict.keys():
                            figure['data'][ind_dict['30m wdir']]['marker']['color'] = solid_color_df['30m wdir_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']=='30m wdir':
                                del change_log[i]
                    if column == '30m wdir':
                        selected_points.discard(date, '30m wspd')
                        ws_pre_change_value = qc_df.at[date, '30m wspd']
                        copied_df.at[date, '30m wspd'] = ws_pre_change_value
                        ws_color_pre_change_value = df.at[date,'30m wspd_colors']
                        copied_df.at[date,'30m wspd_colors'] = ws_color_pre_change_value
                        solid_pre_change_value = copied_solid_color_df.at[date,'30m wspd_colors']
                        solid_color_df.at[date,'30m wspd_colors'] = solid_pre_change_value
                        if '30m wspd' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['30m wspd']]['marker']['color'] = copied_df['30m wspd_colors'].values
                        if rules == 'No' and '30m wspd' in ind_dict.keys():
                            figure['data'][ind_dict['30m wspd']]['marker']['color'] = solid_color_df['30m wspd_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']== '30m wspd':
                                del change_log[i]
            return ( f"{len(selected_points)} total selected points. ",copied_df.to_dict('records'),change_log,figure)
            
        #return(f"De-select: {date} - {column} reverted to {pre_change_value}", copied_df.to_dict('records'), change_log,figure)
        return("No click data", copied_df.to_dict('records'), change_log,figure)    
    @callback([Output("download-dataframe-csv", "data"),    Output("download-qc-log-csv", "data")],
        Input("save-button", "n_clicks"), allow_duplicate=True,
        prevent_initial_call=True)
    def save_data_csv(n_clicks):
        change_log_df = pd.DataFrame(change_log)  
        aws_abbreviation = closest_date_row['Short_Name'] 
        name = closest_date_row['Name'] 
        
        qc_10min = copied_df.copy()
        q10_bf = qc_10min.bfill(limit=1)   #look at 1 data points before (10min)
        q10_bfff = q10_bf.ffill(limit=1)   #10min after one data point after if there isnt a data point
    
        q10_bfff2 = q10_bfff.bfill(limit=1)     #look at 2 data points before (40min)
        q10_bfff3 = q10_bfff2.ffill(limit=1)   #20min  after (2 data points)
        
        q10_bfff4 = q10_bfff3.bfill(limit=1)    #look at 3 data points before (40min)
        q10_bfff5 = q10_bfff4.ffill(limit=1)   #30min  after (3 data points)
        
        q10_bfff6 = q10_bfff5.bfill(limit=1)    # look at 4 data points before  (40min)
        q10_bfff7 = q10_bfff6.ffill(limit=1)   #40 min  after  (4 data points)
        qc_3hr =q10_bfff6.asfreq('3h')
        qc_1hr =q10_bfff.asfreq('1h')
        
        qc_10min = qc_10min.fillna(444.0)
        qc_1hr = qc_1hr.fillna(444.0)
        qc_3hr = qc_3hr.fillna(444.0)
        
        change_log_df = pd.DataFrame(change_log)  
    
        lat1 = closest_date_row['Lat'] 
        lon1 = closest_date_row['Lon'] 
        
        elev = (closest_date_row['Elevation']).rjust(4, " ")
        lat2 = str(round(float(lat1[:-1]),2)).ljust(5, '0')
        lon2 = str(round(float(lon1[:-1]),2))
        
        lat3 = lat1[-1]
        lon3 = lon1[-1]
        
        lat = (lat2+lat3).rjust(6, ' ') 
        lon = (lon2+lon3).rjust(7, ' ')  
        
        qc_header = "Year: "+str(year)+"  Month: "+str(month)+"  ID: "+aws_abbreviation+"  ARGOS: "+((str(argos_id_input).rjust(5, ' ')))+"  Name: "+name+"\nLat: "+str(lat)+"  Lon: "+str(lon)+"  Elev: "+str(elev)+"m"           
        
        qc_10min['year'] = qc_10min['year'].astype(int)
        qc_10min['month']= qc_10min['month'].astype(int)
        qc_10min['day']= qc_10min['day'].astype(int)
        qc_10min['jday']= qc_10min['jday'].astype(int)
        
        qc_3hr['year'] = qc_3hr['year'].astype(int)
        qc_3hr['month']= qc_3hr['month'].astype(int)
        qc_3hr['day']= qc_3hr['day'].astype(int)
        qc_3hr['jday']= qc_3hr['jday'].astype(int)
        
        qc_1hr['year'] = qc_1hr['year'].astype(int)
        qc_1hr['month']= qc_1hr['month'].astype(int)
        qc_1hr['day']= qc_1hr['day'].astype(int)
        qc_1hr['jday']= qc_1hr['jday'].astype(int)
        
        time_10min = qc_10min.index.astype(str)
        qc_10min['time']  = [x[-8:-3].replace(':','') for x in time_10min]
        
        time_1hr= qc_1hr.index.astype(str)
        qc_1hr['time']  = [x[-8:-3].replace(':','') for x in time_1hr]
        
        time_3hr= qc_3hr.index.astype(str)
        qc_3hr['time']  = [x[-8:-3].replace(':','') for x in time_3hr]
        
        qc_10min = qc_10min[['year','jday','month','day','time','1m temp','2m temp','4m temp','7m temp','15m temp','30m temp','pressure','1m wspd','2m wspd','4m wspd','7m wspd','15m wspd','30m wspd','1m wdir','2m wdir','4m wdir','7m wdir','15m wdir','30m wdir','4m RH','7m RH','15m RH','30m RH']]
        qc_1hr = qc_1hr[['year','jday','month','day','time','1m temp','2m temp','4m temp','7m temp','15m temp','30m temp','pressure','1m wspd','2m wspd','4m wspd','7m wspd','15m wspd','30m wspd','1m wdir','2m wdir','4m wdir','7m wdir','15m wdir','30m wdir','4m RH','7m RH','15m RH','30m RH']]
        qc_3hr = qc_3hr[['year','jday','month','day','time','1m temp','2m temp','4m temp','7m temp','15m temp','30m temp','pressure','1m wspd','2m wspd','4m wspd','7m wspd','15m wspd','30m wspd','1m wdir','2m wdir','4m wdir','7m wdir','15m wdir','30m wdir','4m RH','7m RH','15m RH','30m RH']]
        
        qc_10min = qc_10min.fillna(444.0)
        qc_1hr = qc_1hr.fillna(444.0)
        qc_3hr = qc_3hr.fillna(444.0)
        
        qc_10min['month'] = [str(x).rjust(2,' ') for x in qc_10min['month']]
        qc_10min['day'] = [str(x).rjust(2,' ') for x in qc_10min['day']]
        qc_10min['jday'] = [str(x).rjust(3,' ') for x in qc_10min['jday']]
        qc_10min['time']= [str(x).rjust(4,' ') for x in qc_10min['time']]
        
        qc_10min['1m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['1m temp']]
        qc_10min['2m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['2m temp']]
        qc_10min['4m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['4m temp']]
        qc_10min['7m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['7m temp']]
        qc_10min['15m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['15m temp']]
        qc_10min['30m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['30m temp']]
        qc_10min['pressure']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['pressure']]
        qc_10min['1m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['1m wspd']]
        qc_10min['2m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['2m wspd']]
        qc_10min['4m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['4m wspd']]
        qc_10min['7m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['7m wspd']]
        qc_10min['15m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['15m wspd']]
        qc_10min['30m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['30m wspd']]
        qc_10min['1m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['1m wdir']]
        qc_10min['2m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['2m wdir']]
        qc_10min['4m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['4m wdir']]
        qc_10min['7m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['7m wdir']]
        qc_10min['15m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['15m wdir']]
        qc_10min['30m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['30m wdir']]
        qc_10min['4m RH']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['4m RH']]
        qc_10min['7m RH']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['7m RH']]
        qc_10min['15m RH']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['15m RH']]
        qc_10min['30m RH']= [str(round(float(x),1)).rjust(6,' ') for x in qc_10min['30m RH']]
    
        qc_1hr['month'] = [str(x).rjust(2,' ') for x in qc_1hr['month']]
        qc_1hr['day'] = [str(x).rjust(2,' ') for x in qc_1hr['day']]
        qc_1hr['jday'] = [str(x).rjust(3,' ') for x in qc_1hr['jday']]
        qc_1hr['time']= [str(x).rjust(4,' ') for x in qc_1hr['time']]
        
        qc_1hr['1m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['1m temp']]
        qc_1hr['2m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['2m temp']]
        qc_1hr['4m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['4m temp']]
        qc_1hr['7m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['7m temp']]
        qc_1hr['15m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['15m temp']]
        qc_1hr['30m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['30m temp']]
        qc_1hr['pressure']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['pressure']]
        qc_1hr['1m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['1m wspd']]
        qc_1hr['2m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['2m wspd']]
        qc_1hr['4m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['4m wspd']]
        qc_1hr['7m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['7m wspd']]
        qc_1hr['15m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['15m wspd']]
        qc_1hr['30m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['30m wspd']]
        qc_1hr['1m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['1m wdir']]
        qc_1hr['2m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['2m wdir']]
        qc_1hr['4m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['4m wdir']]
        qc_1hr['7m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['7m wdir']]
        qc_1hr['15m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['15m wdir']]
        qc_1hr['30m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['30m wdir']]
        qc_1hr['4m RH']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['4m RH']]
        qc_1hr['7m RH']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['7m RH']]
        qc_1hr['15m RH']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['15m RH']]
        qc_1hr['30m RH']= [str(round(float(x),1)).rjust(6,' ') for x in qc_1hr['30m RH']]
        
        qc_3hr['month'] = [str(x).rjust(2,' ') for x in qc_3hr['month']]
        qc_3hr['day'] = [str(x).rjust(2,' ') for x in qc_3hr['day']]
        qc_3hr['jday'] = [str(x).rjust(3,' ') for x in qc_3hr['jday']]
        qc_3hr['time']= [str(x).rjust(4,' ') for x in qc_3hr['time']]
        
        qc_3hr['1m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['1m temp']]
        qc_3hr['2m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['2m temp']]
        qc_3hr['4m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['4m temp']]
        qc_3hr['7m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['7m temp']]
        qc_3hr['15m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['15m temp']]
        qc_3hr['30m temp']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['30m temp']]
        qc_3hr['pressure']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['pressure']]
        qc_3hr['1m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['1m wspd']]
        qc_3hr['2m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['2m wspd']]
        qc_3hr['4m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['4m wspd']]
        qc_3hr['7m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['7m wspd']]
        qc_3hr['15m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['15m wspd']]
        qc_3hr['30m wspd']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['30m wspd']]
        qc_3hr['1m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['1m wdir']]
        qc_3hr['2m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['2m wdir']]
        qc_3hr['4m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['4m wdir']]
        qc_3hr['7m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['7m wdir']]
        qc_3hr['15m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['15m wdir']]
        qc_3hr['30m wdir']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['30m wdir']]
        qc_3hr['4m RH']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['4m RH']]
        qc_3hr['7m RH']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['7m RH']]
        qc_3hr['15m RH']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['15m RH']]
        qc_3hr['30m RH']= [str(round(float(x),1)).rjust(6,' ') for x in qc_3hr['30m RH']]

        deltaT_3hr = (round((qc_3hr['4m temp'].astype(float) -  qc_3hr['1m temp'].astype(float)),1)).astype(str)
        deltaT_1hr = (round((qc_1hr['4m temp'].astype(float) -  qc_1hr['1m temp'].astype(float)),1)).astype(str)
        deltaT_10min = (round((qc_10min['4m temp'].astype(float) -  qc_10min['1m temp'].astype(float)),1)).astype(str)

        qc_3hr_std = qc_3hr[['year','jday','month','day','time','4m temp','pressure','4m wspd','4m wdir','4m RH']]
        qc_3hr_std['deltaT'] = deltaT_3hr
        qc_1hr_std = qc_1hr[['year','jday','month','day','time','4m temp','pressure','4m wspd','4m wdir','4m RH']]
        qc_1hr_std['deltaT'] = deltaT_1hr
        qc_10min_std = qc_10min[['year','jday','month','day','time','4m temp','pressure','4m wspd','4m wdir','4m RH']]
        qc_10min_std['deltaT'] = deltaT_10min
            
        number_of_rows = len(qc_10min)
        number_of_days = qc_10min['day'].iloc[-1]
        raw_header = aws_abbreviation+"  "+str(argos_id)+"  "+str(name)+"                "+str(lat)+"   "+str(lon)+"    "+str(elev)+"  "+str(year)+"   "+str(month)+"  "+str(number_of_days)+"  "+str(number_of_rows)+"            RH       delta-T"
        dat_header = '  '+str(month)+'  '+str(year_abv)+'   Station : '+str(argos_id)+'  '+str(name)+'\n  Lat : '+str(lat)+'  Long : '+str(lon)+'  Elev : '+str(elev)+' M'
    
        raw_file_df = qc_10min.copy()
    
        raw_file_df['1m temp_man_qc'] = df['1m temp_man_qc']
        raw_file_df['2m temp_man_qc'] = df['1m temp_man_qc']
        raw_file_df['4m temp_man_qc'] = df['1m temp_man_qc']
        raw_file_df['7m temp_man_qc'] = df['1m temp_man_qc']
        raw_file_df['15m temp_man_qc'] = df['1m temp_man_qc']
        raw_file_df['30m temp_man_qc'] = df['1m temp_man_qc']
        
        raw_file_df['pressure_man_qc'] = df['pressure_man_qc']
        raw_file_df['1m wdir_man_qc'] = df['1m wdir_man_qc']
        raw_file_df['2m wdir_man_qc'] = df['2m wdir_man_qc']
        raw_file_df['4m wdir_man_qc'] = df['4m wdir_man_qc']
        raw_file_df['7m wdir_man_qc'] = df['7m wdir_man_qc']
        raw_file_df['15m wdir_man_qc'] = df['15m wdir_man_qc']
        raw_file_df['30m wdir_man_qc'] = df['30m wdir_man_qc']
        
        raw_file_df['1m wspd_man_qc'] = df['1m wspd_man_qc']
        raw_file_df['2m wspd_man_qc'] = df['2m wspd_man_qc']
        raw_file_df['7m wspd_man_qc'] = df['7m wspd_man_qc']
        raw_file_df['15m wspd_man_qc'] = df['15m wspd_man_qc']
        raw_file_df['4m wspd_man_qc'] = df['4m wspd_man_qc']
        raw_file_df['30m wspd_man_qc'] = df['30m wspd_man_qc']
        raw_file_df['7m RH_man_qc'] = df['7m RH_man_qc']
        raw_file_df['30m RH_man_qc'] = df['30m RH_man_qc']
        raw_file_df['4m RH_man_qc'] = df['4m RH_man_qc']
        raw_file_df['15m RH_man_qc'] = df['15m RH_man_qc']
        
        for row in change_log_df.itertuples():
            datetime = row[1]
            variable = row[2]
            value = row[3]
            raw_file_df.loc[datetime,variable+'_man_qc'] = value 
            
        q1h_output_path = base_path + all_filenames.loc['q1h_output_path'].values[0] %(short_name,year,month)
        q3h_output_path = base_path + all_filenames.loc['q3h_output_path'].values[0] %(short_name,year,month)
        q10_output_path = base_path + all_filenames.loc['q10_output_path'].values[0] %(short_name,year,month)
        raw_output_path = base_path + all_filenames.loc['raw_output_path'].values[0] %(short_name,year,month)
        dat_output_path = base_path + all_filenames.loc['dat_output_path'].values[0] %(argos_id[2:],month,year_abv)
        
        tt_q1h_all_output_path = base_path + all_filenames.loc['tt_q1h_all_output_path'].values[0] %(short_name,year,month)
        tt_q3h_all_output_path = base_path + all_filenames.loc['tt_q3h_all_output_path'].values[0] %(short_name,year,month)
        tt_q10_all_output_path = base_path + all_filenames.loc['tt_q10_all_output_path'].values[0] %(short_name,year,month)
        tt_dat_all_output_path = base_path + all_filenames.loc['tt_dat_all_output_path'].values[0] %(argos_id[2:],month,year_abv)
        
        len_temp1_qc = len(raw_file_df['1m temp_man_qc'].dropna())
        len_temp2_qc = len(raw_file_df['2m temp_man_qc'].dropna())
        len_temp4_qc = len(raw_file_df['4m temp_man_qc'].dropna())
        len_temp7_qc = len(raw_file_df['7m temp_man_qc'].dropna())
        len_temp15_qc = len(raw_file_df['15m temp_man_qc'].dropna())
        len_temp30_qc = len(raw_file_df['30m temp_man_qc'].dropna())
        
        len_pres_qc =len(raw_file_df['pressure_man_qc'].dropna())
        len_wspd1_qc = len(raw_file_df['1m wspd_man_qc'].dropna())
        len_wspd2_qc = len(raw_file_df['2m wspd_man_qc'].dropna())
        len_wspd4_qc = len(raw_file_df['4m wspd_man_qc'].dropna())
        len_wspd7_qc = len(raw_file_df['7m wspd_man_qc'].dropna())
        len_wspd15_qc = len(raw_file_df['15m wspd_man_qc'].dropna())
        len_wspd30_qc = len(raw_file_df['30m wspd_man_qc'].dropna())
        len_wdir1_qc =len(raw_file_df['1m wdir_man_qc'].dropna())
        len_wdir2_qc =len(raw_file_df['2m wdir_man_qc'].dropna())
        len_wdir4_qc =len(raw_file_df['4m wdir_man_qc'].dropna())
        len_wdir7_qc =len(raw_file_df['7m wdir_man_qc'].dropna())
        len_wdir15_qc =len(raw_file_df['15m wdir_man_qc'].dropna())
        len_wdir30_qc =len(raw_file_df['30m wdir_man_qc'].dropna())
        
        len_rh4_qc =len(raw_file_df['4m RH_man_qc'].dropna())
        len_rh7_qc =len(raw_file_df['7m RH_man_qc'].dropna())
        len_rh15_qc =len(raw_file_df['15m RH_man_qc'].dropna())
        len_rh30_qc =len(raw_file_df['30m RH_man_qc'].dropna())
        
        
        raw_file_df['1m temp_rules'] = df['1m temp_rules']
        raw_file_df['2m temp_rules'] = df['2m temp_rules']
        raw_file_df['4m temp_rules'] = df['4m temp_rules']
        raw_file_df['7m temp_rules'] = df['7m temp_rules']
        raw_file_df['15m temp_rules'] = df['15m temp_rules']
        raw_file_df['30m temp_rules'] = df['30m temp_rules']
        raw_file_df['pressure_rules'] = df['pressure_rules']
        raw_file_df['1m wspd_rules'] = df['1m wspd_rules']
        raw_file_df['2m wspd_rules'] = df['2m wspd_rules']
        raw_file_df['4m wspd_rules'] =df['4m wspd_rules']
        raw_file_df['7m wspd_rules'] = df['7m wspd_rules']
        raw_file_df['15m wspd_rules'] = df['15m wspd_rules']
        raw_file_df['30m wspd_rules'] = df['30m wspd_rules']
        raw_file_df['1m wdir_rules'] = df['1m wdir_rules']
        raw_file_df['2m wdir_rules'] = df['2m wdir_rules']
        raw_file_df['4m wdir_rules'] = df['4m wdir_rules']
        raw_file_df['7m wdir_rules'] = df['7m wdir_rules']
        raw_file_df['15m wdir_rules'] = df['15m wdir_rules']
        raw_file_df['30m wdir_rules'] = df['30m wdir_rules']
        raw_file_df['4m RH_rules'] = df['4m RH_rules']
        raw_file_df['7m RH_rules'] = df['7m RH_rules']
        raw_file_df['15m RH_rules'] = df['15m RH_rules']
        raw_file_df['30m RH_rules'] = df['30m RH_rules']

        
        len_temp1_rules = len(raw_file_df['1m temp_rules'].dropna())
        len_temp2_rules = len(raw_file_df['2m temp_rules'].dropna())
        len_temp4_rules = len(raw_file_df['4m temp_rules'].dropna())
        len_temp7_rules = len(raw_file_df['7m temp_rules'].dropna())
        len_temp15_rules = len(raw_file_df['15m temp_rules'].dropna())
        len_temp30_rules = len(raw_file_df['30m temp_rules'].dropna())
        len_pres_rules =len(raw_file_df['pressure_rules'].dropna())
        len_wspd1_rules = len(raw_file_df['1m wspd_rules'].dropna())
        len_wspd2_rules = len(raw_file_df['2m wspd_rules'].dropna())
        len_wspd4_rules = len(raw_file_df['4m wspd_rules'].dropna())
        len_wspd7_rules = len(raw_file_df['7m wspd_rules'].dropna())
        len_wspd15_rules = len(raw_file_df['15m wspd_rules'].dropna())
        len_wspd30_rules = len(raw_file_df['30m wspd_rules'].dropna())
        len_wdir1_rules =len(raw_file_df['1m wdir_rules'].dropna())
        len_wdir2_rules =len(raw_file_df['2m wdir_rules'].dropna())
        len_wdir4_rules =len(raw_file_df['4m wdir_rules'].dropna())
        len_wdir7_rules =len(raw_file_df['7m wdir_rules'].dropna())
        len_wdir15_rules =len(raw_file_df['15m wdir_rules'].dropna())
        len_wdir30_rules =len(raw_file_df['30m wdir_rules'].dropna())
        len_rh4_rules =len(raw_file_df['4m RH_rules'].dropna())
        len_rh7_rules =len(raw_file_df['7m RH_rules'].dropna())
        len_rh15_rules =len(raw_file_df['15m RH_rules'].dropna())
        len_rh30_rules =len(raw_file_df['30m RH_rules'].dropna())
        raw_file_df=raw_file_df.fillna(444.0)

        for col in raw_file_df.columns:
            #print(col)
            if col[-6:] == 'man_qc':
                raw_file_df[col] = raw_file_df[col].astype(str).str.rjust(6,' ')
            if col[-5:] == 'rules':
                raw_file_df[col] = raw_file_df[col].astype(str).str.rjust(6,' ')
        raw_header_counter =str(len_temp1_qc).rjust(6,' ')+str(len_temp1_rules).rjust(6,' ')+'\n'+str(len_temp2_qc).rjust(6,' ')+str(len_temp2_rules).rjust(6,' ')+'\n'+str(len_temp4_qc).rjust(6,' ')+str(len_temp4_rules).rjust(6,' ')+'\n'+str(len_temp7_qc).rjust(6,' ')+str(len_temp7_rules).rjust(6,' ')+'\n'+str(len_temp15_qc).rjust(6,' ')+str(len_temp15_rules).rjust(6,' ')+'\n'+str(len_temp30_qc).rjust(6,' ')+str(len_temp30_rules).rjust(6,' ')+'\n'+str(len_pres_qc).rjust(6,' ')+str(len_pres_rules).rjust(6,' ')+'\n'+str(len_wspd1_qc).rjust(6,' ')+str(len_wspd1_rules).rjust(6,' ')+'\n'+str(len_wspd2_qc).rjust(6,' ')+str(len_wspd2_rules).rjust(6,' ')+'\n'+str(len_wspd4_qc).rjust(6,' ')+str(len_wspd4_rules).rjust(6,' ')+'\n'+str(len_wspd7_qc).rjust(6,' ')+str(len_wspd7_rules).rjust(6,' ')+'\n'+str(len_wspd15_qc).rjust(6,' ')+str(len_wspd15_rules).rjust(6,' ')+'\n'+str(len_wspd30_qc).rjust(6,' ')+str(len_wspd30_rules).rjust(6,' ')+'\n'+str(len_wdir1_qc).rjust(6,' ')+str(len_wdir1_rules).rjust(6,' ')+'\n'+str(len_wdir2_qc).rjust(6,' ')+str(len_wdir2_rules).rjust(6,' ')+'\n'+str(len_wdir4_qc).rjust(6,' ')+str(len_wdir4_rules).rjust(6,' ')+'\n'+str(len_wdir7_qc).rjust(6,' ')+str(len_wdir7_rules).rjust(6,' ')+'\n'+str(len_wdir15_qc).rjust(6,' ')+str(len_wdir15_rules).rjust(6,' ')+'\n'+str(len_wdir30_qc).rjust(6,' ')+str(len_wdir30_rules).rjust(6,' ')+'\n'+str(len_rh4_qc).rjust(6,' ')+str(len_rh4_rules).rjust(6,' ')+'\n'+str(len_rh7_qc).rjust(6,' ')+str(len_rh7_rules).rjust(6,' ')+'\n'+str(len_rh15_qc).rjust(6,' ')+str(len_rh15_rules).rjust(6,' ')+'\n'+str(len_rh30_qc).rjust(6,' ')+str(len_rh30_rules).rjust(6,' ')          
        dat_file_df = (qc_3hr.copy())[['1m temp','2m temp','4m temp','7m temp','15m temp','30m temp','pressure','1m wspd','2m wspd','4m wspd','7m wspd','15m wspd','30m wspd','1m wdir','2m wdir','4m wdir','7m wdir','15m wdir','30m wdir','4m RH','7m RH','15m RH','30m RH']]
        dat_file_df_std = (qc_3hr.copy())[['4m temp','pressure','4m wspd','4m wdir','4m RH']]
        raw_file_df=raw_file_df[['year','jday','month','day','time','1m temp','1m temp_man_qc','1m temp_rules','2m temp','2m temp_man_qc','2m temp_rules','4m temp','4m temp_man_qc','4m temp_rules','7m temp','7m temp_man_qc','7m temp_rules','15m temp','15m temp_man_qc','15m temp_rules','30m temp','30m temp_man_qc','30m temp_rules','pressure','pressure_man_qc','pressure_rules','1m wspd','1m wspd_man_qc','1m wspd_rules','2m wspd','2m wspd_man_qc','2m wspd_rules','4m wspd','4m wspd_man_qc','4m wspd_rules','7m wspd','7m wspd_man_qc','7m wspd_rules','15m wspd','15m wspd_man_qc','15m wspd_rules','30m wspd','30m wspd_man_qc','30m wspd_rules','1m wdir','1m wdir_man_qc','1m wdir_rules','2m wdir','2m wdir_man_qc','2m wdir_rules','4m wdir','4m wdir_man_qc','4m wdir_rules','7m wdir','7m wdir_man_qc','7m wdir_rules','15m wdir','15m wdir_man_qc','15m wdir_rules','30m wdir','30m wdir_man_qc','30m wdir_rules','4m RH','4m RH_man_qc','4m RH_rules','7m RH','7m RH_man_qc','7m RH_rules','15m RH','15m RH_man_qc','15m RH_rules','30m RH','30m RH_man_qc','30m RH_rules']]
        qc_10min = qc_10min[['year','jday','month','day','time','1m temp','2m temp','4m temp','7m temp','15m temp','30m temp','pressure','1m wspd','2m wspd','4m wspd','7m wspd','15m wspd','30m wspd','1m wdir','2m wdir','4m wdir','7m wdir','15m wdir','30m wdir','4m RH','7m RH','15m RH','30m RH']]
        #raw_file_df.fillna(444.0,inplace=True)
        std_qc_10min=qc_10min[['year','jday','month','day','time','4m temp','pressure','4m wspd','4m wdir','4m RH']]
        std_qc_1hr=qc_1hr[['year','jday','month','day','time','4m temp','pressure','4m wspd','4m wdir','4m RH']]
        std_qc_3hr=qc_3hr[['year','jday','month','day','time','4m temp','pressure','4m wspd','4m wdir','4m RH']]
                
        #with open(raw_output_path.iloc[0], "w") as f:
        with open(raw_output_path, "w") as f:
            # Write the header
            f.write("".join(raw_header) + "\n")
            f.write("".join(raw_header_counter) + "\n")
            # Write each row
            for row in raw_file_df.itertuples(index=True, name=None):
                f.write(" ".join(map(str, row)) + "\n")
        with open(q3h_output_path, "w") as f:
            # Write the header
            f.write("".join(qc_header) + "\n")
            # Write each row
            for row in qc_3hr_std.itertuples(index=False, name=None):
                f.write(" ".join(map(str, row)) + "\n")
        with open(q1h_output_path, "w") as f:
            # Write the header
            f.write("".join(qc_header) + "\n")
            # Write each row
            for row in qc_1hr_std.itertuples(index=False, name=None):
                f.write(" ".join(map(str, row)) + "\n")
        with open(q10_output_path, "w") as f:
            # Write the header
            f.write("".join(qc_header) + "\n")
            # Write each row
            for row in qc_10min_std.itertuples(index=False, name=None):
                f.write(" ".join(map(str, row)) + "\n")
        with open(tt_q3h_all_output_path, "w") as f:
            # Write the header
            f.write("".join(qc_header) + "\n")
            # Write each row
            for row in qc_3hr.itertuples(index=False, name=None):
                f.write(" ".join(map(str, row)) + "\n")
        with open(tt_q1h_all_output_path, "w") as f:
            # Write the header
            f.write("".join(qc_header) + "\n")
            # Write each row
            for row in qc_1hr.itertuples(index=False, name=None):
                f.write(" ".join(map(str, row)) + "\n")
        with open(tt_q10_all_output_path, "w") as f:
            # Write the header
            f.write("".join(qc_header) + "\n")
            # Write each row
            for row in qc_10min.itertuples(index=False, name=None):
                f.write(" ".join(map(str, row)) + "\n")      
        with open(dat_output_path, "w") as f:
            # Write the header
            f.write("".join(dat_header) + "\n")
            # Write each row
            for row in dat_file_df.itertuples(index=True, name=None):
                f.write(" ".join(map(str, row)) + "\n")
        with open(tt_dat_all_output_path, "w") as f:
            # Write the header
            f.write("".join(dat_header) + "\n")
            # Write each row
            for row in dat_file_df_std.itertuples(index=True, name=None):
                f.write(" ".join(map(str, row)) + "\n")                  
        return(dcc.send_data_frame(copied_df.to_csv , qc_csv_output_path),
        dcc.send_data_frame(change_log_df.to_csv, change_log_output_path))

if __name__ == '__main__':
    app.run(port=8050)
    #app.run(port=8050,debug=True)
    #app.run(debug=True,jupyter_mode="tab",port=8050)

