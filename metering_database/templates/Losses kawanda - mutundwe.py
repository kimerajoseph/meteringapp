import tabula
import pandas as pd
import pymysql
from sqlalchemy.types import String, SmallInteger,VARCHAR,INT,Float
from datetime import datetime
from sqlalchemy import create_engine

file = "C:\\Users\\KIMERA\Desktop\\energy meter downloads and config\\cewe mutundwe - kawanda\\Mutundwe at Kawanda.pdf"

# GETTING METER NUMBER
dfmn = tabula.read_pdf(file, pages='1', guess=False)
colx = dfmn[0].columns.tolist()
global meter_no
for item in colx:
    if item.find('Logger') != -1:
        #print(item)
        meter_no = item.split()[1]
        print(meter_no)
    break
df = tabula.read_pdf(file, pages='all', guess=True)
leng = len(df)
#print(leng)
df0 = df[0]
col_len = len(df0.columns.tolist())
col_names = df0.columns.tolist()
#print(col_names)
global df_final
for i in range(1, leng):
    dfc = df[i]
    dfc_len = len(dfc.columns.tolist())
    #print(len(dfc.columns.tolist()))
    diff = dfc_len - col_len
    #print(diff)
    dfc.drop(dfc.iloc[:, 1:diff + 1], inplace=True, axis=1)
    dfc.columns = col_names
    df_final = pd.concat([df0, dfc], axis=0)
    df0 = df_final
    #dfc.to_csv(f'C:\\Users\\KIMERA\\Desktop\\energy meter downloads and config\\KIM MARCH 2021\\df{i}.csv')
    df0.append(dfc)
#df0.to_csv("C:\\Users\\KIMERA\Desktop\\energy meter downloads and config\\cewe mutundwe - kawanda\\Mutundwe at Kawanda.csv")
# DF0 IS DF_FINAL
df0.drop(df0.columns[1], inplace=True, axis=1)

df0 = df0.iloc[2:]
#df0.to_csv("C:\\Users\\KIMERA\Desktop\\energy meter downloads and config\\cewe mutundwe - kawanda\\Mutundwe at Kawanda12.csv")
# RESETTING PANDAS DF INDEX
df0.reset_index(inplace=True, drop=True)
# final_column_names = ['Datetime', 'V(L1-L2)', 'V(L2-L3)', 'V(L3-L1)', 'I_A', 'I_C', 'Phase Angle', 'PF', 'Freq',
#                       'V_THD(All)',
#                       'I_THD(All)', 'P_kW', 'P_kVAr', 'P_kVA']
final_column_names = ['Datetime','P_kW','P_kVAr','I_T','V_T','V_THD(All)','PF','Freq']
df0.columns = final_column_names

inserted_by = 'admin'
#CONVERTING DATE COLUMN TO DATETIME
df0 = df0.iloc[1:]
df0['Datetime'] = pd.to_datetime(df0['Datetime'])
# df0['Mon_Year'] = df0['Datetime'].dt.strftime('%B %Y')
month_year = df0['Datetime'].dt.strftime('%B %Y').tolist()
#print(month_year)
#time_stamp = datetime.now()
time_stamp = datetime.now().__format__("%Y-%m-%d %H:%M")
insert_list = [inserted_by] * len(df0.index)
timestamp_l = [time_stamp] * len(df0.index)
df0.insert(0, 'inserted_by', insert_list, True)
df0.insert(1, 'Timestamp', timestamp_l, True)
df0.insert(3, 'month_year', month_year)
startx = df0['month_year'].iloc[0]
endx = df0['month_year'].iloc[-1]

df0.to_csv("C:\\Users\\KIMERA\Desktop\\energy meter downloads and config\\cewe mutundwe - kawanda\\Mutundwe at Kawanda12.csv")
# #print(len(df0.index))
#df0.to_csv(f'{temp_store}/{meter_no}_{startx}_{endx}_load_profile.csv')
#df0.to_csv("C:\\Users\\KIMERA\Desktop\\energy meter downloads and config\\cewe mutundwe - kawanda\\Mutundwe at Kawanda.csv")
engine = create_engine(
    'mysql://root:uxiGJV2uwUWAS533CRDd@database-1.cjvdavipre6m.us-west-2.rds.amazonaws.com:3306/meteringdatabase')
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
    df0.to_sql(f'{current_table}', con=engine, if_exists='append', index=False,
    dtype={'inserted_by': VARCHAR(length=10),'Timestamp': VARCHAR(length=20),'Datetime': VARCHAR(length=30),
           'month_year': VARCHAR(length=30),'P_kW': Float(),'P_kVAr': Float(), 'I_T': Float(),
           'V_T': Float(), 'V_THD(All)': VARCHAR(length=5), 'PF': Float(), 'Freq': Float()})

else:
    df0.to_sql(f'{current_table}', con=engine, if_exists='append', index=False,
               dtype={'inserted_by': VARCHAR(length=10), 'Timestamp': VARCHAR(length=20),
                      'Datetime': VARCHAR(length=30),
                      'month_year': VARCHAR(length=30), 'P_kW': Float(), 'P_kVAr': Float(), 'I_T': Float(),
                      'V_T': Float(), 'V_THD(All)': VARCHAR(length=5), 'PF': Float(), 'Freq': Float()})

    c.execute(f"ALTER TABLE {current_table} ADD id int(5) NOT NULL PRIMARY KEY AUTO_INCREMENT FIRST")
conn.commit()
c.close()
conn.close()