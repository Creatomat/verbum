import mysql.connector as m 
import sys

try:
    con= m.connect(host="localhost", connection_timeout=2)
    con.close()
    sql_exists = True
except:
    sql_exists = False

if sql_exists:
    sys.exit(0)
else:
    sys.exit(1)
