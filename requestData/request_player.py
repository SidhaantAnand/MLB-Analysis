def request_player(cursor):
    sql = ''' SELECT player_id,CONCAT(first_name, " ", last_name) AS player_name FROM Players; '''
    players = {}
    cursor.execute(sql)
    result = cursor.fetchall()
    for x in result:
        players[x[1]] = x[0]

    exception_players = []

    while (True):
        option = raw_input('Enter a player name: ')
        option = str(option)
        if(option in players):
            return [option,players[option]]
        else:
            print("No such player found")




