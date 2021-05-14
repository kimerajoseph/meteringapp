import pandas as pd
import pymysql
from datetime import datetime
import dateutil

# file =  'E:\\UETCL\\1_PROTECTION\METERING\\landis\\37102133\\billing data.xlsx'
# df = pd.read_excel(file)
# start = datetime.now()
# #print(df)
# print(df.columns)
# #GETTING METER NO
# meter_no = df['Value'][df['Designation'] == 'COSEM logical device name'].values
# print(meter_no[0])
# #GROSS APPARENT POWER
# apparent_import = df['Value'][(df['Designation'] == 'Gross Apparent energy import +VA (QI+QIV)') & (df['Unit'] == 'kVAh')].values
# print(apparent_import[0])
#
# # apparent_export = df['Value'][(df['Designation'] == 'Gross Apparent energy export -VA (QII+QIII)') & (df['Unit'] == 'kVAh')].values
# # print(apparent_export[0])
#
# #GETTING TOTAL EXPORTS & IMPORTS
# total_export = df['Value'][(df['Designation'] == 'Gross Active energy export -A (QII+QIII)') & (df['Unit'] == 'kWh')].values
# print(total_export[0])
# total_import = df['Value'][(df['Designation'] == 'Gross Active energy import +A (QI+QIV)') & (df['Unit'] == 'kWh')].values
# print(total_import[0])
#
# #GETTING DIFFERENT RATES
# rate_1 = df['Value'][(df['Designation'] == 'Active energy import +A (QI+QIV) rate 1') & (df['Unit'] == 'kWh')].values
# print(f'Rate 1: {rate_1[0]}')
# rate_2 = df['Value'][(df['Designation'] == 'Active energy import +A (QI+QIV) rate 2') & (df['Unit'] == 'kWh')].values
# print(f'Rate 2: {rate_2[0]}')
# rate_3 = df['Value'][(df['Designation'] == 'Active energy import +A (QI+QIV) rate 3') & (df['Unit'] == 'kWh')].values
# print(f'Rate 3: {rate_3[0]}')
# rate_4 = df['Value'][(df['Designation'] == 'Active energy export -A (QII+QIII) rate 1') & (df['Unit'] == 'kWh')].values
# print(f'Rate 4: {rate_4[0]}')
# rate_5 = df['Value'][(df['Designation'] == 'Active energy export -A (QII+QIII) rate 2') & (df['Unit'] == 'kWh')].values
# print(f'Rate 5: {rate_5[0]}')
# rate_6 = df['Value'][(df['Designation'] == 'Active energy export -A (QII+QIII) rate 3') & (df['Unit'] == 'kWh')].values
# print(f'Rate 6: {rate_6[0]}')
#
# #GETTING POWER FARLURES FOR VARIOUS PHASES
# L1_power_f = df['Value'][(df['Designation'] == 'Number of power failures L1') & (df['OBIS'] == '0-0:96.7.1')].any()
# print(f'L1 Power Farlure: {L1_power_f[0]}')
# L2_power_f = df['Value'][(df['Designation'] == 'Number of power failures L2') & (df['OBIS'] == '0-0:96.7.2')].any()
# print(f'L2 Power Farlure: {L2_power_f[0]}')
# L3_power_f = df['Value'][(df['Designation'] == 'Number of power failures L3') & (df['OBIS'] == '0-0:96.7.3')].any()
# print(f'L2 Power Farlure: {L3_power_f}')
#
# end = datetime.now()
# elapsed = end - start
# print(f'time taken:{elapsed}')
#
# x = "2018-10-04 09:17:44 (FF)"
# y= '3300.0 (2021-05-01 00:39:00 (00))'
# z =  '600.0 (2021-05-01 02:55:00 (00))'
#
# print(x.rsplit(' ', 1)[0])
# yz = y.partition(' ')[0]
# yzz = y.partition(' ')[2].replace('(','')
# yf = yzz.rsplit(' ',1)[0]
# print(yz)
# print(yzz)
# print(yf)

list = ['kk','ll','llkh']
if 'e' in list:
    print('kintu')

else:
    print('no there')