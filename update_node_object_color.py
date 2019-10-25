# Importing MySQL Connector.
import mysql.connector

import pymysql

# Connecting to MySQL.
mysql_conn = mysql.connector.connect(user='root', password='', port="3306", host='localhost', database='books_dataset')

def update(asin):
    sql = "SELECT price,booksDay FROM books_salesRank WHERE asin = '"+str(asin)+"';"
    cursor = mysql_conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    sql = "UPDATE node_object_color set booksDay ='"+ result[0][1] +"', price = "+ result[0][0]+" WHERE id = '"+str(asin)+"';"
    cursor = mysql_conn.cursor()
    cursor.execute(sql)
    mysql_conn.commit()

sql = "SELECT asin FROM books_salesRank;"
cursor = mysql_conn.cursor()
cursor.execute(sql)
result = cursor.fetchall()
for i in result:
    update(i[0])