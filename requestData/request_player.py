def request_player(cursor):
    sql = ''' SELECT player_id, CONCAT(first_name, " ", last_name) AS player_name FROM Players; '''
    players = {}
    duplicate_player_names = {}
    cursor.execute(sql)
    result = cursor.fetchall()
    for x in result:
        if players.get(x[1]):
            duplicate_player_names[x[1]] = [players[x[1]], x[0]]
            players.pop(x[1])
        elif duplicate_player_names.get(x[1]):
            duplicate_player_names.get(x[1]).append(x[0])
        else:
            players[x[1]] = x[0]

    while True:
        option = input('Enter a player name: ')
        if option in players:
            return [option, players[option]]
        elif option in duplicate_player_names:
            print("Multiple players named " + option)
            i = 1
            for ID in duplicate_player_names[option]:
                print(str(i) + '. Player ID:' + str(ID))
                i += 1
            player_id = input('Choose which player you want: ')
            try:
                player_id = int(player_id)
            except ValueError:
                print('Not a valid number')
                continue
            if player_id < 1 or player_id > i:
                print('Invalid option')
                continue
            return [option, duplicate_player_names[option][player_id-1]]
        else:
            print("No such player found")
