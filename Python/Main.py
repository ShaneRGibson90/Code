import psycopg2
import csv

#Create a connection object
connect = psycopg2.connect(host="localhost", database="FunStuff", user="postgres", password="TestUser")

#Create a cursor object by using the cursor() function
cursor = connect.cursor()

#Initialize an empty list to store our formatted string later
string_list = []

#Open ProductData.csv and read it using the reader() function
with open ("ProductData.csv", "r+") as file:
    csvreader = csv.reader(file, delimiter = ',')
    next(file)
    for item in csvreader:
        string_list.append("('{0}', '{1}', {2})".format(item[0], item[1], item[2]))
file.close()

#Execute the CREASE TABLE and INSERT INTO commands to create and table and insert the values from our csv into our table
cursor.execute("CREATE TABLE test.ProductData (product_id varchar, product_name varchar, unit_price float(2));")
cursor.execute("INSERT INTO test.ProductData VALUES {}".format(','.join(string_list)))

#Open SalesData.csv and read it using the reader() function
with open ("SalesData.csv", "r+") as file:
    csvreader = csv.reader(file, delimiter = ',')
    next(file)
    string_list.clear()
    for item in csvreader:
        string_list.append("('{0}', '{1}', '{2}', {3}, '{4}')".format(item[0], item[1], item[2], item[3], item[4]))
file.close()

#Execute the CREASE TABLE and INSERT INTO commands to create and table and insert the values from our csv into our table
cursor.execute("CREATE TABLE test.SalesData (customer_name varchar, salesman_id varchar, product_id varchar, quantity_sold int, sale_date varchar);")
cursor.execute("INSERT INTO test.SalesData VALUES {}".format(','.join(string_list)))

#Open SalesManData.csv and read it using the reader() function
with open ("SalesmanData.csv", "r+") as file:
    csvreader = csv.reader(file, delimiter = ',')
    next(file)
    string_list.clear()
    for item in csvreader:
        string_list.append("('{0}', '{1}')".format(item[0], item[1].replace("'", " ")))        
file.close()

#Execute the CREASE TABLE and INSERT INTO commands to create and table and insert the values from our csv into our table
cursor.execute("CREATE TABLE test.SalesmanData (salesman_id varchar, salesman_name varchar);")
cursor.execute("INSERT INTO test.SalesmanData VALUES {}".format(','.join(string_list)))

#Commit the changes to the database
connect.commit()


                    ##FIRST SQL QUERY##

#SELECT salesmandata.salesman_name, SUM(quantity_sold) AS quantity_sold
#FROM test.salesdata
#INNER JOIN test.salesmandata ON salesdata.salesman_id = salesmandata.salesman_id
#WHERE sale_date LIKE '%11%'
#GROUP BY salesmandata.salesman_name
#ORDER BY SUM(quantity_sold) DESC;

#ANSWER: "Pavel McMonies"

                    ##SECOND SQL QUERY##

#SELECT productdata.product_name, SUM(quantity_sold)
#FROM test.productdata
#INNER JOIN test.salesdata ON productdata.product_id = salesdata.product_id
#GROUP BY productdata.product_name
#ORDER BY SUM(quantity_sold);

#ANSWER: "Onion Powder"

                    ##THIRD SQL QUERY##

#SELECT sale_date, COUNT(quantity_sold) AS "quantitysold" FROM test.salesdata
#GROUP BY sale_date
#ORDER BY COUNT(quantity_sold) DESC;

#ANSWER: "2020-12-15"