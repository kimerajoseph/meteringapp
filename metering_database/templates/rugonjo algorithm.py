import pandas as pd

df = pd.read_csv("E:\\UETCL\\1_PROTECTION\METERING\\Mpanga Dam\SOLUTION\\Sample Data Logger.csv") #READING THE CSV FILE
colss = df.columns.tolist()

new_cols = df.loc[df[colss[1]] == 'Interval Start']

name_list = []
for i in df.iloc[6]:
    name_list.append(i)

new_df = df.iloc[7:]
new_df.columns = [name_list] #ASSIGNING NEW COLUMN NAMES TO THE DATAFRAME

new_df['Active(I) Total'] = new_df['Active(I) Total'].astype(float)
new_df['Power Factor-L1'] = new_df['Power Factor-L1'].astype(float)
new_df['Power Factor-L1'] = new_df['Power Factor-L1'].abs()
new_df['Voltage-L1'] = new_df['Voltage-L1'].astype(float)
new_df['Voltage-L1'] = new_df['Voltage-L1'].abs()

new_df['Active(I) Total'] = new_df['Active(I) Total'] - 60000

#CONVERT COLUMN TO FLOAT
new_df['Active(I) Total'] = new_df['Active(I) Total'].astype(float)

#GETTING VALUES ABOVE 4.5 MW
loss_df = new_df[new_df['Active(I) Total'].values > 45000]
#loss_df.reset_index(drop=True,inplace=False)
loss_df.to_csv("E:\\UETCL\\1_PROTECTION\METERING\\Mpanga Dam\SOLUTION\\lossES.csv")

#CHECKING IF THERE IS ADVANCE OR NOT. CHECK IF DATAFRAME IS EMPTY
if loss_df.empty == False:
    #GETTING ADDITIONAL LOAD
    loss_df['additional_load'] = loss_df['Active(I) Total'] - 45000

    #COMPUTING P=1.73*V*PF
    loss_df['comb'] = loss_df.apply(lambda row: (row['Power Factor-L1']*row['Voltage-L1']*1.73),axis=1)

    #ELIMINATING VALUES WHERE P=1.73*V*PF IS 0
    loss_dfx = loss_df[loss_df['comb'].values != 0]
    loss_dfx['Add_I'] = loss_dfx.apply(lambda row: (row['additional_load']/row['comb']),axis=1) #CURRENT DUE TO EXTRA LOAD
    loss_dfx['I_Squared'] = loss_dfx.apply(lambda row: (row['Add_I']*row['Add_I']),axis=1)
    loss_dfx['Interval Start']=loss_dfx['Interval Start'].replace(':','.',regex = True)
    loss_dfx['Interval Start']=loss_dfx['Interval Start'].astype(float)

    #SETTING R AND COMPUTING POWER WHERE INTERVALS ARE 1 HOUR
    r = float(6.8)
    t = 1
    loss_dfx['Power_loss']= loss_dfx.apply(lambda row: (row['I_Squared']*r*t),axis=1)

    #GETTING THE VARIOUS RATES
    rate_3 = loss_dfx[(loss_dfx['Interval Start'].values >= 0) & (loss_dfx['Interval Start'].values <= 5)]
    rate_1 = loss_dfx[(loss_dfx['Interval Start'].values >= 6) & (loss_dfx['Interval Start'].values <= 11)]
    rate_2 = loss_dfx[(loss_dfx['Interval Start'].values >= 12) & (loss_dfx['Interval Start'].values <= 23)]
    #print(loss_dfx.dtypes)

    #ERROR AND EXCEPTIONS HANDLING
    if len(loss_dfx.index) == len(rate_1.index) + len(rate_2.index) + len(rate_3.index):
        rate_1_sum = rate_1['Power_loss'].sum().values
        rate_2_sum = rate_2['Power_loss'].sum().values
        rate_3_sum = rate_3['Power_loss'].sum().values

        rate_1_sum_f = round(rate_1_sum[0],3)
        rate_2_sum_f = round(rate_2_sum[0], 3)
        rate_3_sum_f = round(rate_3_sum[0], 3)
        print(f"RATE 1 IS: {rate_1_sum_f}")
        print(f"RATE 2 IS: {rate_2_sum_f}")
        print(f"RATE 3 IS: {rate_3_sum_f}")

    else:
        print("THERE IS A MISTAKE")

    # loss_dfx.to_csv("E:\\UETCL\\1_PROTECTION\METERING\\Mpanga Dam\SOLUTION\\loss_df.csv")
    # rate_3.to_csv("E:\\UETCL\\1_PROTECTION\METERING\\Mpanga Dam\SOLUTION\\rate_3.csv")
    # rate_2.to_csv("E:\\UETCL\\1_PROTECTION\METERING\\Mpanga Dam\SOLUTION\\rate_2.csv")
    # rate_1.to_csv("E:\\UETCL\\1_PROTECTION\METERING\\Mpanga Dam\SOLUTION\\rate_1.csv")

else:
    print("THERE IS NO ADVANCE")
    rate_1 = 0
    rate_2 = 0
    rate_3 = 0