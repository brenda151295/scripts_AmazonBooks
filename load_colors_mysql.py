import mysql.connector
import numpy as np
import csv

mysql_conn = mysql.connector.connect(user='root', password='', port="3306", host='localhost', database='books_dataset')

def load_sql(filename):
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			asin = row[0][:-4]
			filename = row[0]
			sql = "INSERT INTO colors_12 (asin, filename, black, red, green, blue, yellow, " \
					"magenta, cyan, maroon, purple, orange, gray, white) VALUES ('" + \
					asin + "','"+ filename + "'," + row[1] + "," + row[2] + "," + row[3] + "," + row[4] + \
					"," + row[5] + "," + row[6] + "," + row[7] + "," + row[8] + "," + row[9] + "," + row[10] + \
					"," + row[11] + "," + row[12] + ")"
			cursor = mysql_conn.cursor()
			cursor.execute(sql)
			mysql_conn.commit()

load_sql('total.csv')