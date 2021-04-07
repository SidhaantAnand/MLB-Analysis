def insert_new_team(mydb, mycursor, team_data):
    sql = f"""insert ignore into Teams (team_id, team_name) 
        values ('{team_data['team_id']}', '{team_data['team_name']}');"""
    mycursor.execute(sql)
    mydb.commit()
    myresult = mycursor.fetchall()
    return mycursor.rowcount

def update_new_team(mydb, mycursor, team_data, index, field):
    if index == 0:
        sql = f"""with temp_team as
                (select * from Teams)
                update Teams
                inner join temp_team using(team_id)
                set team_id = '{field}' where team_id = '{team_data['team_id']}'
                and not exists (select * from temp_team where team_id = '{field}'); """
    if index == 1:
        sql = f"""update Teams set team_name = '{field}' where team_id = '{team_data['team_id']}';"""
    mycursor.execute(sql)
    mydb.commit()
    myresult = mycursor.fetchall()
    return mycursor.rowcount

def delete_new_team(mydb, mycursor, team_id):
    sql = f"""delete from Teams where team_id = '{team_id}';"""
    mycursor.execute(sql)
    mydb.commit()
    myresult = mycursor.fetchall()
    return mycursor.rowcount

def add_new_team(mydb, mycursor):
    team_name = input('Enter Team Name: ')
    team_id = input('Enter Team Short Name (3 letter identifier): ')
    team_data = ({'team_name': team_name, 'team_id': team_id})
    result = insert_new_team(mydb, mycursor, team_data)
    if result == 0:
        print('Sorry the data could not be entered either due to either incorrect format or duplicate values')
    else:
        print('\n')
        print('Successfully inserted data! The following data was entered:')
        print('Team Name: ', team_name)
        print('Team Id: ', team_id)
        action = 'random string'
        while action != 'c':
            action = input('See a mistake? Enter (u) to update, (d) to delete or (c) to continue: ')
            result = 0
            if action == 'u':
                print('\n')
                print('Which field would you like to update: ')
                print('1. Team Name')
                print('2. Team Id')
                field = int(input('Enter your choice: '))
                if field == 1:
                    team_name = input('Updated Team Name: ')
                    result = update_new_team(mydb, mycursor, team_data, 1, team_name)
                elif field == 2:
                    team_id = input('Updated Team Id: ')
                    result = update_new_team(mydb, mycursor, team_data, 0, team_id)
                else:
                    print('Sorry invalid field number was entered')
                if result == 1:
                    print('\n')
                    print('Successfully Updated data! The following data was entered:')
                    if field == 1:
                        team_data['team_name'] = team_name
                    if field == 2:
                        team_data['team_id'] = team_id
                    print('Team Name: ', team_data['team_name'])
                    print('Team Id: ', team_data['team_id'])
                if result == 0:
                    print('Sorry the data could not be entered either due to either incorrect format or duplicate values')
        
            if action == 'd':
                result = delete_new_team(mydb, mycursor, team_data['team_id'])
                if result == 1:
                    print('Successfully deleted data!')
                    action = 'c'
                if result == 0:
                    print('Sorry the data could not be deleted due to invalid team id')
        

    

