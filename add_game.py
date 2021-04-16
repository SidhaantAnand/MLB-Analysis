from datetime import datetime

weather_dict = {
    1: 'Clear',
    2: 'Sunny',
    3: 'Overcast',
    4: 'Cloudy',
    5: 'Partly Cloudy',
    6: 'Snow',
    7: 'Drizzle',
    8: 'Dome',
    9: 'Roof Closed',
    10: 'Rain'
}


def add_new_game(mydb, mycursor):
    home_team = get_team_id(mycursor, input('Enter Home Team: '))
    away_team = get_team_id(mycursor, input('Enter Away Team: '))

    while True:
        year = input('Enter the year this game was played in: ')
        month = input('Enter the month this game was played in (as number): ')
        day = input('Enter the day of the month this game was played in: ')

        try:
            date = datetime.strptime(day + ' ' + month + ' ' + year, '%d %m %Y')
        except ValueError:
            print('You did not enter a valid date')
            continue
        break

    while True:
        try:
            home_score = int(input('Enter Home Score: '))
        except ValueError:
            print('Please enter an integer')
            continue
        break

    while True:
        try:
            away_score = int(input('Enter Away Score: '))
        except ValueError:
            print('Please enter an integer')
            continue
        break

    venue = input('Venue: ')
    umpire_1B = input('Enter 1B Umpire: ')
    umpire_2B = input('Enter 2B Umpire: ')
    umpire_3B = input('Enter 3B Umpire: ')
    umpire_HP = input('Enter HP Umpire: ')
    start_time = input('Enter game start time (HH:MM AM/PM): ')

    while True:
        try:
            elapsed_time = int(input('Enter game duration in minutes: '))
        except ValueError:
            print('Please enter an integer')
            continue
        break

    while True:
        try:
            attendance = int(input('Enter attendance: '))
        except ValueError:
            print('Please enter an integer')
            continue
        break

    temperature = input('Enter temperature on game day (Fahrenheit): ')

    print('Choose weather condition')
    for key, val in weather_dict.items():
        print(str(key) + '. ' + val)

    while True:
        weather_conditions = input('Enter choice: ')
        try:
            weather_conditions = int(weather_conditions)
        except ValueError:
            print('Please enter a number between 1 and 10')
            continue

        if weather_conditions < 1 or weather_conditions > 10:
            print('Please enter a number between 1 and 10')
            continue

        break

    wind = input('Enter wind speed (in mph): ')

    while True:
        try:
            delay = int(input('Enter game delay (in minutes): '))
        except ValueError:
            print('Please enter an integer')
            continue
        break

    game_data = {
        'g_id': new_game_id(mycursor, date),
        'home_team': home_team[0][0] if home_team else None,
        'away_team': away_team[0][0] if away_team else None,
        'date': date,
        'home_final_score': home_score,
        'away_final_score': away_score,
        'elapsed_time': elapsed_time,
        'start_time': start_time,
        'venue_name': venue,
        'attendance': attendance,
        'delay': delay,
        'umpire_1B': umpire_1B,
        'umpire_2B': umpire_2B,
        'umpire_3B': umpire_3B,
        'umpire_HP': umpire_HP,
        'weather': temperature + ' degrees, ' + weather_dict[weather_conditions].lower(),
        'wind': wind + ' mph,'
    }

    result = insert_new_game(mydb, mycursor, game_data)
    if result == 0:
        print('Sorry the data could not be entered either due to either incorrect format or duplicate values')
        print('\n')
    else:
        print('\n')
        print('Successfully inserted data!')

        action = 'random string'
        while action != 'c':
            print('The following data was entered:')
            for key, val in game_data.items():
                if key == 'g_id':
                    continue
                print(key.replace('_', ' ').capitalize() + ': ' + str(val))

            action = input('See a mistake? Enter (u) to update, (d) to delete or (c) to continue: ')

            result = 0
            if action == 'u':

                updates = {}
                updated = update_data(mycursor, game_data, updates)
                if not updated:
                    continue

                result = update_new_game(mydb, mycursor, updates, game_data['g_id'])

                if result == 1:
                    print('\n')
                    print('Successfully updated data!')
                else:
                    print('Sorry the data could not be entered either due to either incorrect format or duplicate values')

            if action == 'd':
                result = delete_new_game(mydb, mycursor, game_data['g_id'])
                if result == 1:
                    print('Successfully deleted data!')
                    action = 'c'
                if result == 0:
                    print('Sorry the data could not be deleted due to invalid game name')


def new_game_id(cursor, date):
    sql = 'SELECT max(g_id) FROM Games where year(date) = \'{year}\';'
    sql = sql.format(year=date.year)
    cursor.execute(sql)
    new_g_id = cursor.fetchall()[0][0]
    if new_g_id is None:
        new_g_id = date.year * 100000 + 1
    else:
        new_g_id += 1
    return new_g_id


def get_team_id(cursor, team_name):
    sql = 'SELECT team_id from Teams where team_name = \'{team_name}\''
    sql = sql.format(team_name=team_name)
    cursor.execute(sql)
    return cursor.fetchall()


def insert_new_game(mydb, cursor, game_data):
    sql = 'insert ignore into Games ('

    comma_separator = ''
    for key in game_data.keys():
        sql = sql + comma_separator + key
        comma_separator = ', '

    sql = sql + ') values ('
    comma_separator = ''
    for val in game_data.values():
        if isinstance(val, str) or isinstance(val, datetime):
            data = '\'' + str(val) + '\''
        elif val is not None:
            data = str(val)
        else:
            data = 'null'
        sql = sql + comma_separator + data
        comma_separator = ', '

    sql = sql + ');'
    cursor.execute(sql)
    mydb.commit()
    cursor.fetchall()
    return cursor.rowcount


def update_data(cursor, game_data, updates):
    while True:
        print('\n')
        print('Which field would you like to update: ')
        edit_dict = {}
        i = 1
        for key, val in game_data.items():
            if key == 'g_id':
                continue
            print(str(i) + '. ' + key.replace('_', ' ').capitalize() + ': ' + str(val))
            edit_dict[i] = key
            i += 1
        print(str(i) + '. Cancel')

        field = input('Enter your choice: ')
        try:
            field = int(field)
        except ValueError:
            print('Please enter a number between 1 and ' + str(i))
            continue

        if field < 1 or field > i:
            print('Please enter a number between 1 and ' + str(i))
            continue

        if field == i:
            return len(updates) > 0

        if edit_dict[field] == 'home_team':
            home_team = get_team_id(cursor, input('Enter Home Team: '))
            updates['home_team'] = game_data['home_team'] = home_team[0][0] if home_team else None

        elif edit_dict[field] == 'away_team':
            away_team = get_team_id(cursor, input('Enter Away Team: '))
            updates['away_team'] = game_data['away_team'] = away_team[0][0] if away_team else None

        elif edit_dict[field] == 'date':
            old_date = game_data['date']

            while True:
                year = input('Enter the year this game was played in: ')
                month = input('Enter the month this game was played in (as number): ')
                day = input('Enter the day of the month this game was played in: ')

                try:
                    date = datetime.strptime(day + ' ' + month + ' ' + year, '%d %m %Y')
                except ValueError:
                    print('You did not enter a valid date')
                    continue
                break

            updates['date'] = game_data['date'] = date

            if old_date.year != date.year:
                updates['g_id'] = game_data['g_id'] = new_game_id(cursor, date),

        elif edit_dict[field] == 'home_final_score':
            while True:
                try:
                    home_score = int(input('Enter Home Score: '))
                except ValueError:
                    print('Please enter an integer')
                    continue
                break
            updates['home_final_score'] = game_data['home_final_score'] = home_score

        elif edit_dict[field] == 'away_final_score':
            while True:
                try:
                    away_score = int(input('Enter Away Score: '))
                except ValueError:
                    print('Please enter an integer')
                    continue
                break
            updates['away_final_score'] = game_data['away_final_score'] = away_score

        elif edit_dict[field] == 'elapsed_time':
            while True:
                try:
                    elapsed_time = int(input('Enter game duration in minutes: '))
                except ValueError:
                    print('Please enter an integer')
                    continue
                break
            updates['elapsed_time'] = game_data['elapsed_time'] = elapsed_time

        elif edit_dict[field] == 'start_time':
            updates['start_time'] = game_data['start_time'] = input('Enter game start time (HH:MM AM/PM): ')

        elif edit_dict[field] == 'venue_name':
            updates['venue_name'] = game_data['venue_name'] = input('Venue: ')

        elif edit_dict[field] == 'attendance':
            while True:
                try:
                    attendance = int(input('Enter attendance: '))
                except ValueError:
                    print('Please enter an integer')
                    continue
                break
            updates['attendance'] = game_data['attendance'] = attendance

        elif edit_dict[field] == 'delay':
            while True:
                try:
                    delay = int(input('Enter game delay (in minutes): '))
                except ValueError:
                    print('Please enter an integer')
                    continue
                break
            updates['delay'] = game_data['delay'] = delay

        elif edit_dict[field] == 'umpire_1B':
            updates['umpire_1B'] = game_data['umpire_1B'] = input('Enter 1B Umpire: ')

        elif edit_dict[field] == 'umpire_2B':
            updates['umpire_2B'] = game_data['umpire_2B'] = input('Enter 2B Umpire: ')

        elif edit_dict[field] == 'umpire_3B':
            updates['umpire_3B'] = game_data['umpire_3B'] = input('Enter 3B Umpire: ')

        elif edit_dict[field] == 'umpire_HP':
            updates['umpire_HP'] = game_data['umpire_HP'] = input('Enter HP Umpire: ')

        elif edit_dict[field] == 'weather':
            temperature = input('Enter temperature on game day (Fahrenheit): ')
            print('Choose weather condition')
            for key, val in weather_dict.items():
                print(str(key) + '. ' + val)

            while True:
                weather_conditions = input('Enter choice: ')
                try:
                    weather_conditions = int(weather_conditions)
                except ValueError:
                    print('Please enter a number between 1 and 10')
                    continue

                if weather_conditions < 1 or weather_conditions > 10:
                    print('Please enter a number between 1 and 10')
                    continue
                break

            updates['weather'] = game_data['weather'] = temperature + ' degrees, ' + weather_dict[weather_conditions].lower()

        elif edit_dict[field] == 'wind':
            wind = input('Enter wind speed (in mph): ')
            updates['wind'] = game_data['wind'] = wind + ' mph,'

        continue_updating = input('Type y to continue updating data: ')
        if continue_updating == 'y':
            continue

        return True


def update_new_game(mydb, cursor, updates, game_id):
    sql = 'update ignore Games set '

    comma_separator = ''
    for key, val in updates.items():
        if isinstance(val, str) or isinstance(val, datetime):
            data = '\'' + str(val) + '\''
        elif val is not None:
            data = str(val)
        else:
            data = 'null'

        sql = sql + comma_separator + key + ' = ' + data
        comma_separator = ', '

    sql = sql + ' where g_id = ' + str(game_id) + ';'

    cursor.execute(sql)
    mydb.commit()
    cursor.fetchall()
    return cursor.rowcount


def delete_new_game(mydb, cursor, game_id):
    sql = 'delete from Games where g_id = \'{game_id}\';'
    sql = sql.format(game_id=game_id)
    cursor.execute(sql)
    mydb.commit()
    cursor.fetchall()
    return cursor.rowcount
