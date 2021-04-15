def request_team(cursor):
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
