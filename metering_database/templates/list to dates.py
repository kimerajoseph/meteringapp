listw =['2021/1/1', '2021/01/17', '2021/01/17', '2021/01/17', '2021/01/17', '2021/01/17',
                            '2021/1/7', '2021/01/17', '2021/01/17']
from datetime import datetime,date
from datetime import timedelta
#import datetime
import pandas as pd
import time

mlist = []
for l in listw:
    new_l = datetime.strptime(l , "%Y/%m/%d").date()
    print(new_l)
    #mlist.append(datetime(new_l))

print(mlist)
my_df = []
start_date = date(2020,10,22)
end_date = date(2020,11,22)
print(end_date - start_date)
print(start_date)
print(end_date)
#d_list = pd.date_range(start_date,end_date).tolist()
delta = end_date  - start_date # as timedelta
print(f"this is the start of : {end_date}")
df = pd.read_excel('C:\\Users\\KIMERA\\Desktop\\1.xlsx')
print(df)

diff = df['date'].iloc[1] - df['date'].iloc[90]
#print(diff)
global begin, ending
for i in range(0,len(df.index)):
    if df['date'].iloc[i] == start_date:
        print(f"These dates {start_date} are the same as {df['date'].iloc[i]}")
        begin = df['Unnamed: 0'].iloc[i]
        print(df['Unnamed: 0'].iloc[i])
        end_date = start_date + timedelta(days=1)
        print(end_date)
        break

for i in range(0, len(df.index)):
    if df['date'].iloc[i] == end_date:
        print(f"These dates {end_date} are the same as {df['date'].iloc[i]}")
        ending = df['Unnamed: 0'].iloc[i]
        print(df['Unnamed: 0'].iloc[i])
        break
new_df = df.iloc[begin:ending]
new_df.drop('Unnamed: 0', axis = 1)
#new_df.reset_index(inplace= False)
#print(new_df)
