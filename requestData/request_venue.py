def request_venue(cursor):
    sql = ''' SELECT DISTINCT(venue_name) FROM Venue; '''
    cursor.execute(sql)
    result = cursor.fetchall()
    venues = []
    for x in result:
        venues.append(x[0])

    option = input('Enter a venue: ')
    option = str(option)
    if option in venues:
        return option
    else:
        print("No such venue")
        return None
