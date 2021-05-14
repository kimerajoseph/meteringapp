import pandas as pd
import pymysql
from datetime import datetime
import dateutil
from dateutil.relativedelta import relativedelta

file =  'E:\\UETCL\\1_PROTECTION\METERING\\landis\\37102133\\billing data.xlsx'
df = pd.read_excel(file)
start = datetime.now()
#print(df)
col_list = df.columns.tolist()

#GETTING METER NO
meter_no = df['Value'][(df['Designation'] == 'COSEM logical device name') & (df['OBIS'] == '0-0:42.0.0')].any()
print(meter_no)
#GROSS APPARENT POWER
apparent_import = df['Value'][(df['Designation'] == 'Gross Apparent energy import +VA (QI+QIV)') & (df['Unit'] == 'kVAh')
& (df['OBIS'] == '1-1:9.8.0')].any()
print(apparent_import)

# apparent_export = df['Value'][(df['Designation'] == 'Gross Apparent energy export -VA (QII+QIII)') & (df['Unit'] == 'kVAh')].any()
# print(apparent_export)

#GETTING TOTAL EXPORTS & IMPORTS
total_export = df['Value'][(df['Designation'] == 'Gross Active energy export -A (QII+QIII)') & (df['Unit'] == 'kWh')
& (df['OBIS'] == '1-1:2.8.0')].any()
print(total_export)
total_import = df['Value'][(df['Designation'] == 'Gross Active energy import +A (QI+QIV)') & (df['Unit'] == 'kWh')
& (df['OBIS'] == '1-1:1.8.0')].any()
print(total_import)

#GETTING DIFFERENT RATES
rate_1 = df['Value'][(df['Designation'] == 'Active energy import +A (QI+QIV) rate 1') & (df['Unit'] == 'kWh')
& (df['OBIS'] == '1-1:1.8.1')].any()
print(f'Rate 1: {rate_1}')
rate_2 = df['Value'][(df['Designation'] == 'Active energy import +A (QI+QIV) rate 2') & (df['Unit'] == 'kWh')
& (df['OBIS'] == '1-1:1.8.2')].any()
print(f'Rate 2: {rate_2}')
rate_3 = df['Value'][(df['Designation'] == 'Active energy import +A (QI+QIV) rate 3') & (df['Unit'] == 'kWh')
& (df['OBIS'] == '1-1:1.8.3')].any()
print(f'Rate 3: {rate_3}')
rate_4 = df['Value'][(df['Designation'] == 'Active energy export -A (QII+QIII) rate 1') & (df['Unit'] == 'kWh')
& (df['OBIS'] == '1-1:2.8.1')].any()
print(f'Rate 4: {rate_4}')
rate_5 = df['Value'][(df['Designation'] == 'Active energy export -A (QII+QIII) rate 2') & (df['Unit'] == 'kWh')
& (df['OBIS'] == '1-1:2.8.2')].any()
print(f'Rate 5: {rate_5}')
rate_6 = df['Value'][(df['Designation'] == 'Active energy export -A (QII+QIII) rate 3') & (df['Unit'] == 'kWh')
& (df['OBIS'] == '1-1:2.8.3')].any()
print(f'Rate 6: {rate_6}')

#GETTING POWER FARLURES FOR VARIOUS PHASES
L1_power_f = df['Value'][(df['Designation'] == 'Number of power failures L1') & (df['OBIS'] == '0-0:96.7.1')].any()
print(f'L1 Power Farlure: {L1_power_f}')
L2_power_f = df['Value'][(df['Designation'] == 'Number of power failures L2') & (df['OBIS'] == '0-0:96.7.2')].any()
print(f'L2 Power Farlure: {L2_power_f}')
L3_power_f = df['Value'][(df['Designation'] == 'Number of power failures L3') & (df['OBIS'] == '0-0:96.7.3')].any()
print(f'L2 Power Farlure: {L3_power_f}')

#CHECKING CONFIG COUNT
config_count= df['Value'][(df['Designation'] == 'Number of parameterisations (configuration program changes)')
                          & (df['OBIS'] == '0-0:96.2.0')].any()
print(f'config_count: {config_count}')
last_config_date_x= df['Value'][(df['Designation'] == 'Date of last parameterisation (configuration program change)')
                          & (df['OBIS'] == '0-0:96.2.1')].any()
last_config_date = last_config_date_x.rsplit(' ', 1)[0]
print(f'last_config_date: {last_config_date}')

#MAXIMUM DEMANDS
import_max_DD_x= df['Value'][(df['Designation'] == 'Maximum demand +A (QI+QIV)') & (df['Unit'] == 'kW')
                           & (df['OBIS'] == '1-1:1.6.0')].any()
import_max_DD = import_max_DD_x.partition(' ')[0]  #GETTING IMPORT MAX DD
yzz = import_max_DD_x.partition(' ')[2].replace('(','')
imp_max_dd_datetime = yzz.rsplit(' ',1)[0]              #IMPORT MAX DD DATETIME
print(f'import_max_DD: {import_max_DD}')
print(f'imp_max_dd_datetime: {imp_max_dd_datetime}')


export_max_DD_x= df['Value'][(df['Designation'] == 'Maximum demand -A (QII+QIII)') & (df['Unit'] == 'kW')
                           & (df['OBIS'] == '1-1:2.6.0')].any()
export_max_DD = export_max_DD_x.partition(' ')[0]  #GETTING EXPORT MAX DD
yzx = export_max_DD_x.partition(' ')[2].replace('(','')
exp_max_dd_datetime = yzx.rsplit(' ',1)[0]              #EXPORT MAX DD DATETIME
print(f'export_max_DD: {export_max_DD}')
print(f'exp_max_dd_datetime: {exp_max_dd_datetime}')


#GETTING BILLING RESETS
billing_resets= df['Value'][(df['Designation'] == 'Billing period reset counter') & (df['OBIS'] == '1-0:0.1.0')].any()
print(f'billing_resets: {billing_resets}')

#READING DATETIME
read_datetime_x= df['Value'][(df['Designation'] == 'Clock') & (df['OBIS'] == '0-0:1.0.0')].any()
read_datetime = read_datetime_x.rsplit(' ', 1)[0]
print(f'billing_resets: {read_datetime}')

#GETTING TIME STAMP
time_stamp = now = datetime.now().__format__("%Y-%m-%d %H:%M")

#BILLING PERIOD
bill_date_x= df['Value'][(df['Designation'] == 'Date of last billing period reset') & (df['OBIS'] == '1-0:0.1.2')].any()
date_x = bill_date_x.partition(' ')[0]
new_date = datetime.strptime(date_x, '%Y-%m-%d').date()
a_month = dateutil.relativedelta.relativedelta(months=1)
month_year = new_date - a_month
billing_period = month_year.strftime('%B_%Y')
print(f'billing_period: {billing_period}')

# #CREATING A DATAFRAME FROM THE DATA
# list_1 = ['time_stamp','read_datetime','billing_period','billing_resets','apparent_import','total_export','total_import','rate_1','rate_2','rate_3','rate_4','rate_5','rate_6','import_max_DD',
#           'imp_max_dd_datetime','export_max_DD','exp_max_dd_datetime','config_count','last_config_date']
# list_2 = [time_stamp,read_datetime,billing_period,billing_resets,apparent_import,total_export,total_import,rate_1,rate_2,rate_3,rate_4,rate_5,rate_6,import_max_DD,imp_max_dd_datetime,
#           export_max_DD,exp_max_dd_datetime,config_count,last_config_date]

inserted_by  = 'admin'
#INSERTING INTO THE DATABASE
conn = pymysql.connect(host='database-1.cjvdavipre6m.us-west-2.rds.amazonaws.com', port=3306,
                             user='root', password='uxiGJV2uwUWAS533CRDd', database='meteringdatabase')
c = conn.cursor()
c.execute(f"""CREATE TABLE IF NOT EXISTS {meter_no} (id int(5) NOT NULL AUTO_INCREMENT PRIMARY KEY,time_stamp VARCHAR(20),
inserted_by varchar(10),meter_read_by varchar(10),read_datetime varchar(20),billing_period varchar(20),
billing_resets int(5),apparent_import VARCHAR(13),total_export VARCHAR(13),total_import VARCHAR(13),Rate_1 VARCHAR(13),Rate_2 VARCHAR(13),
Rate_3 VARCHAR(13),Rate_4 VARCHAR(13),Rate_5 VARCHAR(13),Rate_6 VARCHAR(13),import_max_DD VARCHAR(13),imp_max_dd_datetime VARCHAR(20),
export_max_DD VARCHAR(13),exp_max_dd_datetime VARCHAR(20),config_count VARCHAR(13),last_config_date VARCHAR(20))""")

sql = f"""INSERT INTO {meter_no} (time_stamp,inserted_by,meter_read_by,read_datetime,billing_period, billing_resets,apparent_import,
total_export,total_import,Rate_1,Rate_2,Rate_3,Rate_4,Rate_5,Rate_6,import_max_DD,imp_max_dd_datetime,export_max_DD,exp_max_dd_datetime,
config_count,last_config_date)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
val = (time_stamp,inserted_by,inserted_by,read_datetime,billing_period,billing_resets,apparent_import,total_export,total_import,rate_1,
       rate_2,rate_3,rate_4,rate_5,rate_6,import_max_DD,imp_max_dd_datetime,export_max_DD,exp_max_dd_datetime,config_count,last_config_date)
c.execute(sql,val)
conn.commit()
c.close()
conn.close()
end = datetime.now()
elapsed = end - start
print(f'time taken:{elapsed}')

