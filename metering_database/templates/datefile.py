# manu_list_mm = [[0], [5], [0], [0], [18], [6], [7], [0], [2], [1], [0], [2]]
#
# manu_list_ch = [[0], [5], [0], [0], [18], [8], [4], [0], [2], [1], [0], [2]]
# result_1 = sum(manu_list_mm, [])
# result_2 = sum(manu_list_ch, [])
# final = [x + y for x, y in zip(result_1, result_2)]
# print(final)
# print(result_1)
# print(result_2)
# import datetime
# year_list = []
#
# unix = datetime.datetime.now().year
# for i in range(0,4):
#     yearr = unix - i
#     year_list.append(yearr)
# print(year_list)
#
# month_list = []
# import calendar
# for month in calendar.month_name:
#     month_list.append(month)
#
# print(month_list[1:])
# year_list = []
# unix = datetime.datetime.now().year
# for i in range(0,4):
#     yearr = unix - i
#     year_list.append(yearr)
# print(year_list)
# print(calendar.month_name(2019))
# print(calendar.month(2020,4,2,1))
# import pymysql
# from datetime import datetime
# import pandas as pd
# conn = pymysql.connect(host='database-1.cjvdavipre6m.us-west-2.rds.amazonaws.com', port=3306,
#                            user='root', password='uxiGJV2uwUWAS533CRDd', database='meteringdatabase')
# c = conn.cursor
# df_2 = pd.read_sql(sql="select date,end_time, PW, P_var FROM UETCL0102_load_profile", con=conn)
# df_2.reset_index(inplace=False)
# df_2['datetime'] = df_2['date'] + df_2['end_time']
# #df_2['date'] = pd.to_datetime(df_2['date']).format("%Y-%m-%d")
# date_list = df_2['date'].tolist()
# # print(date_list)
# datee = []
# for it in date_list:
#     pp = (str(it)).strip()
#     new_date = datetime.strptime(pp,"%Y-%m-%d").date()
#     datee.append(new_date)
# # print(datee)
#
# list1 = df_2['end_time'].tolist()
# time_list = []
# for item in list1:
#     tt = (str(item)).strip()
#     tt_f = tt.split(':')[0]
#     time_list.append(tt_f)
#
# df_2 = df_2.drop(["date"], axis=1)
# # df_2_ftime = pd.DataFrame(time_list)
# # df_2_ftime.columns = ['final_end_time']
# df_2.insert(2,'f_endtime',time_list,True)
# df_2.insert(1,'date',datee,True)
# df_2['date'] = pd.to_datetime(df_2['date'])
#
#
#
# diff =  df_2['date'].iloc[1] - df_2['date'].iloc[-1]
# print(diff)
# date = '2021-01-01'
# date2 = '2021-01-30'
# datex = datetime.strptime(date, "%Y-%m-%d")
# datex2 = datetime.strptime(date2, "%Y-%m-%d")
# print(df_2.info())
#
# dfx = df_2[df_2['date'].dt.strftime('%Y-%m-%d') == date]
# print(dfx)
# #for i in range(0, len(df_2.index)):
# begining = dfx.index[0]
# print(begining)
# dfm = df_2[df_2['date'].between(datex, datex2)]
# print(dfm)
# #row = df.index[df['A'] == 'Billing period start date'].tolist()
#
# #df_2.to_excel("C:\\Users\KIMERA\\Desktop\\energy meter downloads and config\\tt.xlsx")
# #print(df_2)

list1 = ['id', 'time_inserted', 'inserted_by', 'meter_read_by', 'reading_datetime', 'meter_no', 'Energy_For', 'Cum_Import',
         'Cum_Export', 'Apparent_Power', 'Rate_1', 'Rate_2', 'Rate_3', 'Rate_4', 'Rate_5', 'Rate_6', 'Max_Dem_1',
         'Max_Dem1_time', 'Max_Dem_2', 'Max_Dem2_time', 'Max_Dem_3', 'Max_Dem3_time', 'Import_MVArh', 'Export_MVArh',
         'No_of_Resets', 'Last_Reset', 'Power_Down_Count', 'Lst_pwr_dwn_date_and_time', 'prog_count', 'last_prog_date']

list2 = ['Cum_Import',
         'Cum_Export', 'Apparent_Power', 'Rate_1', 'Rate_2', 'Rate_3', 'Rate_4', 'Rate_5', 'Rate_6']
list3 = list(set(list1) - set(list2))
print(list3)
print(len(list3))
print(len(list1) - len(list2))
