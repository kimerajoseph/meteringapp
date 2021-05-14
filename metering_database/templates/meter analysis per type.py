import calendar
import pymysql
import pandas as pd

#print(calendar.month(2019,4,4,1))
#print(calendar.calendar(2020))

# conn = pymysql.connect(host='localhost', port=3306,
#                        user='root', password='', database='meteringdatabase')
#global all_main_meters
all_main_meters = []
conn = pymysql.connect(host='database-1.cjvdavipre6m.us-west-2.rds.amazonaws.com', port=3306,
                      user='root', password='uxiGJV2uwUWAS533CRDd', database='meteringdatabase')
c = conn.cursor()
# df = pd.read_sql('SELECT * FROM UETCL0102_monthly',conn)
# df.to_excel('C:\\Users\\KIMERA\Desktop\\Tx_test.xlsx')
# df2 = pd.read_sql("SELECT * FROM meteringdatabase.substation_meters WHERE meter_YOM <2011 and component_name LIKE '%Trf%'", conn)
# print(df2)
# df2.to_excel("C:\\Users\\KIMERA\Desktop\\Tx_rep.xlsx")
# df3 = pd.read_sql('SELECT * FROM ipp_meters where meter_YOM <2011',conn)
# df3.to_excel('C:\\Users\\KIMERA\Desktop\\ipp_replace.xlsx')
df4 = pd.read_sql("SELECT * FROM meteringdatabase.substation_meters WHERE meter_YOM <2011 and component_name LIKE '%Gen%'", conn)
#print(df2)
df4.to_excel("C:\\Users\\KIMERA\Desktop\\bujagali.xlsx")

# #sql = "SELECT start_time, PW FROM uetcl0103 WHERE month = 'September' AND date = '22/09/2020'"
# tables = ['standalone_meters', 'substation_meters', 'ipp_meters']
# for table in tables:
#     #sql = f"select count(*) from {table} where meter_YOM = '2012'"
#     sql = f"select count(*) from {table} "
# #     sql = f"select meter_no from {table}"
#     c.execute(sql)
#     data_all = c.fetchall()
#     print(data_all)
#     for data in data_all:
#         data1 = data[0]
#         all_main_meters.append(data1)
# print(all_main_meters)
#
# print(all_main_meters)
# print(len(all_main_meters))
# sub_meters = []
# sql1 = "select meter_no from substation_meters"
# c.execute(sql1)
# data_all = c.fetchall()
# for data in data_all:
#     data1 = data[0]
#     sub_meters.append(data1)
# print(sub_meters)
# print(len(sub_meters))
#
# standalone = []
# sql2 = "select meter_no from standalone_meters"
# c.execute(sql2)
# data_all = c.fetchall()
# for data in data_all:
#     data1 = data[0]
#     standalone.append(data1)
# print(standalone)
# print(len(standalone))
#
# ipp_meter = []
# sql3 = "select meter_no from standalone_meters"
# c.execute(sql3)
# data_all = c.fetchall()
# for data in data_all:
#     data1 = data[0]
#     ipp_meter.append(data1)
# print(ipp_meter)
# print(len(ipp_meter))
#
# conn.commit()
# c.close()
# conn.close()
# if len(ipp_meter) + len(standalone) + len(sub_meters) == len(all_main_meters):
#     print("TRUE")