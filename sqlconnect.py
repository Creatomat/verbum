import mysql.connector as m 
import getpass

password = getpass.getpass("Enter MySQL password: ")

con=m.connect(user='root', host='localhost', password=password)
cur=con.cursor()

cur.execute('DROP DATABASE IF EXISTS Verbum')
cur.execute('Create database Verbum')
cur.execute('Use Verbum')
cur.execute('Create table users(username varchar(20) primary key, play int, win int, score int)')
con.commit()
cur.close()
con.close()