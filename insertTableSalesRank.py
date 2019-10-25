# Importing MongoClient.
from pymongo import MongoClient

# Importing MySQL Connector.
import mysql.connector

import pymysql

# Connecting to MySQL.
mysql_conn = mysql.connector.connect(user='root', password='1234', port="3306", host='127.0.0.1', database='books_dataset')

# Geting the product details from 'asin'.
def getRankingAsin(asin):
    client = MongoClient()
    db = client.Amazon
    dbFilter = {"asin": asin, "title": {'$exists': True}, "salesRank.Books": {'$exists': True}}
    fields = {"asin": 1, "title": 1, "salesRank.Books": 1, "price": 1}
    try:
        for item in db.books_only.find(dbFilter, fields).limit(1):
            return item
    except:
        try:
            for item in db.metadata.find(dbFilter, fields).limit(1):
                return item
        except:
            return None
    finally:
        client.close()

def getBooksAsin():
    sql = "SELECT asin from nodes;"
    cursor = mysql_conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    output = []
    for i in result:
        output.append(i[0])
    return output

def insert():
    books = getBooksAsin()
    for asin in books:
        item = getRankingAsin(asin)
        if item != None:
            asin = item['asin']
            title = item['title']
            salesRank = item['salesRank']['Books']
            try:
                price = item['price']
            except:
                price = 0
            sql = "INSERT INTO books_salesRank (asin,title,salesRank, price) " \
                      "VALUES ('"+ asin +"','"+ pymysql.escape_string(title)+"'," +str(salesRank) + "," + str(price)+")"
            cursor = mysql_conn.cursor()
            cursor.execute(sql)
            mysql_conn.commit()

insert()