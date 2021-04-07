def insert_new_player(mydb, mycursor, player_data):
    get_max = 'select max( player_id ) from Players;'
    mycursor.execute(get_max)
    myresult = mycursor.fetchall()
    new_id = (myresult[0][0] + 1)
    sql = f"""insert ignore into Players (player_id, first_name, last_name) 
                values ({new_id}, '{player_data['first_name']}', 
                '{player_data['last_name']}');"""
    mycursor.execute(sql)
    mydb.commit()
    myresult = mycursor.fetchall()
    return mycursor.rowcount, new_id

def update_new_player(mydb, mycursor, player_data, index, field):
    if index == 0:
        sql = f"""update Players set Players.first_name = '{field}' where Players.player_id = '{player_data['player_id']}' """
    if index == 1:
        sql = f"""update Players set Players.last_name = '{field}' where Players.player_id = '{player_data['player_id']}' """
    mycursor.execute(sql)
    mydb.commit()
    myresult = mycursor.fetchall()
    return mycursor.rowcount

def delete_new_player(mydb, mycursor, player_id):
    sql = f"""delete from Players where player_id = '{player_id}';"""
    mycursor.execute(sql)
    mydb.commit()
    myresult = mycursor.fetchall()
    return mycursor.rowcount

def add_new_player(mydb, mycursor):
    first_name = input('Enter First Name: ')
    last_name = input('Enter Last Name: ')
    player_data = ({'player_id': -1, 'first_name': first_name, 'last_name': last_name})
    result, new_id = insert_new_player(mydb, mycursor, player_data)
    if result == 0:
        print('Sorry the data could not be entered either due to either incorrect format or duplicate values')
    else:
        player_data['player_id'] = new_id
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
                    result = update_new_player(mydb, mycursor, player_data, 0, first_name)
                elif field == 2:
                    last_name = input('Updated Last Name: ')
                    result = update_new_player(mydb, mycursor, player_data, 1, last_name)
                else:
                    print('Sorry invalid field number was entered')
                if result == 1:
                    print('\n')
                    print('Successfully Updated data! The following data was entered:')
                    if field == 1:
                        player_data['first_name'] = first_name
                    if field == 2:
                        player_data['last_name'] = last_name
                    print('First Name: ', player_data['first_name'])
                    print('Last Name: ', player_data['last_name'])
                else:
                    print('Sorry the data could not be entered either due to either incorrect format or duplicate values')
        
            if action == 'd':
                result = delete_new_player(mydb, mycursor, player_data['player_id'])
                if result == 1:
                    print('Successfully deleted data!')
                    action = 'c'
                if result == 0:
                    print('Sorry the data could not be deleted due to invalid player name')
