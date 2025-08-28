import mysql.connector as m 
import getpass

password = getpass.getpass("Enter MySQL password: ")

con=m.connect(user='root', host='localhost', password=password)
cur=con.cursor()

cur.execute('DROP DATABASE IF EXISTS Verbum')
print('The MySQL database has been cleared!')
con.commit()
cur.close()
con.close()