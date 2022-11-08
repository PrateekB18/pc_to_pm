# -*- coding: utf-8 -*-
'''
##########################
Created on Mon May 2 2022
@author: Prateek
##########################
Function to convert Particle Counter data to PM2.5 and PM10 data

Function reads csv file and returns a pandas dataframe with AEST time as index
column in datetime format and PM2.5/PM10 columns in #/cm^3

file_path can be absolute or relative path to the CSV file

'''

import pandas as pd
import datetime
from dateutil import tz

def pc_to_pm(file_path, PM=1):

    data = pd.read_csv(file_path, header=None, names=['a', 'b', 'c', 'd', 'e' ,'f',
                                                     'g','h','i','j','k','l','m',
                                                     'n','o','p','q','r','s','t',
                                                     'u','v','w','x'])
    bins = int(data.iloc[10]['b'])

    df = data[data.index>36]
    headers = df.iloc[0]
    new_df  = pd.DataFrame(df.values[1:], columns=headers)
    new_df.set_index('Elapsed Time [s]', inplace=True)
    new_df = new_df.drop(new_df.columns[[bins+1,14,15,16,21,22]], axis = 1)
    df = new_df
    del new_df

    start_time = datetime.datetime.strptime(data.iloc[7]['b'].replace("/", "-")+' '
                                   +data.iloc[6]['b'], "%Y-%m-%d %H:%M:%S")
    start_time = start_time.replace(tzinfo=tz.gettz('Australia/Sydney'))
    df['time'] = start_time
    for i in range(len(df)):
        df['time'][i] = df['time'][i]+datetime.timedelta(0,int(df.index[i]))

    df = df.reset_index().set_index('time')
    df = df.apply(pd.to_numeric)
    fl_rate = 1000/60
    sample_time = (df.index[2]-df.index[1]).total_seconds()
    vol = fl_rate*sample_time
    
    df['PM25'] = (df['Bin 1']+df['Bin 2']+df['Bin 3']+df['Bin 4']+df['Bin 5']+df['Bin 6'])/vol
    df['PM10'] = (df['Bin 1']+df['Bin 2']+df['Bin 3']+df['Bin 4']+df['Bin 5']+df['Bin 6']+
                  df['Bin 7']+df['Bin 8']+df['Bin 9']+df['Bin 10']+df['Bin 11']+df['Bin 12']+
                  df['Bin 13'])/vol
    if PM==1:
        df = df.drop(['Bin 1', 'Bin 2', 'Bin 3', 'Bin 4', 'Bin 5', 'Bin 6', 'Bin 7', 'Bin 8', 'Bin 9'
                 , 'Bin 10', 'Bin 11', 'Bin 12', 'Bin 13', 'Deadtime (s)', 'Temperature (C)'
                 , 'Humidity (%)', 'Ambient Pressure (kPa)', 'Elapsed Time [s]'], axis=1)
    return df

