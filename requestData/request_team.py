def request_team(cursor):
	sql = ''' SELECT DISTINCT(team_id) FROM Teams; '''
	cursor.execute(sql)
	result = cursor.fetchall()
	teams = []
	for x in result:
		teams.append(x[0])
	while(True):
		option = raw_input('Enter a team: ')
		option = str(option)
		if(option in teams):
			return option
		else:
			print("Incorrect team entered")