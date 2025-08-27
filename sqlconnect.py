import mysql.connector as m 
con=m.connect(user='root', host='localhost', password=' ')
cur=con.cursor()

cur.execute('Create database Verbum;' )
cur.execute('Create table users(username varchar(20) primary key, play int, win int, score int')
con.commit()
cur.close()
con.close()