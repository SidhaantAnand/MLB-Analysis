def request_team_id(cursor):
	sql = ''' SELECT team_id, team_name FROM Teams; '''
	cursor.execute(sql)
	result = cursor.fetchall()
	teams = {}
	for x in result:
		teams[x[1]] = x[0]

	option = input('Enter a team: ')
	option = str(option)
	if option in teams.keys():
		return teams[option], option
	else:
		print("Incorrect team entered")
		return None


def request_team_name(cursor, team_id):
	sql = 'SELECT team_name FROM Teams where team_id = \'{team_id}\';'
	sql = sql.format(team_id=team_id)
	cursor.execute(sql)
	return cursor.fetchall()[0][0]
