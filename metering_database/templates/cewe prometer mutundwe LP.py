import pandas as pd
import tabula
from datetime import datetime
from sqlalchemy import create_engine
import pymysql
from sqlalchemy.types import String, SmallInteger,VARCHAR,INT,Float

# df = tabula.read_pdf('C:\\Users\\KIMERA\\Desktop\\energy meter downloads and config\\cewe mutundwe - kawanda\\'
#                      'KAWANDA II.pdf', pages = 'all')
# print(df)
#
# leng = len(df)
# #print(leng)
# df0 = df[0]
# col_len = len(df0.columns.tolist())
# col_names = df0.columns.tolist()
# #print(col_names)
# global df_final
# for i in range(1, leng):
#     dfc = df[i]
#     dfc_len = len(dfc.columns.tolist())
#     #print(len(dfc.columns.tolist()))
#     diff = dfc_len - col_len
#     #print(diff)
#     dfc.drop(dfc.iloc[:, 1:diff + 1], inplace=True, axis=1)
#     dfc.columns = col_names
#     df_final = pd.concat([df0, dfc], axis=0)
#     df0 = df_final
#     #dfc.to_csv(f'C:\\Users\\KIMERA\\Desktop\\energy meter downloads and config\\cewe mutundwe - kawanda\\df{i}.csv')
#     df0.append(dfc)
#
# df0.drop(df0.columns[[1,2,6]],inplace=True, axis=1)
# #df0.drop(df0.columns[6],inplace=True, axis=1)
# final_column_names = ['Datetime', 'V(All Phases)', 'I(All Phases)', 'PF','V_THD(All)','I_THD(All)']
# df_final = df0.iloc[2:]
# #df_final['Datetime'] = pd.to_datetime(df_final['Datetime'])
# df_final.columns = [final_column_names]
# print(df_final.dtypes)
# # RESETTING PANDAS DF INDEX
# date_list1 = df_final['Datetime'].squeeze().tolist()
# final_date1 = []
# for item in date_list1:
#     new_date = datetime.strptime(item,'%m/%d/%Y %H:%M')
#     final_date1.append(new_date)
# df_f = df_final.drop('Datetime',axis=1)
# print(final_date1)
# #df_f['Datetime'] = pd.to_datetime(df_f['Datetime'])
# df_final.insert(0,'Datetime',final_date1,True)
# print(df_final.dtypes)
# df_final.reset_index(inplace=True, drop=True)
# start_date = df_final['Datetime'].iloc[0]
# end_date = df_final['Datetime'].iloc[-1]
# print(start_date)
# print(end_date)
# df_final.to_csv(f'C:\\Users\\KIMERA\\Desktop\\energy meter downloads and config\\cewe mutundwe - kawanda\\df_final.csv')

#GETTING POWER
file = "C:\\Users\\KIMERA\\Desktop\\energy meter downloads and config\\cewe mutundwe - kawanda\\KAWANDA II POWER.pdf"
df1 = tabula.read_pdf(file, pages = 'all')
print(df1)
dfmn = tabula.read_pdf(file, pages='1', guess=False)
colx = dfmn[0].columns.tolist()
global meter_no
for item in colx:
    if item.find('Logger') != -1:
        #print(item)
        meter_no = item.split()[1]
        print(meter_no)
leng = len(df1)
print(leng)
df10 = df1[0]
col_len = len(df10.columns.tolist())
col_names = df10.columns.tolist()
#print(col_names)
global df1_final
for i in range(1, leng):
    df1c = df1[i]
    df1c_len = len(df1c.columns.tolist())
    #print(len(df1c.columns.tolist()))
    diff = df1c_len - col_len
    #print(diff)
    df1c.drop(df1c.iloc[:, 1:diff + 1], inplace=True, axis=1)
    df1c.columns = col_names
    df1_final = pd.concat([df10, df1c], axis=0)
    df10 = df1_final
    #df1c.to_csv(f'C:\\Users\\KIMERA\\Desktop\\energy meter downloads and config\\cewe mutundwe - kawanda\\df1{i}.csv')
    df10.append(df1c)

df10.drop(df10.columns[[1,2]],inplace=True, axis=1)  #DROPPING UNWANTED COLUMNS WITH DASHES
column_names = ['Datetime','Active_Energy_Imp', 'Active_Energy_Exp'] #COLUMN NAMES AS PER THE DOWNLOADED FILES
df_f = df10.iloc[2:]
df_f.columns = [column_names]
date_list = df_f['Datetime'].squeeze().tolist()
final_date = []
for item in date_list:
    new_date = datetime.strptime(item,'%m/%d/%Y %H:%M')
    final_date.append(new_date)
df_f = df_f.drop('Datetime',axis=1)
print(final_date)
#df_f['Datetime'] = pd.to_datetime(df_f['Datetime'])
df_f.insert(0,'Datetime',final_date,True)
print(df_f.dtypes)

time_stamp = now = datetime.now().__format__("%Y-%m-%d %H:%M") #ADDING TIMESTAMP
df_f.reset_index(inplace=True, drop=True)
timestamp_l = [time_stamp] * len(df_f.index)
df_f.insert(1, 'timestamp', timestamp_l, True)
engine = create_engine('mysql://root:uxiGJV2uwUWAS533CRDd@database-1.cjvdavipre6m.us-west-2.rds.amazonaws.com:3306/meteringdatabase')

table_list = []
conn = pymysql.connect(host='database-1.cjvdavipre6m.us-west-2.rds.amazonaws.com', port=3306,
                       user='root', password='uxiGJV2uwUWAS533CRDd', database='meteringdatabase')
c = conn.cursor()
c.execute("SHOW TABLES ")
data = c.fetchall()
for x in data:
    table_name = x[0]
    table_list.append(table_name)
current_table = f'{meter_no}_load_profile'
if current_table in table_list:
    df_f.to_sql(f'{current_table}', con=engine, if_exists='append', index=False,
    dtype={'Timestamp': VARCHAR(length=20),'Datetime': VARCHAR(length=30),'Active_Energy_Imp': Float(), 'Active_Energy_Exp': Float()})


else:
    df_f.to_sql(f'{current_table}', con=engine, if_exists='append', index=False,
                dtype={'Timestamp': VARCHAR(length=20), 'Datetime': VARCHAR(length=30), 'Active_Energy_Imp': Float(),
                       'Active_Energy_Exp': Float()})

    c.execute(f"ALTER TABLE {current_table} ADD id int(5) NOT NULL PRIMARY KEY AUTO_INCREMENT FIRST")
    conn.commit()
    c.close()
    conn.close()

# #df_f['Datetime'].to_csv(f'C:\\Users\\KIMERA\\Desktop\\energy meter downloads and config\\cewe mutundwe - kawanda\\dfdate.csv')
df_f.to_csv(f'C:\\Users\\KIMERA\\Desktop\\energy meter downloads and config\\cewe mutundwe - kawanda\\dfxx.csv')