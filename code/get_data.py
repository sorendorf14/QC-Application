#!/usr/bin/python
#
#
########################################################################
# FILENAME: get_data.py                                        Mar. 2026
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
from dash.exceptions import PreventUpdate
from pathlib import Path
import plotly.graph_objects as go 
import plotly 
from plotly.subplots import make_subplots 
import numpy as np 
import pandas as pd 
from dash import dcc, html, Input, Output, dash_table, callback, Dash, State 
import dash 
import plotly.express as px
import datetime as dt
from datetime import datetime, timedelta #import cal_file_setup #from cal_file_setup import df import csv import datetime as dt
import os, glob
import cal_file_setup
from cal_file_setup import cal_df, all_filenames

#setting flask setting to only display output in terminal when there is an error
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

base_path = all_filenames.loc['base_path'].values[0] 
#base_path = all_filenames.loc['base_path'].values[0] %(year)

if argos_id[0] == '0':
    argos_id_input = argos_id[1:]
else:
    pass

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
    
df = pd.read_csv(dotr_path,sep='\s+',skiprows=2,na_values=['444.0',444.0,'444'],names=['Jday','Time','temp','pres','wspd','wdir','RH','deltaT'])
dot10_df = pd.read_csv(dot10_path,sep='\s+',na_values=['444.0',444.0,'444'],dtype='str',usecols=[1,2,4,10],names=['Jday','Time','panel_temp','voltage']) 
df['year']=year
df['Jday_rjust'] = [str(x).rjust(3,'0') for x in df['Jday']]
df['year_jdate'] = df['year']+df['Jday_rjust']
df['date'] = pd.to_datetime(df['year_jdate'] ,format='%Y%j')
# Step 4: Map Time to time offsets
df['time'] = (df['Time'] - 1) * pd.Timedelta(minutes=10)
# Step 5: Combine date and time into datetime
df['datetime'] = df['date'] + df['time']
time = df['datetime'].astype(str)
time_list = [x[-8:-3].replace(':','') for x in time]
df['time'] = time_list

day_list = [x.day for x in df['datetime']]
month_list = [x.month for x in df['datetime']]
df['month']= month_list
df['day']= day_list
df= df[['datetime','year','Jday','month','day','time','temp','pres','wspd','wdir','RH','deltaT','year_jdate','date']]
df=df.set_index('datetime')

dot10_df['year']=year
dot10_df['Jday_rjust'] = [str(x).rjust(3,'0') for x in dot10_df['Jday']]
dot10_df['year_jdate'] = dot10_df['year']+dot10_df['Jday_rjust']
dot10_df['date'] = (pd.to_datetime(dot10_df['year_jdate'] ,format='%Y%j')).astype(str)
dot10_df['datetime'] = dot10_df['date'] + " " +dot10_df['Time']
dot10_df['datetime'] = pd.to_datetime(dot10_df['datetime'])
dot10_df = dot10_df.set_index('datetime')

df['voltage'] = dot10_df['voltage']
df['panel_temp'] = dot10_df['panel_temp']

if qc_type == 'prev' or qc_type == 'both':
    prev_month_df = pd.read_csv(prev_month_dotr_path,sep='\s+',skiprows=2,na_values=['444.0',444.0,'444'],names=['Jday','Time','temp','pres','wspd','wdir','RH','deltaT'])
    prev_month_df['year']=prev_year
    prev_month_df['Jday_rjust'] = [str(x).rjust(3,'0') for x in prev_month_df['Jday']]
    prev_month_df['year_jdate'] = prev_month_df['year']+prev_month_df['Jday_rjust']
    prev_month_df['date'] = pd.to_datetime(prev_month_df['year_jdate'] ,format='%Y%j')
    prev_month_df['time'] = (prev_month_df['Time'] - 1) * pd.Timedelta(minutes=10)
    prev_month_dot10_df = pd.read_csv(prev_month_dot10_path,dtype='str',sep='\s+',na_values=['444.0',444.0,'444'],usecols=[1,2,4,10],names=['Jday','Time','panel_temp','voltage'])  
    prev_month_df['datetime'] = prev_month_df['date'] + prev_month_df['time']
    prev_month_time = prev_month_df['datetime'].astype(str)
    prev_month_time_list = [x[-8:-3].replace(':','') for x in prev_month_time]
    prev_month_df['time'] = prev_month_time_list
    prev_month_original_df = prev_month_df.copy()
    first_day = df.index[0]
    three_days_ago = df.index[0] - timedelta(days=3)
    prev_month_df = prev_month_df.set_index('datetime')
    prev_month_dot10_df['year']=year
    prev_month_dot10_df['Jday_rjust'] = [str(x).rjust(3,'0') for x in prev_month_dot10_df['Jday']]
    prev_month_dot10_df['year_jdate'] = prev_month_dot10_df['year']+prev_month_dot10_df['Jday_rjust']
    prev_month_dot10_df['date'] = (pd.to_datetime(prev_month_dot10_df['year_jdate'] ,format='%Y%j')).astype(str)
    prev_month_dot10_df['datetime'] = prev_month_dot10_df['date'] + " " +prev_month_dot10_df['Time']
    prev_month_dot10_df['datetime'] = pd.to_datetime(prev_month_dot10_df['datetime'])
    prev_month_dot10_df = prev_month_dot10_df.set_index('datetime')
    prev_month_df['panel_temp'] = prev_month_dot10_df['panel_temp']
    prev_month_df['voltage'] = prev_month_dot10_df['voltage']
    last_days_df = prev_month_df.loc[three_days_ago:first_day]
    last_days_dot10_df = prev_month_dot10_df.loc[three_days_ago:first_day]
    cat_df = pd.concat([ last_days_df, df])
    
if qc_type == "both" or qc_type == 'next':
    next_month_df = pd.read_csv(next_month_dotr_path,sep='\s+',skiprows=2,na_values=['444.0',444.0,'444'],names=['Jday','Time','temp','pres','wspd','wdir','RH','deltaT'])
    next_month_dot10_df = pd.read_csv(next_month_dot10_path,sep='\s+',na_values=['444.0',444.0,'444'],dtype='str',usecols=[1,2,4,10],names=['Jday','Time','panel_temp','voltage']) 

    next_month_df['year']=next_year
    next_month_df['Jday_rjust'] = [str(x).rjust(3,'0') for x in next_month_df['Jday']]
    next_month_df['year_jdate'] = next_month_df['year']+next_month_df['Jday_rjust']
    next_month_df['date'] = pd.to_datetime(next_month_df['year_jdate'] ,format='%Y%j')
    next_month_df['time'] = (next_month_df['Time'] - 1) * pd.Timedelta(minutes=10)
    next_month_df['datetime'] = next_month_df['date'] + next_month_df['time']
    next_month_time = next_month_df['datetime'].astype(str)
    next_month_time_list = [x[-8:-3].replace(':','') for x in next_month_time]
    next_month_df['time'] = next_month_time_list
   
    next_month_df = next_month_df.set_index('datetime')
    next_month_original_df = next_month_df.copy()
    first_day = next_month_df.index[0]
    next_three_days = next_month_df.index[0] + timedelta(days=3)

    next_month_dot10_df['year']=next_year
    next_month_dot10_df['Jday_rjust'] = [str(x).rjust(3,'0') for x in next_month_dot10_df['Jday']]
    next_month_dot10_df['year_jdate'] = next_month_dot10_df['year']+next_month_dot10_df['Jday_rjust']
    next_month_dot10_df['date'] = (pd.to_datetime(next_month_dot10_df['year_jdate'] ,format='%Y%j')).astype(str)
    next_month_dot10_df['datetime'] = next_month_dot10_df['date'] + " " +next_month_dot10_df['Time']
    next_month_dot10_df['datetime'] = pd.to_datetime(next_month_dot10_df['datetime'])
    next_month_dot10_df = next_month_dot10_df.set_index('datetime')
    next_month_df['voltage'] = next_month_dot10_df['voltage']
    next_month_df['panel_temp'] = next_month_dot10_df['panel_temp']

    next_few_days_df = next_month_df.loc[first_day:next_three_days]
    next_few_days_dot10_df = next_month_dot10_df.loc[first_day:next_three_days]
    if qc_type == 'both':
        cat_df = pd.concat([cat_df, next_few_days_df])
    if qc_type == 'next':
        cat_df = pd.concat([df, next_few_days_df])

test_df = df.copy() 

num_consecutive = 54 
temp_prev_dif=((test_df['temp'].interpolate(method='nearest',limit=1,)).diff()).reindex(df.index) #.fillna(444.0)
temp_next_dif=((test_df['temp'].interpolate(method='nearest',limit=1)).diff(periods=-1)).reindex(df.index) #.fillna(444.0) ,limit=100
wdir_prev_dif=(test_df['wdir'].interpolate(method='nearest',limit=1).diff()).reindex(df.index)
wdir_next_dif=(test_df['wdir'].interpolate(method='nearest',limit=1).diff(periods=-1)).reindex(df.index)
pres_prev_dif=(test_df['pres'].interpolate(method='nearest',limit=1).diff()).reindex(df.index)
pres_next_dif=(test_df['pres'].interpolate(method='nearest',limit=1).diff(periods=-1)).reindex(df.index)
wspd_prev_dif=(test_df['wspd'].interpolate(method='nearest',limit=1).diff()).reindex(df.index)
wspd_next_dif=(test_df['wspd'].interpolate(method='nearest',limit=1).diff(periods=-1)).reindex(df.index)
rh_prev_dif=(test_df['RH'].interpolate(method='nearest',limit=1).diff()).reindex(df.index)
rh_next_dif=(test_df['RH'].interpolate(method='nearest',limit=1).diff(periods=-1)).reindex(df.index)
deltaT_prev_dif=(test_df['deltaT'].interpolate(method='nearest',limit=1).diff()).reindex(df.index)
deltaT_next_dif=(test_df['deltaT'].interpolate(method='nearest',limit=1).diff(periods=-1)).reindex(df.index)

temp_conditional=(abs(temp_prev_dif)>2.) & (abs(temp_next_dif)>2.)  
wspd_conditional= (abs(wspd_prev_dif)>10) | (abs(wspd_next_dif)>10)
deltaT_conditional=(abs(deltaT_prev_dif)>4) & (abs(deltaT_next_dif)>4)
pres_conditional=(abs(pres_prev_dif)>1) | (abs(pres_next_dif)>1)
wdir_conditional=  ((abs(wdir_prev_dif)>100) & (abs(wdir_next_dif)>100)) & (abs(wdir_next_dif)<260) & (abs(wdir_prev_dif) <260) 
rh_conditional=(abs(rh_prev_dif)>5) & (abs(rh_next_dif)>5)

temp_colors = np.where(temp_conditional,'magenta','black').tolist()
pres_colors = np.where(pres_conditional,'magenta','black').tolist()
deltaT_colors = np.where(deltaT_conditional,'magenta','black').tolist()
RH_colors = np.where(rh_conditional,'magenta','black').tolist()

df['wd_streak'] = df['wdir'].ne(df['wdir'].shift()).cumsum()
df['wd_count'] = df.groupby('wd_streak').cumcount() + 1
df['wd_is_repeated'] = df['wd_count'] >= num_consecutive
df['wd_is_repeated'] = df.groupby('wd_streak')['wd_is_repeated'].transform('max')

df['ws_streak'] = df['wspd'].ne(df['wspd'].shift()).cumsum()
df['ws_count'] = df.groupby('ws_streak').cumcount() + 1
df['ws_is_repeated'] = df['ws_count'] >= num_consecutive
df['ws_is_repeated'] = df.groupby('ws_streak')['ws_is_repeated'].transform('max')

wspd_colors = np.where(( wspd_conditional | df['ws_is_repeated'] | df['wd_is_repeated'] | wdir_conditional),'magenta','black').tolist()
wdir_colors = np.where((df['wd_is_repeated'] | wdir_conditional | df['ws_is_repeated'] | wspd_conditional), 'magenta', 'black').tolist()

voltage_colors = ['black' for x in range(len(df))]
panel_temp_colors = ['darkseagreen' for x in range(len(df))]
df['temp_colors']=temp_colors
df['pres_colors']=pres_colors
df['wspd_colors']=wspd_colors
df['wdir_colors']=wdir_colors
df['deltaT_colors']=deltaT_colors
df['RH_colors']=RH_colors
df['voltage_colors']=voltage_colors
df['panel_temp_colors']=panel_temp_colors

solid_color_df = pd.DataFrame(index=df.index,columns=['panel_temp_colors','voltage_colors','temp_colors','pres_colors','RH_colors','wspd_colors','wdir_colors','deltaT_colors']) 
solid_color_df['panel_temp_colors'] = panel_temp_colors 
solid_color_df['voltage_colors']=voltage_colors       
solid_color_df['temp_colors']=['black' for x in range(len(df))]
solid_color_df['pres_colors']=['black' for x in range(len(df))]
solid_color_df['RH_colors']=['black' for x in range(len(df))]
solid_color_df['wspd_colors']=['black' for x in range(len(df))]
solid_color_df['wdir_colors']=['black' for x in range(len(df))]
solid_color_df['deltaT_colors']=['black' for x in range(len(df))]
copied_solid_color_df = solid_color_df.copy()     

rules_df=pd.DataFrame(index=df.index,columns=['temp_rules','pres_rules','wspd_rules','wdir_rules','RH_rules','deltaT_rules'])
rules_df['wspd_rules'] = df['wspd'].where(( wspd_conditional | df['ws_is_repeated'] | df['wd_is_repeated'] | wdir_conditional))
rules_df['wdir_rules'] = df['wdir'].where((df['wd_is_repeated'] | wdir_conditional | df['ws_is_repeated'] | wspd_conditional))
rules_df['temp_rules'] = df['temp'].where(temp_conditional)
rules_df['pres_rules'] = df['pres'].where(pres_conditional)
rules_df['RH_rules'] = df['RH'].where(rh_conditional)
rules_df['deltaT_rules'] = df['deltaT'].where(deltaT_conditional)

app = Dash(__name__)

copied_df = df.copy()
if qc_type == 'none':
    cat_df = copied_df
cat_copy_df = cat_df.copy()

copied_df.drop(['panel_temp','voltage'], axis=1, inplace=True)
change_log = []

variables = (df.drop(columns=['time','year','Jday','month','day', 'year_jdate', 'date','ws_is_repeated','wd_is_repeated','ws_count','wd_count','ws_streak','wd_streak','temp_colors','pres_colors','wspd_colors','wdir_colors','deltaT_colors','RH_colors','voltage_colors','panel_temp_colors' ])).columns
full_var = ['Temperature','Pressure','Wind Speed', 'Wind Direction', 'Relative Humidity', 'deltaT', 'Voltage','Panel Temperature']
var_opt_list = []
for variable, full in zip(list(variables),full_var):
    temporary_dict = {'label':str(full), 'value':str(variable)}
    var_opt_list.append(temporary_dict)
    
app.layout = html.Div([
    html.H1(children="QC Test Platform - Standard"),
    dcc.Checklist(options=var_opt_list,value=['temp','pres'],id='select-variables', inline=True),
    html.H2(children="   "+stn_name+" ("+str(argos_id)+")      "+str(month)+"    "+str(year)+"\n"),
    html.Label(['Select Marker Size:']),
    dcc.RadioItems(options=['2','4','6','8','10','12','14','16'],value='6',inline=True,id='marker-size'),
    html.Br(),
    html.Label(['Select X-Axis Limits: ']),
    html.Br(),
    dcc.Input(placeholder='Day range: ', type='number',value='',id='day-range', min=0, max=32, debounce=False, autoComplete='on',size='5'),
    dcc.Input(placeholder='Center Day: ', type='number',value='',id='center-day', min=0, max=32, debounce=False, autoComplete='on',size='5'),
    html.Br(),
    html.Br(),
    html.Label(['Select Y-Axis Limits: ']),
    html.Br(),
    dcc.Input(placeholder='Min Temp: ', type='number',value='',id='min-temp-ylim', min=-120, max=60, debounce=False, autoComplete='on',size='5'),
    dcc.Input(placeholder='Min Pres: ', type='number',value='',id='min-pres-ylim', min=0, max=1200, debounce=True, autoComplete='on',size='5'),
    dcc.Input(placeholder='Min WSpd: ', type='number',value='',id='min-wspd-ylim', min=-10, max=200, debounce=True, autoComplete='on',size='5'),
    dcc.Input(placeholder='Min WDir: ', type='number',value='',id='min-wdir-ylim', min=-10, max=400, debounce=True, autoComplete='on',size='5'),
    dcc.Input(placeholder='Min RH: ', type='number',value='',id='min-rh-ylim', min=-20, max=120, debounce=True, autoComplete='on',size='5'),
    dcc.Input(placeholder='Min Delta T: ', type='number',value='',id='min-deltaT-ylim', min=-40, max=40, debounce=True, autoComplete='on',size='5') ,
    html.Br(),
    dcc.Input(placeholder='Max Temp: ', type='number',value='',id='max-temp-ylim', min=-120, max=60, debounce=False, autoComplete='on',size='5'),
    dcc.Input(placeholder='Max Pres: ', type='number',value='',id='max-pres-ylim', min=0, max=1200, debounce=True, autoComplete='on',size='5'),
    dcc.Input(placeholder='Max WSpd: ', type='number',value='',id='max-wspd-ylim', min=-10, max=150, debounce=True, autoComplete='on',size='5'),
    dcc.Input(placeholder='Max WDir: ', type='number',value='',id='max-wdir-ylim', min=-10, max=400, debounce=True, autoComplete='on',size='5'),
    dcc.Input(placeholder='Max RH: ', type='number',value='',id='max-rh-ylim', min=-20, max=120, debounce=True, autoComplete='on',size='5'),
    dcc.Input(placeholder='Max Delta T: ', type='number',value='',id='max-deltaT-ylim', min=-40, max=40, debounce=True, autoComplete='on',size='5') ,
    html.Br(),
    html.Label(['Show Rules? ']),
    dcc.RadioItems(options=['Yes','No'],value='Yes',inline=True,id='rules-toggle'),
    html.Br(),
    dcc.Graph(figure={}, id='display-met-data-subplots',config={'displayModeBar': True,"doubleClick":False}),
    dcc.Textarea(id='display-hover-data',style={'width':'15%', 'height':210}),
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
        data=copied_df.to_dict('records'))
])

@app.callback(Output('display-met-data-subplots','figure'),
              Input('select-variables','value'),
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
              Input('min-deltaT-ylim','value'),
              Input('max-deltaT-ylim','value'),
              Input('rules-toggle','value')) 

def update_graph(variables_selected,markersize,day_range,center_day,mintemp,maxtemp,minpres,maxpres,minwspd,maxwspd,minwdir,maxwdir,minrh,maxrh,mindeltaT,maxdeltaT,rules):
    dff = df[variables_selected]
    bounds_dict= {'mintemp':mintemp,'maxtemp':maxtemp,'minpres':minpres,'maxpres':maxpres,'minwspd':minwspd,'maxwspd':maxwspd,'minwdir':minwdir,'maxwdir':maxwdir,'minRH':minrh,'maxRH':maxrh,'mindeltaT':mindeltaT,'maxdeltaT':maxdeltaT}
    ind_dict = {}
    copy_dff = dff.copy()
    update_row_df = pd.DataFrame()
    if 'panel_temp' in dff.columns:
        test = copy_dff.drop(columns=['panel_temp'])
        titles = test.columns
    else:
        titles = list(dff.columns)
      
    marker=False 
    fig = make_subplots(rows=len(titles), cols=1,subplot_titles=titles, shared_xaxes=True, vertical_spacing=0.05, x_title='Date')
    for i, var in enumerate(variables_selected):
        i2 = i+1      
        if var == 'temp':
            temp_ind = i2
            ind_dict[var+'ind']=temp_ind
            fig.add_trace(go.Scattergl(x=dff.index, y=dff[var], mode='markers', name=var,marker=dict(color=copied_df[var+'_colors']),selected_marker_color='grey'),
                            row=i2, col=1)
            if qc_type == "prev":
                last_days_dff = last_days_df[variables_selected]
                fig.add_trace(go.Scattergl(x=last_days_dff.index, y=last_days_dff[var], mode='markers', name="prev"+var,marker_color='lightgrey',showlegend=False),
                                row=i2, col=1)
            if qc_type == "both":
                next_few_days_dff = next_few_days_df[variables_selected]
                fig.add_trace(go.Scattergl(x=next_few_days_dff.index, y=next_few_days_dff[var], mode='markers',showlegend=False, name="next"+var,marker_color='lightgrey'),
                            row=i2, col=1)
                last_days_dff = last_days_df[variables_selected]
                fig.add_trace(go.Scattergl(x=last_days_dff.index, y=last_days_dff[var], mode='markers', name="prev"+var,marker_color='lightgrey',showlegend=False),
                                row=i2, col=1)
            if qc_type == "next":
                next_few_days_dff = next_few_days_df[variables_selected]
                fig.add_trace(go.Scattergl(x=next_few_days_dff.index, y=next_few_days_dff[var], mode='markers',showlegend=False, name="next"+var,marker_color='lightgrey'),
                            row=i2, col=1)
                          
        if var == 'panel_temp':
            marker=True
            ind_dict[var+'ind']= temp_ind
            fig.add_trace(go.Scattergl(x=dot10_df.index, y=dot10_df['panel_temp'].astype(np.float64), mode='markers', name='Panel Temp', marker_color='darkseagreen'),
                                row=temp_ind, col=1)
            if qc_type == "prev":
                fig.add_trace(go.Scattergl(x=last_days_dot10_df.index, y=last_days_dot10_df['panel_temp'].astype(np.float64),showlegend=False, name="prev"+var,mode='markers', marker_color='lightseagreen'),
                                row=temp_ind, col=1)
            if qc_type == "both":
                fig.add_trace(go.Scattergl(x=last_days_dot10_df.index, y=last_days_dot10_df['panel_temp'].astype(np.float64),showlegend=False, name="prev"+var,mode='markers', marker_color='lightseagreen'),
                                row=temp_ind, col=1)
                fig.add_trace(go.Scattergl(x=next_few_days_dot10_df.index, y=next_few_days_dot10_df['panel_temp'].astype(np.float64),showlegend=False, mode='markers', name="next"+var,marker_color='lightseagreen'),
                        row=temp_ind, col=1)
            if qc_type == "next":
                fig.add_trace(go.Scattergl(x=next_few_days_dot10_df.index, y=next_few_days_dot10_df['panel_temp'].astype(np.float64),showlegend=False, mode='markers', name="next"+var,marker_color='lightseagreen'),
                        row=temp_ind, col=1)

        if var != 'temp' and var != 'panel_temp' and marker == True:
            ind_dict[var+'ind']=i
            fig.add_trace(go.Scattergl(x=dff.index, y=dff[var].astype(np.float64), mode='markers', name=str(var),marker=dict(color=copied_df[var+'_colors']),selected_marker_color='grey'),
                            row=i, col=1)
            if qc_type == "both" :
                next_few_days_dff = next_few_days_df[variables_selected]
                last_days_dff = last_days_df[variables_selected]
                fig.add_trace(go.Scattergl(x=next_few_days_dff.index, y=next_few_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="next"+var,marker_color='lightgrey'),
                            row=i, col=1)
                fig.add_trace(go.Scattergl(x=last_days_dff.index, y=last_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="prev"+var ,marker_color='lightgrey'),
                            row=i, col=1)  
            if qc_type == "next":
                next_few_days_dff = next_few_days_df[variables_selected]
                fig.add_trace(go.Scattergl(x=next_few_days_dff.index, y=next_few_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="next"+var,marker_color='lightgrey'),
                            row=i, col=1)              
            if qc_type == 'prev':
                last_days_dff = last_days_df[variables_selected]
                fig.add_trace(go.Scattergl(x=last_days_dff.index, y=last_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="prev"+var ,marker_color='lightgrey'),
                            row=i, col=1)  

        if var != 'temp' and var != 'panel_temp' and marker == False:
            ind_dict[var+'ind']=i2
            fig.add_trace(go.Scattergl(x=dff.index, y=dff[var].astype(np.float64), mode='markers', name=str(var),marker=dict(color=copied_df[var+'_colors']),selected_marker_color='grey'),
                            row=i2, col=1)
            if qc_type == "next" :
                next_few_days_dff = next_few_days_df[variables_selected]
                fig.add_trace(go.Scattergl(x=next_few_days_dff.index, y=next_few_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="next"+var,marker_color='lightgrey'),
                            row=i2, col=1)            
            if qc_type == "both" :
                next_few_days_dff = next_few_days_df[variables_selected]
                last_days_dff = last_days_df[variables_selected]
                fig.add_trace(go.Scattergl(x=next_few_days_dff.index, y=next_few_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="next"+var,marker_color='lightgrey'),
                            row=i2, col=1)
                fig.add_trace(go.Scattergl(x=last_days_dff.index, y=last_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="prev"+var ,marker_color='lightgrey'),
                            row=i2, col=1)    
            if qc_type == 'prev':
                last_days_dff = last_days_df[variables_selected]
                fig.add_trace(go.Scattergl(x=last_days_dff.index, y=last_days_dff[var].astype(np.float64), mode='markers',showlegend=False, name="prev"+var ,marker_color='lightgrey'),
                            row=i2, col=1)  
      
    fig.update_traces(mode="markers", hovertemplate=None)
    fig.update_layout(hovermode="x")
    fig.update_layout(clickmode='event+select',dragmode='pan')   
    fig.update_traces(marker=dict(size=int(markersize)))
    fig.update_layout(autosize=True,height=700,margin=dict(l=20, r=20, t=50, b=50))
    for i3, x in enumerate(fig.data):
        varname = x['name']
        if varname in dff.columns and varname != 'voltage' and varname != 'panel_temp':
            fig.update_yaxes(range=(bounds_dict['min'+varname], bounds_dict['max'+varname]), row=ind_dict[varname+'ind'], col=1) 
    
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

@callback(Output('display-hover-data', 'value'),
          Input('display-met-data-subplots', 'hoverData'),
          [State('display-met-data-subplots', 'figure')],prevent_initial_call=True)

def display_hover_data(hoverData, figure):
    datetime1 = hoverData['points'][0]['x'] 
    datetime = pd.to_datetime(datetime1)
    hover_values = cat_copy_df.loc[datetime]
    hover_date = hover_values['date']
    hover_time =hover_values['time']
    hover_temp =hover_values['temp']
    hover_pres =hover_values['pres']
    hover_rh =hover_values['RH']
    hover_deltaT =hover_values['deltaT']
    hover_wspd =hover_values['wspd']
    hover_wdir =hover_values['wdir']
    obs_id_num = len(copied_df.loc[:datetime]) -1
    info_str = 'Date: '+str(hover_date)[:10]+'\nTime: '+str(hover_time)+'\nTemperature: '+str(hover_temp)+'\nPressure: '+str(hover_pres)+'\nWind Speed: '+str(hover_wspd)+'\nWind Direction: '+str(hover_wdir)+'\nRelative Humidity: '+str(hover_rh)+'\nDeltaT: '+str(hover_deltaT)+'\nObs ID: '+str(obs_id_num)     
    return(info_str)
  
@app.callback([Output('display-click-data', 'value'), 
              Output('updated-data', 'data'),
              Output('change-log', 'data'),
              Output('display-met-data-subplots', 'figure',allow_duplicate=True)],
              [Input('display-met-data-subplots','clickData'),
              Input('display-met-data-subplots', 'selectedData'),
              Input('undo-button', 'n_clicks'),
              Input('reset-button', 'n_clicks'),],
              [State('display-met-data-subplots', 'figure'),
               State('rules-toggle','value')],prevent_initial_call='initial_duplicate') 

def display_clickdata(clickData1, selectData1, undo_clicks,reset_clicks,figure,rules):
    global copied_df, change_log,solid_color_df  # Ensure global reference

    ind_dict = {}
    ctx = dash.callback_context
    if ctx.triggered_id == 'undo-button' and change_log:
        for i in range(len(figure['data'])):
            ind_dict[figure['data'][i]['name']] = i
        last_change = change_log.pop()  # Revert the last change
        date = last_change['date']
        column = last_change['column']
        original_value = last_change['original']
        color_pre_change_value = df.at[date,column+'_colors']
        copied_df.at[date, column+'_colors'] = color_pre_change_value
        copied_df.at[date, column] = original_value
        solid_pre_change_value = copied_solid_color_df.at[date,column+'_colors']
        solid_color_df.at[date, column+'_colors'] = solid_pre_change_value
        
        if column in ind_dict.keys() and rules == 'Yes':
            figure['data'][ind_dict[column]]['marker']['color'] = copied_df[column+'_colors'].values
        if column in ind_dict.keys() and rules == 'No':
            figure['data'][ind_dict[column]]['marker']['color'] = solid_color_df[column+'_colors'].values
        return (f"Undo: {date} - {column} reverted to {original_value}", copied_df.to_dict('records'), change_log,figure)
    
    if ctx.triggered_id == 'reset-button':
        for i in range(len(figure['data'])):
            ind_dict[figure['data'][i-1]['name']] = i
        copied_df = df.copy()  # Reset to original
        solid_color_df = copied_solid_color_df.copy()
        for column in ind_dict.keys():
            if column[0:4] != 'next' and column [0:4] != 'prev' and rules == 'Yes':
                figure['data'][ind_dict[column]]['marker']['color'] = copied_df[column+'_colors']
            if column[0:4] != 'next' and column [0:4] != 'prev' and rules == 'No':
                figure['data'][ind_dict[column]]['marker']['color'] = solid_color_df[column+'_colors']
        change_log = []  # Clear the change log
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
            original_value = copied_df.at[date, column]
            new_value = np.float64(444.0)
            if point not in selected_points:
                # Add new selection
                selected_points.add(point)
                if original_value != new_value:
                    copied_df.at[date, column] = new_value
                    copied_df.at[date, column+'_colors'] = 'grey'
                    solid_color_df.at[date, column+'_colors'] = 'grey'
                    if rules == 'Yes':
                        figure['data'][ind_dict[column]]['marker']['color'] = copied_df[column+'_colors'].values
                    elif rules == 'No':
                        figure['data'][ind_dict[column]]['marker']['color'] = solid_color_df[column+'_colors'].values
                    change_log.append({
                        "date":date,
                        "column":column,
                        "original":original_value,
                        "new":new_value})
                    if column == 'wspd':
                        wd_original_value = copied_df.at[date, 'wdir']
                        copied_df.at[date, 'wdir'] = new_value
                        copied_df.at[date, 'wdir_colors'] = 'grey'
                        solid_color_df.at[date,'wdir_colors'] = 'grey'

                        if 'wdir' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['wdir']]['marker']['color'] = copied_df['wdir_colors'].values
                        if 'wdir' in ind_dict.keys() and rules == 'No':
                            figure['data'][ind_dict['wdir']]['marker']['color'] = solid_color_df['wdir_colors'].values
                        change_log.append({
                            "date":date,
                            "column":'wdir',
                            "original":wd_original_value,
                            "new":new_value})
                    if column == 'wdir' and rules == 'Yes':
                        ws_original_value = copied_df.at[date, 'wspd']
                        copied_df.at[date, 'wspd'] = new_value
                        copied_df.at[date,'wspd_colors'] = 'grey'
                        solid_color_df.at[date, 'wspd_colors'] = 'grey'
                        if 'wspd' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['wspd']]['marker']['color'] = copied_df['wspd_colors'].values
                        if 'wspd' in ind_dict.keys() and rules == 'No':
                            figure['data'][ind_dict['wspd']]['marker']['color'] = solid_color_df['wspd_colors'].values  
                        change_log.append({
                            "date":date,
                            "column":'wspd',
                            "original":ws_original_value,
                            "new":new_value})
                    if column == 'temp':
                        dt_original_value = copied_df.at[date, 'deltaT']
                        copied_df.at[date, 'deltaT'] = new_value
                        copied_df.at[date, 'deltaT_colors'] = 'grey'
                        solid_color_df.at[date,'deltaT_colors'] = 'grey'

                        if 'deltaT' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['deltaT']]['marker']['color'] = copied_df['deltaT_colors'].values
                        if 'deltaT' in ind_dict.keys() and rules == 'No':
                            figure['data'][ind_dict['deltaT']]['marker']['color'] = solid_color_df['deltaT_colors'].values
                        change_log.append({
                            "date":date,
                            "column":'deltaT',
                            "original":dt_original_value,
                            "new":new_value})
               
                if original_value == new_value:
                    selected_points.discard(point)
                    pre_change_value = df.at[date,column]
                    copied_df.at[date,column] = pre_change_value
                    color_pre_change_value = df.at[date,column+'_colors']
                    copied_df.at[date,column+'_colors'] = color_pre_change_value
                    solid_pre_change_value = copied_solid_color_df.at[date,column+'_colors']
                    solid_color_df.at[date,column+'_colors'] = solid_pre_change_value
                    if rules == 'Yes':
                        figure['data'][ind_dict[column]]['marker']['color'] = copied_df[column+'_colors'].values
                    elif rules == 'No':
                        figure['data'][ind_dict[column]]['marker']['color'] = solid_color_df[column+'_colors'].values
                    for i, test in enumerate(change_log):
                        if change_log[i]['date'] == date and change_log[i]['column']== column:
                            del change_log[i]
                    if column == 'wdir':
                        ws_pre_change_value = df.at[date,'wspd']
                        copied_df.at[date,'wspd'] = ws_pre_change_value
                        ws_color_pre_change_value = df.at[date,'wspd_colors']
                        copied_df.at[date,'wspd_colors'] = ws_color_pre_change_value
                        ws_solid_pre_change_value = copied_solid_color_df.at[date,'wspd_colors']
                        solid_color_df.at[date,'wspd_colors'] = ws_solid_pre_change_value
                        if 'wspd' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['wspd']]['marker']['color'] = copied_df['wspd_colors'].values
                        elif 'wspd' in ind_dict.keys() and rules == 'No':
                            figure['data'][ind_dict['wspd']]['marker']['color'] = solid_color_df['wspd_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']== 'wspd':
                                del change_log[i]
                    if column == 'wspd':
                        wd_pre_change_value = df.at[date,'wdir']
                        copied_df.at[date,'wdir'] = wd_pre_change_value
                        wd_color_pre_change_value = df.at[date,'wdir_colors']
                        copied_df.at[date,'wdir_colors'] = wd_color_pre_change_value
                        wd_solid_pre_change_value = copied_solid_color_df.at[date,'wdir_colors']
                        solid_color_df.at[date,'wdir_colors'] = wd_solid_pre_change_value
                        if 'wdir' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['wdir']]['marker']['color'] = copied_df['wdir_colors'].values
                        if 'wdir' in ind_dict.keys() and rules == 'No':
                            figure['data'][ind_dict['wdir']]['marker']['color'] = solid_color_df['wdir_colors'].values
                        for i,test2 in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']== 'wdir':
                                del change_log[i]
                    if column == 'temp':
                        dt_pre_change_value = df.at[date,'deltaT']
                        copied_df.at[date,'deltaT'] = dt_pre_change_value
                        dt_color_pre_change_value = df.at[date,'deltaT_colors']
                        copied_df.at[date,'deltaT_colors'] = dt_color_pre_change_value
                        dt_solid_pre_change_value = copied_solid_color_df.at[date,'deltaT_colors']
                        solid_color_df.at[date,'deltaT_colors'] = dt_solid_pre_change_value
                        
                        if 'deltaT' in ind_dict.keys() and rules == 'Yes':
                            figure['data'][ind_dict['deltaT']]['marker']['color'] = copied_df['deltaT_colors'].values
                        if 'deltaT' in ind_dict.keys() and rules == 'No':
                            figure['data'][ind_dict['deltaT']]['marker']['color'] = solid_color_df['deltaT_colors'].values
                        for i,test in enumerate(change_log):
                            if change_log[i]['date'] == date and change_log[i]['column']== 'deltaT':
                                del change_log[i]  
             
            elif point in selected_points:
                selected_points.discard(point)
                pre_change_value = df.at[date, column]
                copied_df.at[date, column] = pre_change_value
                color_pre_change_value = df.at[date,column+'_colors']
                copied_df.at[date,column+'_colors'] = color_pre_change_value
                solid_pre_change_value = copied_solid_color_df.at[date,column+'_colors']
                solid_color_df.at[date,column+'_colors'] = solid_pre_change_value
                if rules == 'Yes':
                    figure['data'][ind_dict[column]]['marker']['color'] = copied_df[column+'_colors'].values
                elif rules == 'No':
                    figure['data'][ind_dict[column]]['marker']['color'] = solid_color_df[column+'_colors'].values
                for i,test2 in enumerate(change_log):
                    if change_log[i]['date'] == date and change_log[i]['column']== column:
                        del change_log[i]
                if column == 'wspd':
                    selected_points.discard((date, 'wdir'))
                    wd_pre_change_value = df.at[date, 'wdir']
                    copied_df.at[date, 'wdir'] = wd_pre_change_value
                    wd_color_pre_change_value = df.at[date,'wdir_colors']
                    copied_df.at[date,'wdir_colors'] = wd_color_pre_change_value
                    solid_pre_change_value = copied_solid_color_df.at[date,'wdir_colors']
                    solid_color_df.at[date,'wdir_colors'] = solid_pre_change_value
                    if rules == 'Yes' and 'wdir' in ind_dict.keys():
                        figure['data'][ind_dict['wdir']]['marker']['color'] = copied_df['wdir_colors'].values
                    if rules == 'No' and 'wdir' in ind_dict.keys():
                        figure['data'][ind_dict['wdir']]['marker']['color'] = solid_color_df['wdir_colors'].values
                    for i,test2 in enumerate(change_log):
                        if change_log[i]['date'] == date and change_log[i]['column']=='wdir':
                            del change_log[i]
                if column == 'wdir':
                    selected_points.discard((date, 'wspd'))
                    ws_pre_change_value = df.at[date, 'wspd']
                    copied_df.at[date, 'wspd'] = ws_pre_change_value
                    ws_color_pre_change_value = df.at[date,'wspd_colors']
                    copied_df.at[date,'wspd_colors'] = ws_color_pre_change_value
                    solid_pre_change_value = copied_solid_color_df.at[date,'wspd_colors']
                    solid_color_df.at[date,'wspd_colors'] = solid_pre_change_value
                    if rules == 'Yes' and 'wspd' in ind_dict.keys():
                        figure['data'][ind_dict['wspd']]['marker']['color'] = copied_df['wspd_colors'].values
                    if rules == 'No' and 'wspd' in ind_dict.keys():
                        figure['data'][ind_dict['wspd']]['marker']['color'] = solid_color_df['wspd_colors'].values
                    for i,test2 in enumerate(change_log):
                        if change_log[i]['date'] == date and change_log[i]['column']== 'wspd':
                            del change_log[i]
                if column == 'temp':
                    selected_points.discard((date, 'deltaT'))
                    dt_pre_change_value = df.at[date, 'deltaT']
                    copied_df.at[date, 'deltaT'] = dt_pre_change_value
                    dt_color_pre_change_value = df.at[date,'deltaT_colors']
                    copied_df.at[date,'deltaT_colors'] = dt_color_pre_change_value
                    solid_pre_change_value = copied_solid_color_df.at[date,'deltaT_colors']
                    solid_color_df.at[date,'deltaT_colors'] = solid_pre_change_value
                    if rules == 'Yes' and 'wdir' in ind_dict.keys():
                        figure['data'][ind_dict['deltaT']]['marker']['color'] = copied_df['deltaT_colors'].values
                    if rules == 'No' and 'wdir' in ind_dict.keys():
                        figure['data'][ind_dict['deltaT']]['marker']['color'] = solid_color_df['deltaT_colors'].values
                    for i,test2 in enumerate(change_log):
                        if change_log[i]['date'] == date and change_log[i]['column']== 'deltaT':
                            del change_log[i]
                    if 'deltaT' in ind_dict.keys():
                        figure['data'][ind_dict['deltaT']]['marker']['color'] = copied_df['deltaT_colors'].values
        return ( f"{len(selected_points)} total selected points. ",copied_df.to_dict('records'),change_log,figure)
       #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
    return("No click data", copied_df.to_dict('records'), change_log,figure)

@callback(
    [Output("download-dataframe-csv", "data" ),   
     Output("download-qc-log-csv", "data")],
    Input("save-button", "n_clicks"),
    prevent_initial_call=True)
def save_data_csv(n_clicks):
    change_log_df = pd.DataFrame(change_log)  
    aws_abbreviation = closest_date_row['Short_Name'] 
    #name = closest_date_row['Name'] 
    short_name = aws_abbreviation.lower()

    qc_10min = (copied_df.drop(columns=['year_jdate','date','time','temp_colors','pres_colors','wspd_colors','wdir_colors','RH_colors','deltaT_colors','panel_temp_colors','voltage_colors'])).astype(np.float64)
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
    qc_10min['Jday']= qc_10min['Jday'].astype(int)
    
    qc_3hr['year'] = qc_3hr['year'].astype(int)
    qc_3hr['month']= qc_3hr['month'].astype(int)
    qc_3hr['day']= qc_3hr['day'].astype(int)
    qc_3hr['Jday']= qc_3hr['Jday'].astype(int)
    
    qc_1hr['year'] = qc_1hr['year'].astype(int)
    qc_1hr['month']= qc_1hr['month'].astype(int)
    qc_1hr['day']= qc_1hr['day'].astype(int)
    qc_1hr['Jday']= qc_1hr['Jday'].astype(int)
    
    time_10min = qc_10min.index.astype(str)
    qc_10min['time']  = [x[-8:-3].replace(':','') for x in time_10min]
    
    time_1hr= qc_1hr.index.astype(str)
    qc_1hr['time']  = [x[-8:-3].replace(':','') for x in time_1hr]
    
    time_3hr= qc_3hr.index.astype(str)
    qc_3hr['time']  = [x[-8:-3].replace(':','') for x in time_3hr]
    
    qc_10min = qc_10min[['year','Jday','month','day','time','temp','pres','wspd','wdir','RH','deltaT']]
    qc_1hr = qc_1hr[['year','Jday','month','day','time','temp','pres','wspd','wdir','RH','deltaT']]
    qc_3hr = qc_3hr[['year','Jday','month','day','time','temp','pres','wspd','wdir','RH','deltaT']]
    
    qc_10min = qc_10min.fillna(444.0)
    qc_1hr = qc_1hr.fillna(444.0)
    qc_3hr = qc_3hr.fillna(444.0)
    
    qc_10min['month'] = [str(x).rjust(2,' ') for x in qc_10min['month']]
    qc_10min['day'] = [str(x).rjust(2,' ') for x in qc_10min['day']]
    qc_10min['Jday'] = [str(x).rjust(3,' ') for x in qc_10min['Jday']]
    qc_10min['time']= [str(x).rjust(4,' ') for x in qc_10min['time']]
    qc_10min['temp']= [str(x).rjust(6,' ') for x in qc_10min['temp']]
    qc_10min['pres']= [str(x).rjust(6,' ') for x in qc_10min['pres']]
    qc_10min['wspd']= [str(x).rjust(6,' ') for x in qc_10min['wspd']]
    qc_10min['wdir']= [str(x).rjust(6,' ') for x in qc_10min['wdir']]
    qc_10min['RH']= [str(x).rjust(6,' ') for x in qc_10min['RH']]
    qc_10min['deltaT']= [str(x).rjust(6,' ') for x in qc_10min['deltaT']]
    
    qc_1hr['month'] = [str(x).rjust(2,' ') for x in qc_1hr['month']]
    qc_1hr['day'] = [str(x).rjust(2,' ') for x in qc_1hr['day']]
    qc_1hr['Jday'] = [str(x).rjust(3,' ') for x in qc_1hr['Jday']]
    qc_1hr['time']= [str(x).rjust(4,' ') for x in qc_1hr['time']]
    qc_1hr['temp']= [str(x).rjust(6,' ') for x in qc_1hr['temp']]
    qc_1hr['pres']= [str(x).rjust(6,' ') for x in qc_1hr['pres']]
    qc_1hr['wspd']= [str(x).rjust(6,' ') for x in qc_1hr['wspd']]
    qc_1hr['wdir']= [str(x).rjust(6,' ') for x in qc_1hr['wdir']]
    qc_1hr['RH']= [str(x).rjust(6,' ') for x in qc_1hr['RH']]
    qc_1hr['deltaT']= [str(x).rjust(6,' ') for x in qc_1hr['deltaT']]
    
    qc_3hr['month'] = [str(x).rjust(2,' ') for x in qc_3hr['month']]
    qc_3hr['day'] = [str(x).rjust(2,' ') for x in qc_3hr['day']]
    qc_3hr['Jday'] = [str(x).rjust(3,' ') for x in qc_3hr['Jday']]
    qc_3hr['time']= [str(x).rjust(4,' ') for x in qc_3hr['time']]
    qc_3hr['temp']= [str(x).rjust(6,' ') for x in qc_3hr['temp']]
    qc_3hr['pres']= [str(x).rjust(6,' ') for x in qc_3hr['pres']]
    qc_3hr['wspd']= [str(x).rjust(6,' ') for x in qc_3hr['wspd']]
    qc_3hr['wdir']= [str(x).rjust(6,' ') for x in qc_3hr['wdir']]
    qc_3hr['RH']= [str(x).rjust(6,' ') for x in qc_3hr['RH']]
    qc_3hr['deltaT']= [str(x).rjust(6,' ') for x in qc_3hr['deltaT']]
    number_of_rows = len(qc_10min)
    number_of_days = qc_10min['day'].iloc[-1]
    raw_header = aws_abbreviation+"  "+str(argos_id)+"  "+str(name)+"                "+str(lat)+"   "+str(lon)+"    "+str(elev)+"  "+str(year)+"   "+str(month)+"  "+str(number_of_days)+"  "+str(number_of_rows)+"            RH       delta-T"
    dat_header = '  '+str(month)+'  '+str(year_abv)+'   Station : '+str(argos_id)+'  '+str(name)+'\n  Lat : '+str(lat)+'  Long : '+str(lon)+'  Elev : '+str(elev)+' M'

    raw_file_df = qc_10min.copy()
    raw_file_df['temp_man_qc'] = np.nan
    raw_file_df['pres_man_qc'] = np.nan
    raw_file_df['wdir_man_qc'] = np.nan
    raw_file_df['wspd_man_qc'] = np.nan
    raw_file_df['RH_man_qc'] = np.nan
    raw_file_df['deltaT_man_qc'] = np.nan
    for row in change_log_df.itertuples():
        datetime = row[1]
        variable = row[2]
        value = row[3]
        raw_file_df.loc[datetime,variable+'_man_qc'] = value 
    len_temp_qc = len(raw_file_df['temp_man_qc'].dropna())
    len_pres_qc =len(raw_file_df['pres_man_qc'].dropna())
    len_wspd_qc = len(raw_file_df['wspd_man_qc'].dropna())
    len_wdir_qc =len(raw_file_df['wdir_man_qc'].dropna())
    len_deltaT_qc =len(raw_file_df['deltaT_man_qc'].dropna())
    len_rh_qc =len(raw_file_df['RH_man_qc'].dropna())

    raw_file_df['temp_rules'] = rules_df['temp_rules']
    raw_file_df['pres_rules'] = rules_df['pres_rules']
    raw_file_df['wspd_rules'] = rules_df['wspd_rules']
    raw_file_df['wdir_rules'] = rules_df['wdir_rules']
    raw_file_df['RH_rules'] = rules_df['RH_rules']
    raw_file_df['deltaT_rules'] = rules_df['deltaT_rules']
    raw_file_df =raw_file_df.fillna(444.0)
    for col in raw_file_df.columns:
        if col[-6:] == 'man_qc':
            raw_file_df[col] = raw_file_df[col].astype(str).str.rjust(6,' ')
        if col[-5:] == 'rules':
            raw_file_df[col] = raw_file_df[col].astype(str).str.rjust(6,' ')
            
    len_temp_rules = len(rules_df['temp_rules'].dropna())
    len_pres_rules =len(rules_df['pres_rules'].dropna())
    len_wspd_rules = len(rules_df['wspd_rules'].dropna())
    len_wdir_rules =len(rules_df['wdir_rules'].dropna())
    len_deltaT_rules =len(rules_df['deltaT_rules'].dropna())
    len_rh_rules =len(rules_df['RH_rules'].dropna())
    raw_header_counter =str(len_temp_qc).rjust(6,' ')+str(len_temp_rules).rjust(6,' ')+'\n'+str(len_pres_qc).rjust(6,' ')+str(len_pres_rules).rjust(6,' ')+'\n'+str(len_wspd_qc).rjust(6,' ')+str(len_wspd_rules).rjust(6,' ')+'\n'+str(len_wdir_qc).rjust(6,' ')+str(len_wdir_rules).rjust(6,' ')+'\n'+str(len_rh_qc).rjust(6,' ')+str(len_rh_rules).rjust(6,' ')+'\n'+str(len_deltaT_qc).rjust(6,' ')+str(len_deltaT_rules).rjust(6,' ')
    dat_file_df = (qc_3hr.copy())[['temp','pres','wspd','wdir','RH','deltaT']]
    
    #output paths
    q1h_output_path = base_path + all_filenames.loc['q1h_output_path'].values[0] %(short_name,year,month)
    q3h_output_path = base_path + all_filenames.loc['q3h_output_path'].values[0] %(short_name,year,month)
    q10_output_path = base_path + all_filenames.loc['q10_output_path'].values[0] %(short_name,year,month)
    raw_output_path = base_path + all_filenames.loc['raw_output_path'].values[0] %(short_name,year,month)

    dat_output_path = base_path + all_filenames.loc['dat_output_path'].values[0] %(argos_id[2:],month,year_abv)

    raw_file_df=raw_file_df[['year','Jday','month','day','time','temp','temp_man_qc','temp_rules','pres','pres_man_qc','pres_rules','wspd','wspd_man_qc','wspd_rules','wdir','wdir_man_qc','wdir_rules','RH','RH_man_qc','RH_rules','deltaT','deltaT_man_qc','deltaT_rules']]

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
        for row in qc_3hr.itertuples(index=False, name=None):
            f.write(" ".join(map(str, row)) + "\n")
    with open(q1h_output_path, "w") as f:
        # Write the header
        f.write("".join(qc_header) + "\n")
        # Write each row
        for row in qc_1hr.itertuples(index=False, name=None):
            f.write(" ".join(map(str, row)) + "\n")
    with open(q10_output_path, "w") as f:
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
    return(dcc.send_data_frame(copied_df.to_csv , str(qc_csv_output_path)),
    dcc.send_data_frame(change_log_df.to_csv, str(change_log_output_path)))

if __name__ == '__main__':
    app.run(port=8871)
    #app.run(port=8871,debug=True)
    #app.run(debug=True,jupyter_mode="tab",port=8872)
