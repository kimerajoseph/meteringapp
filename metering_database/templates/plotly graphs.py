import plotly
import cufflinks
from plotly.offline import iplot
cufflinks.go_offline()
# Set global theme
#cufflinks.set_config_file(world_readable=True, theme='pearl')

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
df1 = pd.DataFrame(time)
df1.columns = ['time']
df2 = pd.DataFrame(power)
df2.columns = ['power']
df = pd.concat([df1,df2], axis=1)
df.head()
conn.commit()
c.close()
conn.close()

print(df)
kk = df.iplot(kind = 'bar', x = 'time', y = 'power')
kk.show()

