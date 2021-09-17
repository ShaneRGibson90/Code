import psycopg2, csv, os, sys

#Initialize variables
csv_file_list = []
string_list = []
joined_string = ""
table_name = ""

#Create a connection object
connect = psycopg2.connect(host="localhost", database="FunStuff", user="postgres", password="TestUser")

#Create a cursor object by using the cursor() function
cursor = connect.cursor()

#Get a list of all .csv files in the specfied directory
path = r"C:\Users\shane\Desktop\Python"
dirs = os.listdir(path)
for file in dirs:
   if file.endswith(".csv"):
       csv_file_list.append(file)

#Function that reads the .csv file and retrieves data from it and inserts it into it's respective table
def ReadCSVFiles(csv_file):
    with open (csv_file, "r+") as file:
        table_name = csv_file.replace(".csv", "")
        csvreader = csv.reader(file, delimiter = ',')
        next(file)
        for item in csvreader:
            string_list.clear()
            for i in item:
                i = i.replace("'", "")
                if any(c.isalpha() for c in i) or '-' in i:
                    i = "'" + i + "'"
                string_list.append(i)
                joined_string = ", ".join(string_list)
            cursor.execute("INSERT INTO test.{0} VALUES ({1})".format(table_name, joined_string))
        connect.commit()
        file.close()

#Try to create tables. If you can't then stop execution of the script
try:
    cursor.execute("CREATE TABLE test.ProductData (product_id varchar, product_name varchar, unit_price float(2));")
    cursor.execute("CREATE TABLE test.SalesData (customer_name varchar, salesman_id varchar, product_id varchar, quantity_sold int, sale_date varchar);")
    cursor.execute("CREATE TABLE test.SalesmanData (salesman_id varchar, salesman_name varchar);")

    #Call function on every .csv in the specified directory
    for item in csv_file_list:
        ReadCSVFiles(item)

    #The results from the SQL queries with answers
    cursor.execute("SELECT salesmandata.salesman_name, SUM(quantity_sold) AS quantity_sold FROM test.salesdata INNER JOIN test.salesmandata ON salesdata.salesman_id = salesmandata.salesman_id WHERE sale_date LIKE '_____11___' GROUP BY salesmandata.salesman_name ORDER BY SUM(quantity_sold) DESC LIMIT 1 ;")
    result = cursor.fetchall()
    print(result)

    cursor.execute("SELECT productdata.product_name, SUM(quantity_sold) FROM test.productdata INNER JOIN test.salesdata ON productdata.product_id = salesdata.product_id GROUP BY productdata.product_name ORDER BY SUM(quantity_sold) LIMIT 1;")
    result = cursor.fetchall()
    print(result)

    cursor.execute("SELECT sale_date, COUNT(quantity_sold) FROM test.salesdata GROUP BY sale_date ORDER BY COUNT(quantity_sold) DESC LIMIT 1;")
    result = cursor.fetchall()
    print(result)
  
except Exception as e:
    print("Unable to create tables: already exist")