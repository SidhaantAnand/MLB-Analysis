def insert_new_venue(mydb, mycursor, venue_data):
    get_max = 'select max( venue_id ) from Venue;'
    mycursor.execute(get_max)
    myresult = mycursor.fetchall()
    new_id = (myresult[0][0] + 1)
    sql = f"""insert ignore into Venue (venue_id, venue_name) 
                values ({new_id}, '{venue_data['venue_name']}');"""
    mycursor.execute(sql)
    mydb.commit()
    myresult = mycursor.fetchall()
    return mycursor.rowcount, new_id

def update_new_venue(mydb, mycursor, venue_data, field):
    sql = f"""with temp_venue as
        (select * from Venue)
        update Venue
        inner join temp_venue using(venue_id)
        set Venue.venue_name = '{field}' where Venue.venue_id = '{venue_data['venue_id']}'
        and not exists (select * from temp_venue where temp_venue.venue_name = '{field}'); """
    mycursor.execute(sql)
    mydb.commit()
    myresult = mycursor.fetchall()
    return mycursor.rowcount

def delete_new_venue(mydb, mycursor, venue_id):
    sql = f"""delete from Venue where venue_id = '{venue_id}';"""
    mycursor.execute(sql)
    mydb.commit()
    myresult = mycursor.fetchall()
    return mycursor.rowcount

def add_new_venue(mydb, mycursor):
    venue_name = input('Enter VenueName: ')
    venue_data = ({'venueId': -1, 'venue_name': venue_name})
    result, new_id = insert_new_venue(mydb, mycursor, venue_data)
    if result == 0:
        print('Sorry the data could not be entered either due to either incorrect format or duplicate values')
    else:
        venue_data['venue_id'] = new_id
        print('\n')
        print('Successfully inserted data! The following data was entered:')
        print('Venue Name: ', venue_name)
        action = 'random string'
        while action != 'c':
            action = input('See a mistake? Enter (u) to update, (d) to delete or (c) to continue: ')
            result = 0
            if action == 'u':
                print('\n')
                venue_name = input('Enter the venue name: ')
                result = update_new_venue(mydb, mycursor, venue_data, venue_name)
                if result == 1:
                    print('\n')
                    print('Successfully Updated data! The following data was entered:')
                    venue_data['venue_name'] = venue_name
                    print('Venue Name: ', venue_data['venue_name'])
                if result == 0:
                    print('Sorry the data could not be entered either due to either incorrect format or duplicate values')
        
            if action == 'd':
                result = delete_new_venue(mydb, mycursor, venue_data['venue_id'])
                if result == 1:
                    print('Successfully deleted data!')
                    action = 'c'
                if result == 0:
                    print('Sorry the data could not be deleted due to invalid venue name')
