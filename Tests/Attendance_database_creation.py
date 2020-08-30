import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3

conn = sqlite3.connect('Attendance_database.db')
c = conn.cursor()

c.execute('CREATE TABLE ATTENDANCE (Time TEXT, User_full_name TEXT, IP_address TEXT, Roll_no INT, Course_id INT)')


df = pd.read_csv(r'C:\Users\samya\Downloads\logs_20200827-1619.csv')

df['Time'] = df['Time'].apply(lambda x : datetime.strptime(x, '%d/%m/%y, %H:%M'))

dummy = df.loc[((df['Event name'] == 'Meeting left') | (df['Event name'] == 'Meeting joined'))]

dummy['User full name'].str.findall(r'(\D+)').apply(lambda x : x[-1])

dummy['Roll_no'] = dummy['User full name'].str.findall(r'(\d+)')
dummy = dummy[~dummy.Roll_no.str.len().eq(0)]
dummy['Roll_no'] = dummy['Roll_no'].apply(lambda x : x[-1])
dummy['Roll_no'] = dummy['Roll_no'].astype('int64')

dummy['Course_id'] = dummy['Description'].str.findall(r'(\d+)').apply(lambda x : x[-1])
dummy['Course_id'] = dummy['Course_id'].astype(int)

dummy.drop(['Affected user','Event context','Component','Origin','Description','Event name'],axis=1,inplace = True)

dummy.to_sql('ATTENDANCE', conn, if_exists='replace', index = False)

c.execute('''  SELECT * FROM ATTENDANCE''')
for row in c.fetchall():
    print (row)

#dummy.loc[((dummy['Roll_no'] == 1803310179) & (df['Time'].dt.hour < 12))]
a = dummy.columns
print(a)
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