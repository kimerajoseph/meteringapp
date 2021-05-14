import pandas as pd
import openpyxl
import os
import pymysql
import calendar

#connect to database
conn = pymysql.connect(host='localhost', port=3306,
                           user='root', password='', database='meteringdatabase')
c = conn.cursor()
df = pd.read_sql(sql="select Energy_For, Rate_1,Rate_2,Rate_3,Rate_4,Rate_5,Rate_6 from uetcl0102_historical_data", con=conn)

months = df['Energy_For'][:-1]
#print(months)
new_df = df.drop('Energy_For',axis=1)
#new_df.apply(lambda x: x.str.replace(',', '').astype(float), axis=1)
new_df['Rate_1'] = df['Rate_1'].str.replace(',', '').astype(float)
new_df['Rate_2'] = df['Rate_2'].str.replace(',', '').astype(float)
new_df['Rate_3'] = df['Rate_3'].str.replace(',', '').astype(float)
new_df['Rate_4'] = df['Rate_4'].str.replace(',', '').astype(float)
new_df['Rate_5'] = df['Rate_5'].str.replace(',', '').astype(float)
new_df['Rate_6'] = df['Rate_6'].str.replace(',', '').astype(float)

numx = len(new_df.index) #number of months

print(len(new_df.index))
columns = list(new_df)
data = []
for i in range(1,int(numx)):
    values = new_df.loc[i-1] - new_df.loc[i]
    zipped = zip(columns, values)
    a_dictionary = dict(zipped)
    data.append(a_dictionary)

newx = pd.DataFrame(data)
  #subtract dataframes

#second table
df_2 = pd.read_sql(sql="select Energy_For, Rate_1,Rate_2,Rate_3,Rate_4,Rate_5,Rate_6 from uetcl0102", con=conn)
months = df_2['Energy_For'][:-1]
#print(months)
new_df_2 = df.drop('Energy_For',axis=1)
#new_df.apply(lambda x: x.str.replace(',', '').astype(float), axis=1)
new_df_2['Rate_1'] = df['Rate_1'].str.replace(',', '').astype(float)
new_df_2['Rate_2'] = df['Rate_2'].str.replace(',', '').astype(float)
new_df_2['Rate_3'] = df['Rate_3'].str.replace(',', '').astype(float)
new_df_2['Rate_4'] = df['Rate_4'].str.replace(',', '').astype(float)
new_df_2['Rate_5'] = df['Rate_5'].str.replace(',', '').astype(float)
new_df_2['Rate_6'] = df['Rate_6'].str.replace(',', '').astype(float)

numx = len(new_df_2.index) #number of months

print(len(new_df_2.index))
columns = list(new_df_2)
data = []
for i in range(1,int(numx)):
    values = new_df_2.loc[i-1] - new_df_2.loc[i]
    zipped = zip(columns, values)
    a_dictionary = dict(zipped)
    data.append(a_dictionary)

newx_2 = pd.DataFrame(data)
final_df = (newx_2.reindex_like(newx).fillna(0) - newx.fillna(0).fillna(0))

#mergedStuff = pd.merge(df, df_2, on=['Energy_For'], how='inner')
#print(mergedStuff.head())
xl = df['Energy_For'].isin(df_2['Energy_For']).value_counts()
print(xl)

newx.insert(0, "Energy_For", months, True)
newx.to_excel("E:\\METERING DATABASE\\metering_database\\pdf_analysis\\diff.xlsx",sheet_name='Sheet1')
new_df = new_df.append(data, True)
mn = new_df.to_excel("E:\\METERING DATABASE\\metering_database\\pdf_analysis\\out.xlsx",sheet_name='Sheet1')
print (final_df)
newx_2.insert(0, "Energy_For", months, True)
newx_2.to_excel("E:\\METERING DATABASE\\metering_database\\pdf_analysis\\diff_2.xlsx",sheet_name='Sheet1')
final_df.insert(0, "Energy_For", months, True)
final_df.to_excel("E:\\METERING DATABASE\\metering_database\\pdf_analysis\\final_df.xlsx",sheet_name='Sheet1')
conn.commit()
c.close()
conn.close()