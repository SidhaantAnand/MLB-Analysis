def request_player(cursor):
    sql = ''' SELECT player_id, CONCAT(first_name, " ", last_name) AS player_name FROM Players; '''
    players = {}
    duplicate_player_names = {}
    cursor.execute(sql)
    result = cursor.fetchall()
    for x in result:
        if players.get(x[1]):
            duplicate_player_names[x[1]] = x[0]
            players.pop(x[1])
        else:
            players[x[1]] = x[0]

    while True:
        option = input('Enter a player name: ')
        if option in players:
            return [option, players[option]]
        elif option in duplicate_player_names:
            print("Multiple player have that name")
        else:
            print("No such player found")


def get_player_teams(cursor):
    cursor.execute()
