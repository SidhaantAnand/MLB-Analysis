import mysql.connector


def get_cursor():

	mydb = mysql.connector.connect(
		host='99.250.146.93',
		user='root',
		password='MLB356',
		database='MLB',
		connection_timeout=10
	)

	return mydb, mydb.cursor()
