import pymysql

try:
    conn = pymysql.connect(host='localhost', port=3307, user='root', password='Technology30#', database='meteringdatabase')
    c = conn.cursor()
    print('connection successful')

except:
    print('not connected')
