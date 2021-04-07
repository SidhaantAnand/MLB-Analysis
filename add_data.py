from add_team import add_new_team
from add_venue import add_new_venue
from add_umpire import add_new_umpire
from add_player import add_new_player

def add_user_data(mydb, mycursor):
    print('What data would you like to enter?')
    print('1. New Game')
    print('2. New Player')
    print('3. New Team')
    print('4. New Venue')
    print('5. New Umpire')

    update_choice = input('Enter your choice: ')

    try:
        update_choice = int(update_choice)
    except ValueError:
        print('Error: You must enter an integer between 1 and 5')

    if update_choice < 1 or update_choice > 5:
        print('Invalid update_choice, please choose 1 or 5')
    
    if update_choice == 1:
        add_new_game(mydb, mycursor)

    if update_choice == 2:
        add_new_player(mydb, mycursor)

    if update_choice == 3:
        add_new_team(mydb, mycursor)

    if update_choice == 4:
        add_new_venue(mydb, mycursor)

    if update_choice == 5:
        add_new_umpire(mydb, mycursor)