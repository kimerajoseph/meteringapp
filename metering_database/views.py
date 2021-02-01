from django.shortcuts import render
from django.http import HttpResponse, request
import datetime
from datetime import datetime,date
import time
import pymysql
import pandas as pd
import openpyxl as py
from pygrok import Grok
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import AnonymousUser
import openpyxl as xl
#import datetime
import xlsxwriter
from sqlalchemy import create_engine
from sqlalchemy.types import String, SmallInteger,VARCHAR
import matplotlib.pyplot as plt
import mpld3
from django.core.files.storage import FileSystemStorage
import io
import calendar



def index(request):
    return render(request, 'index.html')

def homepage(request):
    #user = user_act
    #user = active_user
    return render(request, 'index.html')

def welcome(request):
    if request.method == 'POST':
        user_act = request.POST['username']
        password_given = request.POST['password']
        user = authenticate(username = user_act, password = password_given)
        #if user.is_authenticated == True:
        if user is not None:
            global active_user
            active_user = user_act
            AnonymousUser = user
            return render(request, 'welcome.html',{'user':user})

        else:
            error = 'Please check your username and password'
            return render(request, 'index.html', {'error':error})


def meterrecord(request):  #inserting meter records for standalone meter
    if request.method == 'POST':
        unix = datetime.now().replace (microsecond=0)
        time_added = unix
        #date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
        village = request.POST['village_st']
        subcounty = request.POST['sub_county_st']
        district = request.POST['district_st']
        region = request.POST['region_st']
        x_cordinates = request.POST['x_cordinates_st']
        y_cordinates = request.POST['y_cordinates_st']
        feeder_name = request.POST['feeder_name_st']
        voltage = request.POST['voltage_st']

        distributor_1 = request.POST['distributor_1']
        distributor_2 = request.POST['distributor_2']
        meter_owner = request.POST['meter_owner_st']


        manu_st = request.POST['manu_meter_st'] #second take
        unit_type = request.POST['meter_type_st']
        D_O_M = request.POST['DOM_st']
        MU_Serial_No = request.POST['mu_meter_no_st']
        no_of_elements = request.POST['elements_st']
        wired_as = request.POST['wired_as_st']
        comm_date = request.POST['comm_date_st']
        DLP = request.POST['DLP_st']
        metering_cores = request.POST['meter_cores_st']
        CTratios = request.POST['core_ratios_st']
        core_used = request.POST['core_used_st']
        core_used_accuracy = request.POST['accuracy_st']
        avail_spares = request.POST['avail_spares_st']
        spares_class = request.POST['spares_class_st']
        VTratio = request.POST['vt_ratio_st']
        VT_accuracy = request.POST['vt_accuracy_st']
        #meter_no = request.POST['meter_no_st']
        #global meter_no
        #meter_no = request.POST['meter_no']
        global active_user
        added_by = active_user
        #global meter

        meter_manuf = request.POST['energy_meter_manu'] #main energy meter details
        meter_type = request.POST['energy_meter_type']
        meter_no = request.POST['energy_meter_no']
        Y_O_M = request.POST['meter_YOM']
        meter_accuracy = request.POST['e_meter_accuracy']
        no_of_meter_elements = request.POST['e_meter_elements']
        meter_wired_as = request.POST['e_meter_wired']
        meter_install_date = request.POST['e_instal_date']
        meter_decom_date = request.POST['e_decom_date']
        access = request.POST['access']
        IP_Address = request.POST['ip_address']
        avail_interfaces = request.POST['interfaces']
        comm_protocol = request.POST['comm_protocol']
        comm_protocol_used = request.POST['comm_protocol_used']

        meter_manuf_ch = request.POST['energy_meter_manu_ch']  # main energy meter details
        meter_type_ch = request.POST['energy_meter_type_ch']
        meter_no_ch = request.POST['energy_meter_no_ch']
        Y_O_M_ch = request.POST['meter_YOM_ch']
        meter_accuracy_ch = request.POST['e_meter_accuracy_ch']
        no_of_meter_elements_ch = request.POST['e_meter_elements_ch']
        meter_wired_as_ch = request.POST['e_meter_wired_ch']
        meter_install_date_ch = request.POST['e_instal_date_ch']
        meter_decom_date_ch = request.POST['e_decom_date_ch']
        access_ch = request.POST['access_ch']
        IP_Address_ch = request.POST['ip_address_ch']
        avail_interfaces_ch = request.POST['interfaces_ch']
        comm_protocol_ch = request.POST['comm_protocol_ch']
        comm_protocol_used_ch = request.POST['comm_protocol_used_ch']


        conn = pymysql.connect(host='localhost', port=3306, user='root', password='', database='meteringdatabase')
        c = conn.cursor()
        sql_1 = """INSERT INTO standalone_meter_details (time_added,added_by,village,subcounty,district,region,x_cordinates,y_cordinates,feeder_name,
         voltage,distributor_1,distributor_2,meter_owner,manufacturer,unit_type,D_O_M,MU_Serial_No,no_of_elements,wired_as,comm_date,DLP,metering_cores,CTratios,
          core_used,core_used_accuracy,avail_spares,spares_class,VTratio,VT_accuracy,meter_manuf,meter_type,meter_no,Y_O_M,meter_accuracy,no_of_meter_elements,
          meter_wired_as,meter_install_date,meter_decom_date,access,IP_Address,avail_interfaces,comm_protocol,comm_protocol_used,meter_manuf_ch,meter_type_ch,meter_no_ch,
          Y_O_M_ch,meter_accuracy_ch,no_of_meter_elements_ch,meter_wired_as_ch,meter_install_date_ch,meter_decom_date_ch,access_ch,IP_Address_ch,avail_interfaces_ch,comm_protocol_ch,
          comm_protocol_used_ch) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (unix,added_by,village,subcounty,district,region,x_cordinates,y_cordinates,feeder_name,voltage,distributor_1,distributor_2,meter_owner,manu_st,
                  unit_type,D_O_M,MU_Serial_No,no_of_elements,wired_as,comm_date,DLP,metering_cores,CTratios,core_used,core_used_accuracy,avail_spares,spares_class,VTratio,VT_accuracy,
                  meter_manuf,meter_type,meter_no,Y_O_M,meter_accuracy,no_of_meter_elements,meter_wired_as,meter_install_date,meter_decom_date,access,IP_Address,avail_interfaces,
                  comm_protocol,comm_protocol_used,meter_manuf_ch,meter_type_ch,meter_no_ch,Y_O_M_ch,meter_accuracy_ch,no_of_meter_elements_ch,meter_wired_as_ch,
                  meter_install_date_ch,meter_decom_date_ch,access_ch,IP_Address_ch,avail_interfaces_ch,comm_protocol_ch,comm_protocol_used_ch)
        c.execute(sql_1, values)
        c.close()
        conn.commit()
        conn.close()
        return render(request, 'form_success.html')

def sub_meterrecord(request):  #inserting substationo meter records
    if request.method == 'POST':
        unix = datetime.now().replace (microsecond=0)
        time_added = unix

        #date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
        substation = request.POST['sub']
        voltage = request.POST['voltage']
        district = request.POST['sub_dist']
        region = request.POST['sub_region']
        x_cordinates = request.POST['sub_cord_x']
        y_cordinates = request.POST['sub_cord_y']
        feeder_name = request.POST['sub_feeder'] #second take
        feeder_voltage = request.POST['sub_feeder_voltage']
        meter_owner = request.POST['sub_meter_owner']
        distributor = request.POST['distributor']
        contractor = request.POST['subs_contractor']
        ct_manufacturer = request.POST['sub_ct_manu'] #Third take
        ct_type = request.POST['sub_ct_type']
        no_ct_cores = request.POST['sub_ct_cores']
        ct_ratios = request.POST['sub_ct_core_ratios']
        core_used = request.POST['sub_core_used']
        accuracy_class = request.POST['sub_accuracy_class']
        avail_spares = request.POST['sub_avail_spares']
        spares_class = request.POST['sub_spares_class']
        VT_manufacturer = request.POST['sub_vt_manu']
        VT_type = request.POST['sub_VT_type']
        VT_ratio = request.POST['sub_vt_ratio']
        VT_accuracy = request.POST['sub_vt_accuracy']
        meter_manufacturer = request.POST['sub_meter_manu'] #fourth take
        meter_type = request.POST['sub_meter_type']
        meter_no = request.POST['sub_meter_no']
        meter_YOM = request.POST['sub_YOM']
        meter_accuracy_class = request.POST['sub_meter_acc_class']
        no_of_elements = request.POST['sub_meter_elements']
        wired_as = request.POST['sub_meter_wire']
        meter_install_date = request.POST['sub_meter_install_date']
        meter_decom_date = request.POST['sub_meter_decom_date']
        access = request.POST['sub_meter_access']
        IP_Address = request.POST['sub_ip_address']
        avail_interfaces = request.POST['sub_meter_interfaces']
        comm_protocols = request.POST['sub_meter_comm_protocols']
        protocol_used = request.POST['sub_meter_protocol_used']


        meter_manufacturer_ch = request.POST['sub_meter_manu_ch']  # fifth take
        meter_type_ch = request.POST['sub_meter_type_ch']
        meter_no_ch = request.POST['sub_meter_no_ch']
        meter_YOM_ch = request.POST['sub_YOM_ch']
        meter_accuracy_class_ch = request.POST['sub_meter_acc_class_ch']
        no_of_elements_ch = request.POST['sub_meter_elements_ch']
        wired_as_ch = request.POST['sub_meter_wire_ch']
        meter_install_date_ch = request.POST['sub_meter_install_date_ch']
        meter_decom_date_ch = request.POST['sub_meter_decom_date_ch']
        access_ch = request.POST['sub_meter_access_ch']
        IP_Address_ch = request.POST['sub_ip_address_ch']
        avail_interfaces_ch = request.POST['sub_meter_interfaces_ch']
        comm_protocols_ch = request.POST['sub_meter_comm_protocols_ch']
        protocol_used_ch = request.POST['sub_meter_protocol_used_ch']


        #global meter_no
        #meter_no = request.POST['meter_no']
        global active_user
        added_by = active_user
        #global meter

        conn = pymysql.connect(host='localhost', port=3306, user='root', password='', database='meteringdatabase')
        c = conn.cursor()
        sql_2 = """INSERT INTO substation_meters (time_added,added_by,substation,voltage, district,region,x_cordinates,y_cordinates,feeder_name,feeder_voltage,meter_owner,
                    distributor,contractor,ct_manufacturer,ct_type,no_ct_cores,ct_ratios,core_used,accuracy_class,avail_spares,spares_class,VT_manufacturer,VT_type,VT_ratio,VT_accuracy,
                    meter_manufacturer,meter_type,meter_no,meter_YOM,meter_accuracy_class,no_of_elements,wired_as,meter_install_date,meter_decom_date,access,IP_Address,avail_interfaces,comm_protocols,protocol_used,
                    meter_manufacturer_ch,meter_type_ch,meter_no_ch,meter_YOM_ch,meter_accuracy_class_ch,no_of_elements_ch,wired_as_ch,meter_install_date_ch,meter_decom_date_ch,access_ch,IP_Address_ch,avail_interfaces_ch,comm_protocols_ch,protocol_used_ch) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (unix,added_by,substation,voltage,district,region,x_cordinates,y_cordinates,feeder_name,feeder_voltage,meter_owner,distributor,contractor,
                  ct_manufacturer,ct_type,no_ct_cores,ct_ratios,core_used,accuracy_class,avail_spares,spares_class,VT_manufacturer,VT_type,VT_ratio,VT_accuracy,
                  meter_manufacturer,meter_type,meter_no,meter_YOM,meter_accuracy_class,no_of_elements,wired_as,meter_install_date,meter_decom_date,access,IP_Address,avail_interfaces,comm_protocols,protocol_used,
                  meter_manufacturer_ch,meter_type_ch,meter_no_ch,meter_YOM_ch,meter_accuracy_class_ch,no_of_elements_ch,wired_as_ch,meter_install_date_ch,meter_decom_date_ch,access_ch,IP_Address_ch,avail_interfaces_ch,comm_protocols_ch,protocol_used_ch)

        c.execute(sql_2, values)

        conn.commit()
        c.close()
        conn.close()
        return render(request, 'form_success.html')

def new_submission(request):
    #user = user_act
    #user = active_user
    return render(request, 'welcome.html')

def success(request):
    return render(request, 'uetcl_meter.html')
    #if request.method == 'POST':
        #user = request.POST['username']
        #password_given = request.POST['password']
        #unix = int(time.time())
        #date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
now = datetime.now()
#assigning the excel sheet a dynamic name
xlm = now.strftime('%B')
#import csv
def fillform(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['filename_m']
        uploaded_file_ch = request.FILES['filename_c']
        fs = FileSystemStorage()
        file_m = fs.save(uploaded_file.name, uploaded_file)
        file_ch = fs.save(uploaded_file_ch.name, uploaded_file_ch)
        #filepath = request.FILES['filepath'] if 'filepath' in request.FILES else False
        #if uploaded_file != '' and uploaded_file_ch == '':
        #print(uploaded_file.name)
        #print(uploaded_file.size)

        #with open(f'media/{file1}') as csvfile:
            #csvreader = csv.reader(csvfile)

        fd = pd.read_csv(f'media/{file_m}')
        fd.to_excel(f"files/{xlm}.xlsx", sheet_name='sheet1',
                    index=False)
        #df = pd.DataFrame(fd)
        #print(df)
        workbook = py.load_workbook(f"FILES/{xlm}.xlsx")
        sheet = workbook['sheet1']
        man_value = sheet['B1'].value
        manu = man_value.split()[0]  # meter manufacturer
        # print(manu)
        input_string = str(sheet["B2"].value)
        # global meter
        meter = input_string.split()[0].replace('-', '')  # meter number
        # print(meter)
        read_time = f'{input_string.split()[2]} {input_string.split()[3]}'
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='', database='meteringdatabase')
        c = conn.cursor()
        global meter_no
        # sql_1 = "SELECT CTratio, VTratio FROM meter_details WHERE meter_no=?",((meter,))
        c.execute("SELECT CTratios, VTratio FROM standalone_meter_details WHERE meter_no = %s", meter)
        data = c.fetchone()
        c.close()
        conn.close()
        date_pattern = '%{MONTHNUM:month}/%{MONTHDAY:day}/%{YEAR:year}'
        grok = Grok(date_pattern)
        xl = (grok.match(input_string))
        mm = xl['month']
        dd = xl['day']
        yr = xl['year']
        x = datetime(int(yr), int(mm), int(dd))
        # ll = (x.strftime("%d-%m-%Y"))
        D_O_R = (x.strftime("%d-%b-%Y"))  # reading date
        for r in range(1, sheet.max_row):
            for x in range(1, sheet.max_column):
                cell = sheet.cell(r, x)
                if cell.value == 'Cumulative totals':
                    cell_imp_whr = sheet.cell(r + 3, x + 1)
                    cell_unit = sheet.cell(r + 3, x + 2)
                    cell_expwh_unit = sheet.cell(r + 4, x + 2)
                    if cell_unit.value == 'Import Wh' and cell_expwh_unit.value == 'Export Wh':  # cum import
                        imp_whr = cell_imp_whr.value.replace(',', '')
                        imp_whh = round(float(imp_whr) / 1000000, 3)
                        imp_wh = "{:,}".format(imp_whh)
                        # print(float(imp_wh))

                    cell_exp_whr = sheet.cell(r + 4, x + 1)  # cum export
                    if cell_unit.value == 'Import Wh' and cell_expwh_unit.value == 'Export Wh':
                        exp_whr = cell_exp_whr.value.replace(',', '')
                        exp_whh = round(float(exp_whr) / 1000000, 3)
                        exp_wh = "{:,}".format(exp_whh)

                    cell_app_pow = sheet.cell(r + 9, x + 1)  # getting apparent power
                    cell_app_pow_unit = sheet.cell(r + 9, x + 2)
                    if cell_app_pow_unit.value == 'VAh':
                        app_powr = cell_app_pow.value.replace(',', '')
                        app_powh = round(float(app_powr) / 1000000, 3)
                        app_pow = "{:,}".format(app_powh)
                        # app_pow = float(app_powr)

                    # getting total import and export MVarh
                    unit1_MVArh = sheet.cell(r + 5, x + 2)
                    unit3_MVArh = sheet.cell(r + 7, x + 2)
                    if unit1_MVArh.value == 'Q1 varh' and unit3_MVArh.value == 'Q3 varh':  # getting import MVArh. We add Q1 & Q2
                        imp_MVArh1_r = sheet.cell(r + 5, x + 1).value.replace(',', '')
                        imp_MVArh1 = float(imp_MVArh1_r)
                        imp_MVArh2_r = sheet.cell(r + 7, x + 1).value.replace(',', '')
                        imp_MVArh2 = float(imp_MVArh2_r)
                        total_imp_MVArh_r = round((imp_MVArh1 + imp_MVArh2) / 1000000, 3)

                        total_imp_MVArh = "{:,}".format(total_imp_MVArh_r)

                    unit2_MVArh = sheet.cell(r + 6, x + 2)
                    unit4_MVArh = sheet.cell(r + 8, x + 2)
                    if unit2_MVArh.value == 'Q2 varh' and unit4_MVArh.value == 'Q4 varh':  # getting import MVArh. We add Q3 & Q4
                        exp_MVArh1_r = sheet.cell(r + 6, x + 1).value.replace(',', '')
                        exp_MVArh1 = float(exp_MVArh1_r)
                        exp_MVArh2_r = sheet.cell(r + 8, x + 1).value.replace(',', '')
                        exp_MVArh2 = float(exp_MVArh2_r)
                        total_exp_MVArh_r = round((exp_MVArh1 + exp_MVArh2) / 1000000, 3)
                        total_exp_MVArh = "{:,}".format(total_exp_MVArh_r)

                    # total MVArh
                    total_MVArh_x = float(total_exp_MVArh.replace(',', '')) - float(total_imp_MVArh.replace(',', ''))
                    total_MVArh_xx = round(total_MVArh_x, 3)
                    total_MVArh = "{:,}".format(total_MVArh_xx)

                if cell.value == 'Register':  # getting the various rates
                    unit1 = sheet.cell(r + 1, x + 2)
                    unit2 = sheet.cell(r + 2, x + 2)
                    unit3 = sheet.cell(r + 3, x + 2)
                    if unit3.value == unit2.value == 'Import Wh':
                        rate1_r = sheet.cell(r + 1, x + 1).value.replace(',', '')
                        rate1_rh = round(float(rate1_r) / 1000000, 3)
                        rate1 = "{:,}".format(rate1_rh)

                    if unit1.value == unit3.value == 'Import Wh':
                        rate2_r = sheet.cell(r + 2, x + 1).value.replace(',', '')
                        rate2_rh = round(float(rate2_r) / 1000000, 3)
                        rate2 = "{:,}".format(rate2_rh)

                    if unit2.value == unit1.value == 'Import Wh':
                        rate3_r = sheet.cell(r + 3, x + 1).value.replace(',', '')
                        rate3_rh = round(float(rate3_r) / 1000000, 3)
                        rate3 = "{:,}".format(rate3_rh)

                    unit4 = sheet.cell(r + 4, x + 2)
                    unit5 = sheet.cell(r + 5, x + 2)
                    unit6 = sheet.cell(r + 6, x + 2)
                    if unit5.value == unit6.value == 'Export Wh':
                        rate4_r = sheet.cell(r + 4, x + 1).value.replace(',', '')
                        rate4_rh = round(float(rate4_r) / 1000000, 3)
                        rate4 = "{:,}".format(rate4_rh)

                    if unit4.value == unit6.value == 'Export Wh':
                        rate5_r = sheet.cell(r + 5, x + 1).value.replace(',', '')
                        rate5_rh = round(float(rate5_r) / 1000000, 3)
                        rate5 = "{:,}".format(rate5_rh)

                    if unit4.value == unit5.value == 'Export Wh':
                        rate6_r = sheet.cell(r + 6, x + 1).value.replace(',', '')
                        rate6_rh = round(float(rate6_r) / 1000000, 3)
                        rate6 = "{:,}".format(rate6_rh)

                if cell.value == 'Billing event details':
                    req_cell = sheet.cell(r + 2, x)
                    req_cell1 = sheet.cell(r + 3, x)
                    if req_cell.value == 'Billing reset number:':
                        resets = sheet.cell(r + 2, x + 1).value
                        # no_of_resets = float(no_of_resets_r)

                    if req_cell1.value == 'Time of billing reset:':
                        reset_time = sheet.cell(r + 3, x + 1).value

                if cell.value == 'Billing period start date' and sheet.cell(r + 1,
                                                                            x).value == 'Billing period end date':
                    M_O_S_r = sheet.cell(r + 1, x + 1).value
                    date_pattern = '%{MONTHNUM:month}/%{MONTHDAY:day}/%{YEAR:year}'
                    grok = Grok(date_pattern)
                    xl = (grok.match(M_O_S_r))
                    mm = xl['month']
                    dd = xl['day']
                    yr = xl['year']
                    x = datetime(int(yr), int(mm), int(dd))
                    M_O_S = (x.strftime("%B %Y"))

                if cell.value == 'Cumulative maximum demands' and sheet.cell(r + 2,
                                                                             x).value == 'Register':  # getting maximum demands

                    unit_1 = sheet.cell(r + 3, x + 2)
                    unit_2 = sheet.cell(r + 4, x + 2)
                    unit_3 = sheet.cell(r + 5, x + 2)
                    if unit_1.value == 'VA' and unit_2.value == 'VA' and unit_3.value == 'VA':
                        max_dem_1_r = sheet.cell(r + 3, x + 1).value.replace(',', '')  # max demand 1
                        max_dem_1_rh = round(float(max_dem_1_r) / 1000000, 4)
                        max_dem_1 = "{:,}".format(max_dem_1_rh)

                        max_dem_2_r = sheet.cell(r + 4, x + 1).value.replace(',', '')  # max demand 2
                        max_dem_2_rh = round(float(max_dem_2_r) / 1000000, 4)
                        max_dem_2 = "{:,}".format(max_dem_2_rh)

                        max_dem_3_r = sheet.cell(r + 5, x + 1).value.replace(',', '')  # max demand 3
                        max_dem_3_rh = round(float(max_dem_3_r) / 1000000, 4)
                        max_dem_3 = "{:,}".format(max_dem_3_rh)

                if cell.value == 'Maximum demands' and sheet.cell(r + 2, x).value == 'Register' and sheet.cell(r + 2,
                                                                                                               x + 3).value == 'Time and date':  # getting max-demands time
                    unit_1t = sheet.cell(r + 3, x + 3)
                    unit_2t = sheet.cell(r + 4, x + 3)
                    unit_3t = sheet.cell(r + 5, x + 3)

                    max_dem_1t = unit_1t.value
                    max_dem_2t = unit_2t.value
                    max_dem_3t = unit_3t.value




        # Processing Check meter data
        #fd = pd.read_csv(f'media/{file_m}')
        #fd.to_excel(f"FILES/{xlm}.xlsx", sheet_name='sheet1',
                    #index=False)
        # df = pd.DataFrame(fd)
        # print(df)
        #workbook = py.load_workbook(f"FILES/{xlm}.xlsx")
        ch = pd.read_csv(f'media/{file_ch}')
        fd.to_excel(f"FILES/{xlm}_ch.xlsx", sheet_name='sheet1',
                    index=False)
        workbook_ck = py.load_workbook(f"FILES/{xlm}_ch.xlsx")
        sheet_ch = workbook_ck['sheet1']
        man_ch_value = sheet_ch['B1'].value
        manu_ch = man_value.split()[0]  # meter manufacturer
        # print(manu)
        input_string_ch = sheet_ch["B2"].value
        meter_ch = input_string_ch.split()[0].replace('-', '')  # meter number
        # print(meter)
        date_pattern_ch = '%{MONTHNUM:month}/%{MONTHDAY:day}/%{YEAR:year}'
        grok = Grok(date_pattern_ch)
        xl = (grok.match(input_string_ch))
        mm = xl['month']
        dd = xl['day']
        yr = xl['year']
        x = datetime(int(yr), int(mm), int(dd))
        # ll = (x.strftime("%d-%m-%Y"))
        D_O_R_ch = (x.strftime("%d-%b-%Y"))  # reading date
        for p in range(1, sheet_ch.max_row):
            for q in range(1, sheet_ch.max_column):
                cell = sheet_ch.cell(p, q)
                if cell.value == 'Cumulative totals':
                    cell_imp_whr = sheet_ch.cell(p + 3, q + 1)
                    cell_unit = sheet_ch.cell(p + 3, q + 2)
                    cell_expwh_unit = sheet_ch.cell(p + 4, q + 2)
                    if cell_unit.value == 'Import Wh' and cell_expwh_unit.value == 'Export Wh':  # cum import
                        imp_whr_ch = cell_imp_whr.value.replace(',', '')
                        imp_whh_ch = round(float(imp_whr_ch) / 1000000, 3)
                        imp_wh_ch = "{:,}".format(imp_whh_ch)

                    cell_exp_whr_ch = sheet_ch.cell(p + 4, q + 1)  # cum export
                    if cell_unit.value == 'Import Wh' and cell_expwh_unit.value == 'Export Wh':
                        exp_whr_ch = cell_exp_whr_ch.value.replace(',', '')
                        exp_whh_ch = round(float(exp_whr_ch) / 1000000, 3)
                        exp_wh_ch = "{:,}".format(exp_whh_ch)

                    cell_app_pow_ch = sheet_ch.cell(p + 9, q + 1)  # getting apparent power
                    cell_app_pow_unit_ch = sheet_ch.cell(p + 9, q + 2)
                    if cell_app_pow_unit_ch.value == 'VAh':
                        app_powr_ch = cell_app_pow_ch.value.replace(',', '')
                        app_powh_ch = round(float(app_powr_ch) / 1000000, 3)
                        app_pow_ch = "{:,}".format(app_powh_ch)

                    # getting total import and export MVarh
                    unit1_MVArh_ch = sheet_ch.cell(p + 5, q + 2)
                    unit3_MVArh_ch = sheet_ch.cell(p + 7, q + 2)
                    if unit1_MVArh_ch.value == 'Q1 varh' and unit3_MVArh_ch.value == 'Q3 varh':  # getting import MVArh. We add Q1 & Q2
                        imp_MVArh1_r_ch = sheet_ch.cell(p + 5, q + 1).value.replace(',', '')
                        imp_MVArh1_ch = float(imp_MVArh1_r_ch)
                        imp_MVArh2_r_ch = sheet_ch.cell(p + 7, q + 1).value.replace(',', '')
                        imp_MVArh2_ch = float(imp_MVArh2_r_ch)
                        total_imp_MVArh_r_ch = round((imp_MVArh1_ch + imp_MVArh2_ch) / 1000000, 3)

                        total_imp_MVArh_ch = "{:,}".format(total_imp_MVArh_r_ch)

                    unit2_MVArh_ch = sheet_ch.cell(p + 6, q + 2)
                    unit4_MVArh_ch = sheet_ch.cell(p + 8, q + 2)
                    if unit2_MVArh_ch.value == 'Q2 varh' and unit4_MVArh_ch.value == 'Q4 varh':  # getting import MVArh. We add Q3 & Q4
                        exp_MVArh1_r_ch = sheet_ch.cell(p + 6, q + 1).value.replace(',', '')
                        exp_MVArh1_ch = float(exp_MVArh1_r_ch)
                        exp_MVArh2_r_ch = sheet_ch.cell(p + 8, q + 1).value.replace(',', '')
                        exp_MVArh2_ch = float(exp_MVArh2_r_ch)
                        total_exp_MVArh_r_ch = round((exp_MVArh1_ch + exp_MVArh2_ch) / 1000000, 3)
                        total_exp_MVArh_ch = "{:,}".format(total_exp_MVArh_r_ch)

                    # total MVArh
                    total_MVArh_x_ch = float(total_exp_MVArh_ch.replace(',', '')) - float(
                        total_imp_MVArh_ch.replace(',', ''))
                    total_MVArh_xx_ch = round(total_MVArh_x_ch, 3)
                    total_MVArh_ch = "{:,}".format(total_MVArh_xx_ch)

                if cell.value == 'Register':  # getting the various rates
                    unit1 = sheet_ch.cell(p + 1, q + 2)
                    unit2 = sheet_ch.cell(p + 2, q + 2)
                    unit3 = sheet_ch.cell(p + 3, q + 2)
                    if unit3.value == unit2.value == 'Import Wh':
                        rate1_r_ch = sheet_ch.cell(p + 1, q + 1).value.replace(',', '')
                        rate1_rh_ch = round(float(rate1_r_ch) / 1000000, 3)
                        rate1_ch = "{:,}".format(rate1_rh_ch)
                    if unit1.value == unit3.value == 'Import Wh':
                        rate2_r_ch = sheet.cell(p + 2, q + 1).value.replace(',', '')
                        rate2_rh_ch = round(float(rate2_r_ch) / 1000000, 3)
                        rate2_ch = "{:,}".format(rate2_rh_ch)
                    if unit2.value == unit1.value == 'Import Wh':
                        rate3_r_ch = sheet.cell(p + 3, q + 1).value.replace(',', '')
                        rate3_rh_ch = round(float(rate3_r_ch) / 1000000, 3)
                        rate3_ch = "{:,}".format(rate3_rh_ch)

                    unit4 = sheet.cell(p + 4, q + 2)
                    unit5 = sheet.cell(p + 5, q + 2)
                    unit6 = sheet.cell(p + 6, q + 2)
                    if unit5.value == unit6.value == 'Export Wh':
                        rate4_r_ch = sheet.cell(p + 4, q + 1).value.replace(',', '')
                        rate4_rh_ch = round(float(rate4_r_ch) / 1000000, 3)
                        rate4_ch = "{:,}".format(rate4_rh_ch)

                    if unit4.value == unit6.value == 'Export Wh':
                        rate5_r_ch = sheet.cell(p + 5, q + 1).value.replace(',', '')
                        rate5_rh_ch = round(float(rate5_r_ch) / 1000000, 3)
                        rate5_ch = "{:,}".format(rate5_rh_ch)

                    if unit4.value == unit5.value == 'Export Wh':
                        rate6_r_ch = sheet.cell(p + 6, q + 1).value.replace(',', '')
                        rate6_rh_ch = round(float(rate6_r_ch) / 1000000, 3)
                        rate6_ch = "{:,}".format(rate6_rh_ch)

                if cell.value == 'Cumulative maximum demands' and sheet.cell(p + 2,q).value == 'Register':  # getting maximum demands


                    unit_1 = sheet.cell(p + 3, q + 2)
                    unit_2 = sheet.cell(p + 4, q + 2)
                    unit_3 = sheet.cell(p + 5, q + 2)
                    if unit_1.value == 'VA' and unit_2.value == 'VA' and unit_3.value == 'VA':
                        max_dem_1_r_ch = sheet.cell(p + 3, q + 1).value.replace(',', '')  # max demand 1
                        max_dem_1_rh_ch = round(float(max_dem_1_r_ch) / 1000000, 4)
                        max_dem_1_ch = "{:,}".format(max_dem_1_rh_ch)

                        max_dem_2_r_ch = sheet.cell(p + 4, q + 1).value.replace(',', '')  # max demand 2
                        max_dem_2_rh_ch = round(float(max_dem_2_r_ch) / 1000000, 4)
                        max_dem_2_ch = "{:,}".format(max_dem_2_rh_ch)

                        max_dem_3_r_ch = sheet.cell(p + 5, q + 1).value.replace(',', '')  # max demand 3
                        max_dem_3_rh_ch = round(float(max_dem_3_r_ch) / 1000000, 4)
                        max_dem_3_ch = "{:,}".format(max_dem_3_rh_ch)

                if cell.value == 'Maximum demands' and sheet.cell(p + 2, q).value == 'Register' and \
                        sheet.cell(p + 2,q + 3).value == 'Time and date':  # getting max-demands time
                    unit_1t_ch = sheet.cell(p + 3, q + 3)
                    unit_2t_ch = sheet.cell(p + 4, q + 3)
                    unit_3t_ch = sheet.cell(p + 5, q + 3)

                    max_dem_1t_ch = unit_1t_ch.value
                    max_dem_2t_ch = unit_2t_ch.value
                    max_dem_3t_ch = unit_3t_ch.value

                if cell.value == 'Billing event details':
                    req_cell = sheet.cell(p + 2, q)
                    req_cell1 = sheet.cell(p + 3, q)
                    if req_cell.value == 'Billing reset number:':
                        resets_ch = sheet.cell(p + 2, q + 1).value
                        # no_of_resets = float(no_of_resets_r)

                    if req_cell1.value == 'Time of billing reset:':
                        reset_time_ch = sheet.cell(p + 3, q + 1).value






        return render(request, 'uetcl_meter.html',
                      {'manu': manu, 'meter': meter, 'xl': xl, 'D_O_R': D_O_R, 'imp_wh': imp_wh, 'exp_wh': exp_wh,
                       'app_pow': app_pow, 'rate1': rate1,
                       'rate2': rate2, 'rate3': rate3, 'rate4': rate4, 'rate5': rate5, 'rate6': rate6, 'resets': resets,
                       'reset_time': reset_time,
                       'M_O_S': M_O_S, 'total_imp_MVArh': total_imp_MVArh, 'total_exp_MVArh': total_exp_MVArh,
                       'total_MVArh': total_MVArh,
                       'max_dem_1': max_dem_1, 'max_dem_2': max_dem_2, 'max_dem_3': max_dem_3, 'max_dem_1t': max_dem_1t,
                       'max_dem_2t': max_dem_2t,
                       'max_dem_3t': max_dem_3t, 'manu_ch': manu_ch, 'D_O_R_ch': D_O_R_ch, 'meter_ch': meter_ch,
                       'imp_wh_ch': imp_wh_ch, 'exp_wh_ch': exp_wh_ch,
                       'app_pow_ch': app_pow_ch, 'total_imp_MVArh_ch': total_imp_MVArh_ch, 'total_MVArh_ch': total_MVArh_ch,
                       'total_exp_MVArh_ch': total_exp_MVArh_ch,
                       'rate1_ch': rate1_ch, 'data': data, 'read_time': read_time,'rate2_ch':rate2_ch,'rate3_ch':rate3_ch,'rate4_ch':rate4_ch,
                        'rate5_ch':rate5_ch,'rate6_ch':rate6_ch,'max_dem_1_ch':max_dem_1_ch,'max_dem_2_ch':max_dem_2_ch,'max_dem_3_ch':max_dem_3_ch,
                       'max_dem_1t_ch': max_dem_1t_ch, 'max_dem_2t_ch': max_dem_2t_ch, 'max_dem_3t_ch': max_dem_3t_ch,'resets_ch':resets_ch,
                       'reset_time_ch':reset_time_ch,
                       })


def submission(request):
    if request.method == 'POST':
        global active_user
        unix = datetime.now().replace (microsecond=0)
        #date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
        #substation = request.POST['subst']
        M_O_S = request.POST['month_of_sale']
        R_D = request.POST['reading_date']
        R_T = request.POST['reading_time']
        meter_no = request.POST['main_meter_no']
        cum_imp = request.POST['cum_imp_m'].replace(',','')
        cum_exp = request.POST['cum_exp_m'].replace(',','')
        app_pow = request.POST['app_pow_m'].replace(',','')
        rate1 = request.POST['rate1_m'].replace(',','')
        rate2 = request.POST['rate2_m'].replace(',','')
        rate3 = request.POST['rate3_m'].replace(',','')
        rate4 = request.POST['rate4_m'].replace(',','')
        rate5 = request.POST['rate5_m'].replace(',','')
        rate6 = request.POST['rate6_m'].replace(',','')
        max_dem1 = request.POST['max_dem_m']
        max_dem1_time = request.POST['max_dem_t_m']
        max_dem2 = request.POST['max_dem2_m']
        max_dem2_time = request.POST['max_dem2_t_m']
        max_dem3 = request.POST['max_dem3_m']
        max_dem3_time = request.POST['max_dem3_t_m']
        imp_mvarh = request.POST['imp_mvarh_m'].replace(',','')
        exp_mvarh = request.POST['exp_mvarh_m'].replace(',','')
        total_mvarh = request.POST['total_mvarh_m'].replace(',','')
        resets = request.POST['resets_m']
        last_reset = request.POST['last_reset_m']
        pow_down_count = request.POST['pow_down_count_m']
        pow_down_dt = request.POST['pow_down_dt_m']
        prog_count = request.POST['prog_count_m']
        prog_count_dt = request.POST['prog_count_dt_m']
        vt_ratio = request.POST['vt_ratio_m']
        ct_ratio = request.POST['ct_ratio_m']

        #date for check meter
        meter_no_ch = request.POST['check_meter_no']
        cum_imp_ch = request.POST['cum_imp_c'].replace(',', '')
        cum_exp_ch = request.POST['cum_exp_c'].replace(',', '')
        app_pow_ch = request.POST['app_pow_c'].replace(',', '')
        rate1_ch = request.POST['rate1_c'].replace(',', '')
        rate2_ch = request.POST['rate2_c'].replace(',', '')
        rate3_ch = request.POST['rate3_c'].replace(',', '')
        rate4_ch = request.POST['rate4_c'].replace(',', '')
        rate5_ch = request.POST['rate5_c'].replace(',', '')
        rate6_ch = request.POST['rate6_c'].replace(',', '')
        max_dem1_ch = request.POST['max_dem_c']
        max_dem1_time_ch = request.POST['max_dem_t_c']
        max_dem2_ch = request.POST['max_dem2_c']
        max_dem2_time_ch = request.POST['max_dem2_t_c']
        max_dem3_ch = request.POST['max_dem3_c']
        max_dem3_time_ch = request.POST['max_dem3_t_c']
        imp_mvarh_ch = request.POST['imp_mvarh_c'].replace(',', '')
        exp_mvarh_ch = request.POST['exp_mvarh_c'].replace(',', '')
        total_mvarh_ch = request.POST['total_mvarh_c'].replace(',', '')
        resets_ch = request.POST['resets_c']
        last_reset_ch = request.POST['last_reset_c']
        pow_down_count_ch = request.POST['pow_down_count_c']
        pow_down_dt_ch = request.POST['pow_down_dt_c']
        prog_count_ch = request.POST['prog_count_c']
        prog_count_dt_ch = request.POST['prog_count_dt_c']
        vt_ratio_ch = request.POST['vt_ratio_c']
        ct_ratio_ch = request.POST['ct_ratio_c']
        #current_user = request.user

        #active_user = user_act
        #active_user = read_by
        #inserted_by = active_user
        read_time= request.POST['reading_time']
        read_date = request.POST['reading_date']
        #id = 0

        conn = pymysql.connect(host='localhost', port=3306, user='root', password='', database='meteringdatabase')
        c = conn.cursor()
        sql = """INSERT INTO lgg_main(time_stamp,inserted_by,meter_read_by,reading_date,reading_time,meter_no, Energy_For, Cum_Import, Cum_Export, Apparent_Power,Rate_1,
        Rate_2, Rate_3, Rate_4, Rate_5, Rate_6, Max_Dem_1, Max_Dem1_time, Max_Dem_2,Max_Dem2_time, Max_Dem3, Max_Dem3_time, Import_MVArh,
        Export_MVArh,Total_MVAh,No_of_Resets,Last_Reset,Power_Down_Count,Lst_pwr_dwn_date_and_time,prog_count,last_prog_date,VT_Ratio,CT_Ratio,
        meter_no_ch,Cum_Import_ch, Cum_Export_ch, Apparent_Power_ch,Rate_1_ch,
        Rate_2_ch, Rate_3_ch, Rate_4_ch, Rate_5_ch, Rate_6_ch, Max_Dem_1_ch, Max_Dem1_time_ch, Max_Dem_2_ch,Max_Dem2_time_ch, Max_Dem3_ch,
         Max_Dem3_time_ch, Import_MVArh_ch,Export_MVArh_ch,Total_MVAh_ch,No_of_Resets_ch,Last_Reset_ch,
        Power_Down_Count_ch,Lst_pwr_dwn_date_and_time_ch,prog_count_ch,last_prog_date_ch,VT_Ratio_ch,CT_Ratio_ch)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,
         %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)"""
        #sql2 = 'read username FROM auth_user'

        val = (unix, active_user, active_user,read_date,read_time, meter_no, M_O_S, cum_imp, cum_exp, app_pow, rate1, rate2, rate3, rate4, rate5,
               rate6, max_dem1, max_dem1_time, max_dem2, max_dem2_time, max_dem3, max_dem3_time, imp_mvarh, exp_mvarh,
               total_mvarh, resets, last_reset, pow_down_count, pow_down_dt, prog_count, prog_count_dt, vt_ratio, ct_ratio,
               meter_no_ch,cum_imp_ch,cum_exp_ch,app_pow_ch,rate1_ch,rate2_ch,rate3_ch,rate4_ch,rate5_ch,rate6_ch,max_dem1_ch,max_dem1_time_ch,
               max_dem2_ch,max_dem2_time_ch,max_dem3_ch,max_dem3_time_ch,imp_mvarh_ch,exp_mvarh_ch,total_mvarh_ch,resets_ch,last_reset_ch,
               pow_down_count_ch,pow_down_dt_ch,prog_count_ch,prog_count_dt_ch,vt_ratio_ch,ct_ratio_ch)

        c.execute(sql,val)

        conn.commit()
        c.close()
        conn.close()
        return render(request, 'form_success.html')
#global df1,df2,df3,df_ia,df_ib,df_ic,df_va,df_vb,df_vc,df_pw,df_vars
def monthly_LP(request):
    engine = create_engine('mysql://root:@localhost/meteringdatabase')
    if request.method == 'POST':
        uploaded_file = request.FILES['LP']
        fs = FileSystemStorage()
        file_LP = fs.save(uploaded_file.name, uploaded_file)

        now = datetime.now()
        xlm = f"Meter Load Profile For {now.strftime('%B')}"
        fd = pd.read_csv(f'media/{file_LP}')
        fd.to_excel(f"loadprofiles/{xlm}.xlsx", index=False)
        #month = now.strftime('%B')
        start = time.time()
        #workbook = xlsxwriter.Workbook('Example1.xlsx')
        #worksheet = workbook.add_worksheet()
        wb = xl.load_workbook(f"loadprofiles/{xlm}.xlsx")
        sheets = wb.sheetnames
        ws = wb[sheets[0]]
        for i in range(1, ws.max_column):
            cell_value = ws.cell(row=1, column=i).value
            # if cell_value1 != '':
            if not cell_value == None:
                # cell_value = cell_value1.replace('-','')
                manu_1 = 'Elster'
                if cell_value.find(manu_1) == 1:
                    print(f'manufacturer is Elster')
                    break

        meter_no_x = ws["B2"].value
        meter_no = meter_no_x.split()[0].replace('-', '')
        print(meter_no)
        # engine = create_engine('mysql://root:@localhost/meteringdatabase')
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='',
                               database='meteringdatabase')
        c = conn.cursor()
        list_1 = []
        list_2 = []
        list_3 = []
        list_4 = []
        for x in range(1, 20):
            for r in range(1, ws.max_column + 1):
                cell = ws.cell(r, x)
                global df,df1,df2,df3,df4
                if cell.value == 'Date' and ws.cell(r, x + 1).value == 'Start' and ws.cell(r,
                                                                                           x + 2).value == 'End':  # check this loop for x and r (row and column)
                    for m in range(r + 1, ws.max_row+1):
                        use_date = ws.cell(m, x).value
                        date_time_obj = datetime.strptime(use_date, '%d/%m/%Y').date()
                        #print(date_time_obj)
                        month = date_time_obj.strftime("%B")
                        #month = use_date.strftime('%B')
                        start_time_1 = ws.cell(m, x + 1).value
                        start_time = '%.6s' % start_time_1
                        end_time_1 = ws.cell(m, x + 2).value
                        end_time = '%.6s' % end_time_1
                        list_1.append(use_date)
                        list_2.append(start_time)
                        list_3.append(end_time)
                        list_4.append(month)
                    # print(list_1)
                    df1 = pd.DataFrame(list_1)
                    df1.columns = ['date']
                    # print(df1)
                    df2 = pd.DataFrame(list_2)
                    df2.columns = ['start_time']
                    # print(df2)
                    df3 = pd.DataFrame(list_3)
                    df3.columns = ['end_time']
                    df4 = pd.DataFrame(list_4)
                    df4.columns = ['month']
                    # print(df3)
                    #df = pd.concat([df1, df2, df3], axis=1)

                    # print(df)

                list_ia = []
                # row_ia = 0
                global dfnew
                global df_ia
                if cell.value == 'A: PhA: Av':
                    for m in range(r, ws.max_row+1):
                        I_A = ws.cell(m, x - 1).value
                        list_ia.append(I_A)
                    df_ia = pd.DataFrame(list_ia)
                    df_ia.columns = ['I_A']
                    #dfnew = pd.concat([df, df_ia], axis=1)
                    # print(dfnew)

                    break

                list_ib = []
                global df_ib
                if cell.value == 'A: PhB: Av':
                    for m in range(r, ws.max_row+1):
                        I_B = ws.cell(m, x - 1).value
                        list_ib.append(I_B)
                    df_ib = pd.DataFrame(list_ib)
                    df_ib.columns = ['I_B']
                    #df_ib = pd.concat([dfnew, df_ib_x], axis=1)
                    # print(df_ib)
                    break

                list_ic = []
                global df_ic
                if cell.value == 'A: PhC: Av':
                    for m in range(r, ws.max_row+1):
                        I_C = ws.cell(m, x - 1).value
                        list_ic.append(I_C)
                    df_ic = pd.DataFrame(list_ic)
                    df_ic.columns = ['I_C']
                    #df_ic = pd.concat([df_ib, df_ic_x], axis=1)
                    #print(df_ic)
                    break

                list_va = []
                global df_va
                if cell.value == 'V: PhA: Av':
                    for m in range(r, ws.max_row+1):
                        V_A = ws.cell(m, x - 1).value
                        list_va.append(V_A)
                    df_va = pd.DataFrame(list_va)
                    df_va.columns = ['V_A']
                    break

                global df_vb
                list_vb = []
                if cell.value == 'V: PhB: Av':
                    for m in range(r, ws.max_row+1):
                        V_B = ws.cell(m, x - 1).value
                        list_vb.append(V_B)
                    df_vb = pd.DataFrame(list_vb)
                    df_vb.columns = ['V_B']
                    break
                global df_vc
                list_vc = []
                if cell.value == 'V: PhC: Av':
                    for m in range(r, ws.max_row+1):
                        V_C = ws.cell(m, x - 1).value
                        list_vc.append(V_C)
                    df_vc = pd.DataFrame(list_vc)
                    df_vc.columns = ['V_C']
                    break

                global df_pw
                list_pw = []
                if cell.value == 'kW: Sys: Av':
                    for m in range(r, ws.max_row+1):
                        PW = ws.cell(m, x - 1).value
                        # print(PW)
                        list_pw.append(PW)
                    df_pw = pd.DataFrame(list_pw)
                    df_pw.columns = ['PW']
                    break

                global df_Pvar
                list_Pvar = []
                if cell.value == 'kvar: Sys: Av':
                    for m in range(r, ws.max_row+1):
                        Pvar = ws.cell(m, x - 1).value
                        # print(PW)
                        list_Pvar.append(Pvar)
                    df_Pvar = pd.DataFrame(list_Pvar)
                    df_Pvar.columns = ['P_var']

                    df = pd.concat([df1,df4,df2,df3,df_ia,df_ib,df_ic,df_va,df_vb,df_vc,df_pw,df_Pvar],axis=1)
                    #print(df)
                    df.to_sql('uetcl0103', con=engine, if_exists='append', index=False,
                                 dtype={'date': VARCHAR(length=30),'month': VARCHAR(length=12),
                                        'start_time': String(length=10), 'end_time': String(length=10),
                                        'I_A': String(length=10), 'I_B': String(length=10),
                                        'I_C': String(length=10)})
                    break

        end = time.time()
        print("Elapsed time is  {}".format(end - start))

        return render(request,'form_success.html')

def LP_plot(request): #Plotting Load profiles
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='', database='meteringdatabase')
    c = conn.cursor()
    sql = "SELECT start_time, PW FROM uetcl0102 WHERE month = 'September' AND date = '22/09/2020'"
    time = []
    power = []
    c.execute(sql)
    data = c.fetchall()
    for row in data:
        time.append(row[0])
        power.append(float(row[1])/1000)

    # print(power)
    plt.rcParams.update({'font.size': 22})
    fig = plt.figure(figsize=(15, 6))
    plt.ylabel("Power/kW")
    plt.xlabel('Time/Hrs')
    plt.plot(time, power, color='red', )
    plt.title("Load Profile For January")
    #plt.show()
    mpld3.save_html(fig, 'E:\\METERING DATABASE\\metering_database\\templates\\kim.html')

    conn.commit()
    c.close()
    conn.close()

    return render(request, 'kim.html') #end of function



def umeme(request):
    #global meters_umeme
    meters_umeme = []
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='', database='meteringdatabase')
    c = conn.cursor()
    sql = "SELECT meter_no FROM substation_meters WHERE distributor = 'umeme'"
    c.execute(sql)
    data = c.fetchall()
    for row in data:
        meters_umeme.append(row[0])
    # print(meters)
    conn.commit()
    c.close()
    conn.close()
    year = date.today().year
    xxl = date.today().month - 1
    # print(now)
    month = calendar.month_name[xxl]
    bill_date = f'{month} {year}'

    #{"distributor": distributor,}
    #months = []
    #for name in calendar.month_name:
        # print(name)
        #months.append(name)
    #years = []
    #for i in range(-2, 5):
        #year = date.today().year + i
        #years.append(year)
    #print(years)

    #meter = ['UETCL001', 'UETCL002', 'UETCL003','UETCL004']
    #distributors = ['Umeme','UEDCL','PACKMECS','BEL','KRECS']
    #print(list1)
    return render(request, 'gen_bill.html',{'meters_umeme':meters_umeme,'bill_date':bill_date})

def bill_gen(request):
    if request.method == 'POST':
        meter_no = request.POST['meter_no']
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='', database='meteringdatabase')
        c = conn.cursor()
        sql = "SELECT reading_date, reading_time, meter_no_ch,"
        conn.commit()
        c.close()
        conn.close()

    return render(request,'bill.html')

def newmeter(request):
    return render(request,'new_meter_home.html')

def standalone(request):
    return render(request,'standalone_meter.html')

def substation(request):
    return render(request,'substation_meter.html')



def querries(request):
    return render(request, 'querries.html')

def querriesback(request):
    return render(request, 'welcome.html')

def new_LP(request):
    return render(request,'insertLP.html')
