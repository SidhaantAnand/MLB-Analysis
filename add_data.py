import mysql.connector
from add_team import add_new_team
from add_venue import add_new_venue
from add_umpire import add_new_umpire
from add_player import add_new_player

mydb = mysql.connector.connect(
  host="99.250.146.93",
  user="root",
  password="MLB_Gang",
  database="MLB"
)

mycursor = mydb.cursor()

def add_data():
    print('What data would you like to enter?')
    print('1. New Game')
    print('2. New Player')
    print('3. New Team')
    print('4. New Venue')
    print('5. New Umpire')

    option = input('Enter your choice: ')

    try:
        option = int(option)
    except ValueError:
        print('Error: You must enter an integer between 1 and 5')

    if option < 1 or option > 5:
        print('Invalid option, please choose 1 or 5')
    
    if option == 1:
        add_new_game(mydb, mycursor)

    if option == 2:
        add_new_player(mydb, mycursor)

    if option == 3:
        add_new_team(mydb, mycursor)

    if option == 4:
        add_new_venue(mydb, mycursor)

    if option == 5:
        add_new_umpire(mydb, mycursor)

add_data()