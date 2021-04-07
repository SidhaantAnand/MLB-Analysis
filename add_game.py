# TODO: Insertion/Deletion and updates in the games table by the user
def add_new_game(mydb, mycursor):
    home_team = input('Enter Home Team (3 character identifier): ')
    away_team = input('Enter Away Team (3 character identifier): ')
    date      = input('Enter Date (dd/mm/yyyy): ')
    home_score = int(input('Enter Home Score: '))
    away_score = int(input('Enter Away Score: '))
    venue       = input('Venue: ')
    umpire_1B = input('1B Umpire: ')
    umpire_2B = input('2B Umpire: ')
    umpire_3B = input('3B Umpire: ')
    umpire_HP = input('HP Umpire: ')
    game_data = (
        {'game_id': -1, 
        'home_team': home_team, 
        'away_team': away_team, 
        'date': date,
        'home_score': home_score,
        'away_score': away_score,
        'elapsed_time': elapsed_time,
        'start_time': start_time,
        'venue': venue,
        'attendence': attendence,
        'delay': delay,
        'umpire_1B': umpire_1B,
        'umpire_2B': umpire_2B,
        'umpire_3B': umpire_3B,
        'umpire_HP': umpire_HP,
        'weather': weather
        })
    result, new_id = insert_new_game(mydb, mycursor, game_data)
    if result == 0:
        print('Sorry the data could not be entered either due to either incorrect format or duplicate values')
    else:
        game_data['game_id'] = new_id
        print('\n')
        print('Successfully inserted data! The following data was entered:')
        print('First Name: ', first_name)
        print('Last Name: ', last_name)
        action = 'random string'
        while action != 'c':
            action = input('See a mistake? Enter (u) to update, (d) to delete or (c) to continue: ')
            result = 0
            if action == 'u':
                print('\n')
                print('Which field would you like to update: ')
                print('1. First Name')
                print('2. Last Name')
                field = int(input('Enter your choice: '))
                if field == 1:
                    first_name = input('Updated First Name: ')
                    full_name = first_name + ' ' + last_name
                    result = update_new_game(mydb, mycursor, game_data, 0, full_name, first_name)
                elif field == 2:
                    last_name = input('Updated Last Name: ')
                    full_name = first_name + ' ' + last_name
                    result = update_new_game(mydb, mycursor, game_data, 1, full_name, last_name)
                else:
                    print('Sorry invalid field number was entered')
                if result == 2:
                    print('\n')
                    print('Successfully Updated data! The following data was entered:')
                    if field == 1:
                        game_data['first_name'] = first_name
                    if field == 2:
                        game_data['last_name'] = last_name
                        game_data['full_name'] = game_data['first_name'] + ' ' + game_data['last_name']
                    print('First Name: ', game_data['first_name'])
                    print('Last Name: ', game_data['last_name'])
                else:
                    print('Sorry the data could not be entered either due to either incorrect format or duplicate values')
        
            if action == 'd':
                result = delete_new_game(mydb, mycursor, game_data['game_id'])
                if result == 1:
                    print('Successfully deleted data!')
                    action = 'c'
                if result == 0:
                    print('Sorry the data could not be deleted due to invalid game name')
