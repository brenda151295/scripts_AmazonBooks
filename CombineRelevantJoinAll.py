# Importing MySQL Connector.
import mysql.connector

import pymysql

# Connecting to MySQL.
mysql_conn = mysql.connector.connect(user='root', password='', port="3306", host='localhost', database='books_dataset')

treshold = 50

def getObjectsRemoveFromNetwork(times):
    sql = "SELECT object from all_algorithms group by object having count(*)>"+str(times)+";"
    cursor = mysql_conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    sql_all = "SELECT object from all_algorithms group by object;"
    cursor = mysql_conn.cursor()
    cursor.execute(sql_all)
    result_all = cursor.fetchall()
    output = []
    for r in result_all:
        output.append(r[0])
    for r in result:
        output.remove(r[0])
    return output

def getObjects(asin, remove):
    sql = 'SELECT * FROM all_algorithms ' + remove + ' AND probability > ' + str(treshold) + ' AND book = "' + str(asin) + '" ORDER BY cast(probability as unsigned) DESC LIMIT 3;'
    cursor = mysql_conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def remove(object_remove):
    remove = " WHERE object != '" + object_remove[0] + "' "
    for i in range(1, len(object_remove)):
        remove = remove + 'AND object != "'+ object_remove[i] +'" '
    return remove

def delete_repeated(objects_book):
    temp = objects_book[0]
    i = 0
    while i < len(objects_book)-1:
        if temp[2] != objects_book[i+1][2]:
            temp = objects_book[i]
            i = i + 1
        else:
            del objects_book[i+1]
    return objects_book

def insert():
    sql = "SELECT * from books_objects;"
    cursor = mysql_conn.cursor()
    cursor.execute(sql)
    books = cursor.fetchall()
    objects_remove = getObjectsRemoveFromNetwork(100)
    remove_str = remove(objects_remove)

    for book in books:
        asin = book[1]
        objects_book = getObjects(asin, remove_str)
        if len(objects_book):
            objects_book = delete_repeated(objects_book)
            sql_1 = "INSERT INTO books_objects_abstract (asin, title, subcat1, subcat2 "
            sql_2 = ""
            sql_3 = ' VALUES ("' + book[1] + '","' + book[2].replace('"','´´') + '","' + book[3] + '","' + book[4] + '" '
            count = 1
            for object in objects_book:
                sql_2 = sql_2 + ", obj"+ str(count)+ ", pb" + str(count)  
                sql_3 = sql_3 + ',"' + object[2] +'","' + str(object[3]) + '"'
                count = count + 1

            sql_2 = sql_2 + ")" 
            sql_3 = sql_3 + ")"
            sql = sql_1 + sql_2 + sql_3

            cursor = mysql_conn.cursor()
            cursor.execute(sql)
            mysql_conn.commit()


#listBooks()
#A = getObjectsFromNetwork('densenet', 100)
#print (len(A))
insert()