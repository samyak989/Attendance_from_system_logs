import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3
import os

#location of log files
data_path = os.path.join(os.path.dirname(__file__),'Data')
#data_path = os.path.join(os.path.dirname(__file__),'Data/logs_20200827-1619.csv')
#location of datbase file
database_path = os.path.join(os.path.dirname(__file__),'Database/Attendance_database.db')

conn = sqlite3.connect(database_path)
c = conn.cursor()

#creating attendance table
c.execute('CREATE TABLE ATTENDANCE (Time TEXT, User_full_name TEXT, IP_address TEXT, Roll_no INT, Course_id INT)')


#reading log file
files_list = os.listdir(data_path)
df = pd.concat([pd.read_csv(os.path.join(data_path,f)) for f in files_list])
#df = pd.read_csv(data_path)

#Converting to datetime object
df['Time'] = df['Time'].apply(lambda x : datetime.strptime(x, '%d/%m/%y, %H:%M'))

#Only taking the rows with evntname = meting left or join
dummy = df.loc[((df['Event name'] == 'Meeting left') | (df['Event name'] == 'Meeting joined'))]

#extracting names
dummy['Name']=dummy['User full name'].str.findall(r'(\D+)').apply(lambda x : x[-1])

#extracting roll no.
dummy['Roll_no'] = dummy['User full name'].str.findall(r'(\d+)')
dummy = dummy[~dummy.Roll_no.str.len().eq(0)]
dummy['Roll_no'] = dummy['Roll_no'].apply(lambda x : x[-1])
dummy['Roll_no'] = dummy['Roll_no'].astype('int64')

#extracting course_id
dummy['Course_id'] = dummy['Description'].str.findall(r'(\d+)').apply(lambda x : x[-1])
dummy['Course_id'] = dummy['Course_id'].astype(int)

#extracting date and time
dummy['Year'] = dummy['Time'].dt.year
dummy['Month'] = dummy['Time'].dt.month
dummy['Day'] = dummy['Time'].dt.day
dummy['Hour'] = dummy['Time'].dt.hour
dummy['Minute'] = dummy['Time'].dt.minute
#extracting time
#dummy['Time']=dummy['Time'].dt.time

#dropping columns
dummy.drop(['User full name','Affected user','Event context','Component','Origin','Description','Event name'],axis=1,inplace = True)

#dummy = dummy.groupby(df['Roll_no']).aggregate({'Name':'first', 'Month':'first', 'Day':'first', 'Hour':'first','Minute':'first', 'Course_id':'first', 'IP address':'first'})
#rearranging columns
dummy = dummy[['Name', 'Roll_no','Year', 'Month', 'Day', 'Hour','Minute', 'Course_id', 'IP address']]

#giving datafrme to database
dummy.to_sql('ATTENDANCE', conn, if_exists='replace', index = False)

c.execute('''  SELECT * FROM ATTENDANCE''')
for row in c.fetchall():
    print (row)

#cane used to extract roll no. wise data
#dummy.loc[((dummy['Roll_no'] == 1803310179) & (df['Time'].dt.hour < 12))]

#extracting course_id's
classes = np.sort(dummy['Course_id'].unique())

'''for sec in classes:
    for low_interval in range(10,17):
        a = dummy.loc[((dummy['Course_id'] == sec) & (dummy['Time'].dt.hour < (low_interval+1)) &
                       (dummy['Time'].dt.hour >= low_interval))]#['User full name'].unique()
        a =a.groupby(df['User full name']).aggregate({'Roll_no':'first','Time':'first'})
        if low_interval == 13:
            continue
        if len(a)>0:
            print(sec)
            print(low_interval,"-",low_interval+1)
            print(a)
            print("-------------------------------------------")
'''