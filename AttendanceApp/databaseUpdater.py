from AttendanceApp import app, db
from AttendanceApp.models import Attendance
from datetime import datetime
import pandas as pd
import numpy as np
import sqlite3
import os

def update_database(file_name):
    class_starttime = 10
    class_endtime = 17
    thresholdDuration = 30
    
    #location of log files
    file_path = os.path.join('Data', file_name)
    
    #reading log file
    sourceFrame = pd.read_csv(file_path)
    #sourceFrame = pd.read_csv(data_path)    #for reaing single file
    
    #Converting to datetime object
    sourceFrame['Time'] = sourceFrame['Time'].apply(lambda x : datetime.strptime(x, '%d/%m/%y, %H:%M'))
    
    #Only taking the rows with evntname = meting left or join 
    dummy = sourceFrame.loc[((sourceFrame['Event name'] == 'Meeting left') | (sourceFrame['Event name'] == 'Meeting joined') | (sourceFrame['Event name'] == 'Activity viewed'))]
    #Renaming 'Activity viewed' to 'Meeting Joined'
    dummy.loc[(dummy['Event name'] == 'Activity viewed', 'Event name')] = 'Meeting joined'
    
    #extracting roll no.
    dummy['Roll_no'] = dummy['User full name'].str.findall(r'(\d+)')
    dummy = dummy[~dummy.Roll_no.str.len().eq(0)]
    dummy['Roll_no'] = dummy['Roll_no'].apply(lambda x : x[-1])
    dummy['Roll_no'] = dummy['Roll_no'].astype('int64')
    
    #extracting names
    dummy['Name']=dummy['User full name'].str.findall(r'(\D+)').apply(lambda x : x[-1])
    
    #extracting course_id
    dummy['Course_id'] = dummy['Description'].str.findall(r'(\d+)').apply(lambda x : x[-1])
    dummy['Course_id'] = dummy['Course_id'].astype(int)
    
    #dropping columns
    dummy.drop(['User full name','Affected user','Event context','Component','Origin','Description'],axis=1,inplace = True)
    
    #extracting sec id's's
    classes = np.sort(dummy['Course_id'].unique())
    
    #extracting dates
    dates = np.sort(dummy['Time'].dt.date.unique())
    
    #removing the duplicate rows in same hour
    final = pd.DataFrame()
    for sec in classes:
        for date in dates:
            for low_interval in range(class_starttime,class_endtime):
                temp = dummy.loc[((dummy['Course_id'] == sec) & (dummy['Time'].dt.hour < (low_interval+1)) &(dummy['Time'].dt.hour >= low_interval) & (dummy['Time'].dt.date == date))]
    
                temp = temp.sort_values(by = 'Time')     
                temp = temp.loc[(temp['Event name'] == 'Meeting joined')]
                temp.drop_duplicates(subset ="Roll_no", keep = 'first', inplace = True)
                
                temp['duration'] = 60 - temp['Time'].dt.minute

                if low_interval == 13:
                    continue
                if not temp.empty:
                    final = final.append(temp,ignore_index=True)
    final.reset_index(drop=True,inplace= True)

    #adding className
    final['className'] = final['Course_id']
    final.loc[final['Course_id'] == 29, 'className'] = 'CSE 4(C+D)'
    final.loc[final['Course_id'] == 28, 'className'] = 'CSE 4D'
    final.loc[final['Course_id'] == 27, 'className'] = 'CSE 4C'
    final.loc[final['Course_id'] == 32, 'className'] = 'CSE 4(A+B) 1'
    final.loc[final['Course_id'] == 30, 'className'] = 'CSE 4(A+B)'
    final.loc[final['Course_id'] == 26, 'className'] = 'CSE 4B'
    final.loc[final['Course_id'] == 25, 'className'] = 'CSE 4A'
    final.loc[final['Course_id'] == 31, 'className'] = 'CSE 3(C+D) 1'
    final.loc[final['Course_id'] == 24, 'className'] = 'CSE 3(C+D)'
    final.loc[final['Course_id'] == 22, 'className'] = 'CSE 3D'
    final.loc[final['Course_id'] == 21, 'className'] = 'CSE 3C'
    final.loc[final['Course_id'] == 60, 'className'] = 'CSE 3(A+B) 1'
    final.loc[final['Course_id'] == 23, 'className'] = 'CSE 3(A+B)'
    final.loc[final['Course_id'] == 20, 'className'] = 'CSE 3B'
    final.loc[final['Course_id'] == 19, 'className'] = 'CSE 3A'
    final.loc[final['Course_id'] == 18, 'className'] = 'CSE 2(C+D)'
    final.loc[final['Course_id'] == 16, 'className'] = 'CSE 2D'
    final.loc[final['Course_id'] == 15, 'className'] = 'CSE 2C'
    final.loc[final['Course_id'] == 17, 'className'] = 'CSE 2(A+B)'
    final.loc[final['Course_id'] == 14, 'className'] = 'CSE 2B'
    final.loc[final['Course_id'] == 13, 'className'] = 'CSE 2A'
    final.loc[final['Course_id'] == 12, 'className'] =  'ME 3C'
    final.loc[final['Course_id'] == 11, 'className'] =  'ME 3A'
    final.loc[final['Course_id'] == 33, 'className'] = 'CE 2A'
    final.loc[final['Course_id'] == 39, 'className'] = 'IT 2A'

    #add attended column
    final['attended'] = False
    final.loc[final['duration'] > thresholdDuration, 'attended'] = True

    #drop unneccesary columns
    final.drop(columns= ['Event name', 'Course_id'], inplace= True)

    #Rename columns to match table
    final.rename(columns= {
        'Time': 'dateTime',
        'IP address': 'ipAddress',
        'Roll_no': 'rollNo',
        'Name': 'name'
    }, inplace= True)

    #providing dataframe to database
    final.to_sql(name='Attendance', con=db.engine, if_exists= 'append', index=False)
