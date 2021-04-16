import mysql.connector
from mysql.connector.errors import DatabaseError, ProgrammingError


def get_cursor():

	while True:
		host = input('Enter IP address of host: ')
		user = input('Enter username: ')
		password = input('Enter password: ')

		try:
			print("\033c", end="") # Clearing console
			mydb = mysql.connector.connect(
				host=host,
				user=user,
				password=password,
				database='MLB',
				connection_timeout=10
			)
		except ProgrammingError:
			print('Invalid credentials! Please try again')
			continue
		except DatabaseError:
			print('Connection timed out. IP address may be incorrect. Please try again')
			continue
		break

	return mydb, mydb.cursor()
