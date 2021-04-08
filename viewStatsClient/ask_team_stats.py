def ask_team(mydb,cursor):
	print("1: win_ratio_per_team")
	print("2: best_win_ratio")
	print("3: win_ratio_vs_every_team")
	print("4: best_team_to_play_against")
	print("5: home_record_every_team")
	print("6: best_home_record")
	print("7: top_batters_in_terms_of_homeruns")
	print("8: top_pitchers_in_terms_of_strikeout")
	print("9: most_player_apps")
	while(True):
		option = input('Enter your choice: ')
		try:
			option = int(option)
		except ValueError:
			print('Error: You must enter an integer between 1 and 9')
			continue
		if option < 1 or option > 9:
			print('Invalid option, please choose 1 or 2')
			continue

		if(option == 1):
			return win_ratio_per_team(cursor)
		elif(option == 2):
			return best_win_ratio(cursor)
		elif(option == 3):
			team = request_team(cursor)
			return win_ratio_vs_every_team(cursor,team)
		elif(option == 4):
			team = request_team(cursor)
			return best_team_to_play_against(cusor,team)
		elif(option == 5):
			return home_record_every_team(cursor)
		elif(option == 6):
			return best_home_record(cursor)
		elif(option == 7):
			team = request_team(cursor)
			return top_batters_in_terms_of_homeruns(cursor,team)
		elif(option == 8):
			team = request_team(cursor)
			return top_pitchers_in_terms_of_strikeout(cursor,team)
		elif(option == 9):
			team = request_team(cursor)
			return most_player_apps(cursor,team)