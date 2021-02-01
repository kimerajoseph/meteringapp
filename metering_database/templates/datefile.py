import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pymysql
import pandas as pd
import mpld3
conn = pymysql.connect(host='localhost', port=3306, user='root', password='', database='meteringdatabase')
c = conn.cursor()
sql = "SELECT start_time, PW FROM uetcl0102 WHERE month = 'September' AND date = '22/09/2020'"
time = []
power = []
c.execute(sql)
data = c.fetchall()
for row in data:
    time.append(row[0])
    power.append(float(row[1]))

#print(power)
plt.rcParams.update({'font.size': 22})
fig = plt.figure(figsize=(15, 6))
plt.plot(time,power,color = 'red', linestyle = 'dashed')
plt.title("load profile for January")
#plt.show()
mpld3.save_html(fig,'kim.html')


conn.commit()
c.close()
conn.close()


