def insert_new_umpire(mydb, mycursor, umpire_data):
    get_max = 'select max( umpire_id ) from Umpires;'
    mycursor.execute(get_max)
    myresult = mycursor.fetchall()
    new_id = (myresult[0][0] + 1)
    sql = f"""insert ignore into Umpires (umpire_id, first_name, last_name, full_name) 
                values ({new_id}, '{umpire_data['first_name']}', 
                '{umpire_data['last_name']}', '{umpire_data['full_name']}');"""
    mycursor.execute(sql)
    mydb.commit()
    myresult = mycursor.fetchall()
    return mycursor.rowcount, new_id

def update_new_umpire(mydb, mycursor, umpire_data, index, full_name, field):
    if index == 0:
        sql = f"""update Umpires set Umpires.first_name = '{field}' where Umpires.umpire_id = '{umpire_data['umpire_id']}' """
    if index == 1:
        sql = f"""update Umpires set Umpires.last_name = '{field}' where Umpires.umpire_id = '{umpire_data['umpire_id']}' """
    mycursor.execute(sql)
    mydb.commit()
    count = mycursor.rowcount
    sql = f"""update Umpires set Umpires.full_name = '{full_name}' where Umpires.umpire_id = '{umpire_data['umpire_id']}' """
    mycursor.execute(sql)
    mydb.commit()
    myresult = mycursor.fetchall()
    count = count + mycursor.rowcount
    return count

def delete_new_umpire(mydb, mycursor, umpire_id):
    sql = f"""delete from Umpires where umpire_id = '{umpire_id}';"""
    mycursor.execute(sql)
    mydb.commit()
    myresult = mycursor.fetchall()
    return mycursor.rowcount

def add_new_umpire(mydb, mycursor):
    first_name = input('Enter First Name: ')
    last_name = input('Enter Last Name: ')
    full_name = first_name + ' ' + last_name
    umpire_data = ({'umpire_id': -1, 'first_name': first_name, 'last_name': last_name, 'full_name': full_name})
    result, new_id = insert_new_umpire(mydb, mycursor, umpire_data)
    if result == 0:
        print('Sorry the data could not be entered either due to either incorrect format or duplicate values')
    else:
        umpire_data['umpire_id'] = new_id
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
                    result = update_new_umpire(mydb, mycursor, umpire_data, 0, full_name, first_name)
                elif field == 2:
                    last_name = input('Updated Last Name: ')
                    full_name = first_name + ' ' + last_name
                    result = update_new_umpire(mydb, mycursor, umpire_data, 1, full_name, last_name)
                else:
                    print('Sorry invalid field number was entered')
                if result == 2:
                    print('\n')
                    print('Successfully Updated data! The following data was entered:')
                    if field == 1:
                        umpire_data['first_name'] = first_name
                    if field == 2:
                        umpire_data['last_name'] = last_name
                        umpire_data['full_name'] = umpire_data['first_name'] + ' ' + umpire_data['last_name']
                    print('First Name: ', umpire_data['first_name'])
                    print('Last Name: ', umpire_data['last_name'])
                else:
                    print('Sorry the data could not be entered either due to either incorrect format or duplicate values')
        
            if action == 'd':
                result = delete_new_umpire(mydb, mycursor, umpire_data['umpire_id'])
                if result == 1:
                    print('Successfully deleted data!')
                    action = 'c'
                if result == 0:
                    print('Sorry the data could not be deleted due to invalid umpire name')
