import mysql.connector
import numpy as np

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="books_dataset"
)
mycursor = mydb.cursor()

def print_objects_algorithm():
	mycursor.execute("select DISTINCT object from objects_densenet")
	objects_densenet = mycursor.fetchall()
	mycursor.execute("select DISTINCT object from objects_inceptionV3")
	objects_inceptionV3 = mycursor.fetchall()
	mycursor.execute("select DISTINCT object from objects_resnet2")
	objects_resnet2 = mycursor.fetchall()
	mycursor.execute("select DISTINCT object from objects_resnet50_coco")
	objects_resnet50_coco = mycursor.fetchall()

	print ('Densenet: ', len(objects_densenet))
	for x in objects_densenet:
	  print(x, end=' ')
	print ('\n')

	print ('InceptionV3: ',len(objects_inceptionV3))
	for x in objects_inceptionV3:
	  print(x, end=' ')
	print ('\n')

	print ('Resnet2: ',len(objects_resnet2))
	for x in objects_resnet2:
	  print(x, end=' ')
	print ('\n')

	print ('Resnet50: ',len(objects_resnet50_coco))
	for x in objects_resnet50_coco:
	  print(x, end=' ')
	print ('\n')

def generate_sorted_objects(network, probability):
	objects_array = []
	mycursor.execute("select DISTINCT object from objects_"+network+" where probability < "+str(probability)+";")
	objects = mycursor.fetchall()
	for x in objects:
		objects_array.append(x[0].lower())
	return sorted(objects_array)

def get_objects(network, probability):
	mycursor.execute("select DISTINCT book, object from objects_"+network+" where probability < "+ str(probability)+";")
	objects = mycursor.fetchall()
	print (len(objects))
	return objects

def get_books(network):
	mycursor.execute("select DISTINCT book from objects_"+network+";")
	books = mycursor.fetchall()
	books_array = []
	for book in books:
		books_array.append(book[0])
	return books_array

def book_object_array(network, book, probability):
	request = "select DISTINCT book, object from objects_"+network+" where book='"+book+"' and probability < "+ str(probability)+";"
	mycursor.execute(request)
	objects = mycursor.fetchall()
	objects_book = []
	for x in objects:
		objects_book.append(x[1].lower())
	objects_all = generate_sorted_objects(network, probability)
	len_objects = len(objects_all)
	array = ['?']*len_objects #np.zeros((len_objects,), dtype=int)
	for obj in objects_book:
		i = objects_all.index(obj)
		array[i] = '1'
	return array

def get_category(book):
	mycursor.execute("select subcat1 from books_objects where asin='"+book+"';")
	category = mycursor.fetchall()
	category = category[0][0].replace(" ","_").replace(",","")
	if len(category):
		return category
	return 0

def get_all_categories():
	mycursor.execute("select distinct subcat1 from books_objects ;")
	categories = mycursor.fetchall()
	categories_array = []
	for category in categories:
		if len(category[0]):
			categories_array.append(category[0].replace(" ","_").replace(",",""))
	return categories_array

def generate_arff(network, probability):
	file = open("books_"+network+".arff","w") 
	
	file.write("@relation books_"+network+"\n")
	file.write("@attribute assin string\n") 
	objects_all = generate_sorted_objects(network, probability)
	for obj in objects_all:
		a = "@attribute '"+str(obj).replace("'","")+"' {?,1}\n"
		file.write(a)
	books_all = get_books(network)
	a = "@attribute Category {"
	categories = get_all_categories()
	for category in categories:
		a = a + category.replace("'","") + ", "
	file.write(a+"}\n")
	file.write("@data\n") 
	for book in books_all:
		array_book = book_object_array(network, book, probability)
		string = ""
		for i in array_book:
			string = string + str(i) +","
		category = get_category(book)
		if category:
			file.write(book+","+string+category.replace("'","")+"\n")

generate_arff("inceptionV3",50)