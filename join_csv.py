from os import listdir
import mysql.connector

def get_category_subcat(book):
    mycursor.execute("select subcat1, subcat2 from books_objects where asin='"+book+"';")
    categories = mycursor.fetchall()
    try:
        subcat1 = categories[0][0].replace(" ","_").replace(",","")
    except:
        subcat1 = " "
    try:
        subcat2 = categories[0][1].replace(" ","_").replace(",","")
    except:
        subcat2 = " "
    output = [subcat1, subcat2]
    return output

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="books_dataset"
)
mycursor = mydb.cursor()

path = '/home/ademir/Documents/SCRIPTS/csv'
files_csv = listdir(path)

fout=open("total.csv","a")
# first file:
fout.write('arquivo,black,red,green,blue,yellow,magenta,cyan,maroon,purple,orange,gray,white,subcat1,subcat2\n')
for line in open("csv/"+files_csv[0]):
    book = files_csv[0][:-8]
    line = line[:-1] + "," + get_category_subcat(book)[0] + "," + get_category_subcat(book)[1]+'\n'
    fout.write(line)
# now the rest:    
for num in range(1, len(files_csv)):
    f = open("csv/"+files_csv[num])
    for line in f:
        book = files_csv[num][:-8]
        line = line[:-1] + "," + get_category_subcat(book)[0] + "," + get_category_subcat(book)[1]+'\n'
        fout.write(line)
    f.close() # not really needed
fout.close()
