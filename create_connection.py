import mysql.connector

def get_cursor():
	mydb = mysql.connector.connect(
	  host="99.250.146.93",
	  user="root",
	  password="MLB_Gang",
	  database="MLB"
	)
	return mydb, mydb.cursor()