import mysql.connector
import numpy as np
import collections

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="books_dataset"
)
mycursor = mydb.cursor()

def clean_categories():
	mycursor.execute("SELECT nodes.subcat1, count(*) from nodes group by nodes.subcat1 having count(*)>100 and nodes.subcat1!='';")
	subcat1 = mycursor.fetchall()
	output = []
	for subcat in subcat1:
		mycursor.execute('SELECT nodes.asin from nodes where nodes.subcat1="'+subcat[0]+'";')
		output = output+mycursor.fetchall()
	return output

def clean_instances(instances):
	mycursor.execute("SELECT Edges.source from Edges;")
	source = mycursor.fetchall()
	mycursor.execute("SELECT Edges.target from Edges;")
	target = mycursor.fetchall()
	total = source + target
	total_clean = []
	for i in total:
		total_clean.append(i[0])
	count = collections.Counter(total_clean)
	most_common =  count.most_common(instances)
#	for i in most_common:
#		print (i)
	output = []
	for i in most_common:
		output.append(i[0])
	return output 

def clean_edges(nodes):
	output = []
	for node in nodes:
		mycursor.execute("SELECT Edges.id from Edges where Edges.source ='"+node+"' or Edges.target='"+node+"';")
		output = output+mycursor.fetchall()
	return output

def create_table_nodes(nodes):
	for node in nodes:
		mycursor.execute("INSERT INTO nodes_abstract SELECT * FROM nodes where asin='"+node+"';")
		mydb.commit()

def create_table_edges(edges):
	for edge in edges:
		mycursor.execute("INSERT INTO edges_abstract SELECT * FROM Edges where Edges.id="+str(edge[0])+";")
		mydb.commit()

nodes = clean_instances(100)
print (len(nodes))
edges = clean_edges(nodes)
print (len(edges))

#create_table_nodes(nodes)
create_table_edges(edges)