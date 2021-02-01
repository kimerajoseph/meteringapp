import datetime
import calendar

now = datetime.datetime.now().year
month = datetime.datetime.now().month-1
#print(now)
xxl = calendar.month_name[month]
print(f'{xxl} {now}')