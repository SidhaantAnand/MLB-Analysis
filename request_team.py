def request_team(cursor):
	sql = ''' SELECT DISTINCT(team_id) FROM Teams; '''
	cursor.execute(sql)
	result = cursor.fetchall()
	teams = []
	for x in result:
		teams.append(x[0])
	while(True):
		option = input('Enter a team')
		if(not option in teams):
			print("Incorrect team entered")
		else:
			return option