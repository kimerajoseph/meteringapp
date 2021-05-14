import pandas as pd
import tabula
from datetime import datetime
from sqlalchemy import create_engine
import pymysql
from sqlalchemy.types import String, SmallInteger,VARCHAR,INT,Float
import numpy as np

engine = create_engine('mysql://root:uxiGJV2uwUWAS533CRDd@database-1.cjvdavipre6m.us-west-2.rds.amazonaws.com:3306/meteringdatabase')

table_list = []
conn = pymysql.connect(host='database-1.cjvdavipre6m.us-west-2.rds.amazonaws.com', port=3306,
                       user='root', password='uxiGJV2uwUWAS533CRDd', database='meteringdatabase')
c = conn.cursor()
df1 = pd.read_sql(f"select Datetime,P_kW from 1749606_load_profile",con=conn)
print(df1)
df2 = pd.read_sql(f"select Datetime,Active_Energy_Exp from 1755501_load_profile",con=conn)
df1['Datetime'] = pd.to_datetime(df1['Datetime'])
df2['Active_Energy_Exp'] = df2['Active_Energy_Exp'].astype(float)
#df2['P_kW'] = df2.apply(lambda row: (row['Active_Energy_Exp']/2),axis=1)
#loss_dfx['Add_I'] = loss_dfx.apply(lambda row: (row['additional_load']/row['comb']),axis=1)
df2['P_kW'] = df2['Active_Energy_Exp']*2
df1.to_csv(f'C:\\Users\\KIMERA\\Desktop\\energy meter downloads and config\\cewe mutundwe - kawanda\\compp.csv')

start_datex = df1['Datetime'].iloc[0]
end_datex = df1['Datetime'].iloc[-1]
final_df = df2[df2['Datetime'].between(start_datex, end_datex)]

date_list = final_df['Datetime'].tolist()
date_list2 = df1['Datetime'].tolist()

new_list = set(date_list) & set(date_list2) #COMPARING THE TWO LISTS
print(len(date_list))
print(len(date_list2))
print(len(new_list))
power_list,power_list1 = [],[]
for item in new_list:
    power = df1['P_kW'][df1['Datetime'] == item].values
    power_list.append(power)
    power2 = final_df['P_kW'][final_df['Datetime'] == item].values
    power_list1.append(power2)

#print(len(power_list1))
df_date = pd.DataFrame(new_list)
df_date.columns = ["Datetime"]
dfxx = pd.DataFrame(power_list)
dfxx.columns = ["P_MW_s"]
#print(dfxx)
dfxx1= pd.DataFrame(power_list1)
dfxx1.columns = ["P_MW_r"]

capacity = float(457)
my_df = pd.concat([df_date, dfxx, dfxx1], axis=1)
month_year = my_df['Datetime'].dt.strftime('%B_%Y').tolist()
my_df.insert(1, 'month_year', month_year)

#FILTER VALUES WHERE NO POWER WAS BEING SENT OR RECEIVED
my_df = my_df[my_df['P_MW_s'].values != 0]
my_df = my_df[my_df['P_MW_r'].values != 0]

#CONVERT POWER TO FLOATS AND MAKE VALUES ABSOLUTE
my_df["P_MW_s"] = my_df["P_MW_s"].astype(float).abs()
my_df["P_MW_r"] = my_df["P_MW_r"].astype(float).abs()
my_df['perc_load'] = my_df.apply(lambda row: (row['P_MW_s'] * 100 /capacity),axis=1)
my_df['perc_load'] = my_df['perc_load'].round(decimals=2)
my_df['loss'] = my_df.apply(lambda row: (row['P_MW_s'] - row['P_MW_r']),axis=1)
my_df['loss'] = my_df['loss'].abs()
my_df['loss'] = my_df['loss'].round(decimals=2)
my_df['perc_loss'] = my_df.apply(lambda row: (row['loss']*100/ row['P_MW_s']),axis=1)
my_df['perc_loss'] = my_df['perc_loss'].round(decimals=2)
component = 'Kawanda_Mutundwe'
time_stamp = datetime.now().__format__("%Y-%m-%d %H:%M")
timestamp_l = [time_stamp] * len(my_df.index)
my_df.insert(1, 'timestamp', timestamp_l, True)
# print(dfxx1)
# print(len(dfxx1.index))
# print(len(dfxx.index))
# print(len(df_date.index))
# list_x = zip(new_list, power_list)
# ff_list = dict(list_x)
# print(ff_list)

# print(power_list)
# print(power_list1)
# dd = pd.DataFrame(power_list)
# dd.columns = ['final_PW']
# # new_df1.to_csv(f'C:\\Users\\KIMERA\\Desktop\\energy meter downloads and config\\cewe mutundwe - kawanda\\kakasa1.csv')
#my_df.to_csv(f'C:\\Users\\KIMERA\\Desktop\\energy meter downloads and config\\cewe mutundwe - kawanda\\pakasa.csv')

c.execute("SHOW TABLES ")
data = c.fetchall()
table_list = []
for x in data:
    table_name = x[0]
    table_list.append(table_name)
current_table = f'{component}_Loss'

if current_table in table_list:
    my_df.to_sql(f'{current_table}', con=engine, if_exists='append', index=False,
               dtype={'Timestamp': VARCHAR(length=20),'Datetime': VARCHAR(length=30), 'month_year': VARCHAR(length=30),
                      'P_MW_s': Float(), 'P_MW_r': Float(), 'perc_load': Float(),'loss': Float(), 'perc_loss': Float()})

else:
    my_df.to_sql(f'{current_table}', con=engine, if_exists='append', index=False,
              dtype={'Timestamp': VARCHAR(length=20), 'Datetime': VARCHAR(length=30),
                     'month_year': VARCHAR(length=30),
                     'P_MW_s': Float(), 'P_MW_r': Float(), 'perc_load': Float(), 'loss': Float(),
                     'perc_loss': Float()})

    #c.execute(f"ALTER TABLE {current_table} ADD id int(5) NOT NULL PRIMARY KEY AUTO_INCREMENT FIRST")
    c.execute(f"ALTER TABLE {current_table} ADD id int(5) NOT NULL PRIMARY KEY AUTO_INCREMENT FIRST")
    conn.commit()
    c.close()
    conn.close()





