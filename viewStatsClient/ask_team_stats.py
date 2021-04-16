from requestData.request_team import *
from searchPython.team_queries import *


def ask_team(mydb, cursor):

	while True:
		print("1. Win ratio for every team")
		print("2. Best win ratio amongst all teams")
		print("3. Per team win ratio vs all other teams")
		print("4. Per team best win record against")
		print("5. Home record per team")
		print("6. Team with the best home record")
		print("7. Top 5 batters with the best hits:bat-sessions ratio per team")
		print("8. Top 5 batters with the most homeruns per team")
		print("9. Top 5 pitchers with the best strikeouts:pitches ratio per team")
		print("10. Top 5 players with the most appearances per team")
		print("11. Back")
		option = input('Enter your choice: ')
		print('\n')

		try:
			option = int(option)
		except ValueError:
			print('Error: You must enter an integer between 1 and 11\n')
			continue
		if option < 1 or option > 11:
			print('Invalid option, please choose between 1 and 11\n')
			continue

		if option in [3, 4, 7, 8, 9, 10]:
			team_info = request_team_id(cursor)
			if team_info is None:
				print('\n')
				continue
			team = team_info[0]
			team_name = team_info[1]

		if option == 1:
			result = win_ratio_per_team(cursor)
			print("These are the win ratios of all the MLB teams")
			for x in result:
				print(x[1] + " " + str(x[0]))

		elif option == 2:
			result = best_win_ratio(cursor)
			print(result[0][1] + " has the best win ratio amongst all teams at " + str(result[0][0]))

		elif option == 3:
			result = win_ratio_vs_every_team(cursor, team)
			print("These are the win ratios of the " + team_name + " vs all MLB teams")
			for x in result:
				print(x[1] + " " + str(x[0]))

		elif option == 4:
			result = best_team_to_play_against(cursor, team)
			print("The " + team_name + " have the best win record against the " + result[0][1] + " at " + str(result[0][0]))

		elif option == 5:
			print("These are the home records of every team")
			result =  home_record_every_team(cursor)
			for x in result:
				print(x[1] + ": " + str(round(x[0]*100, 2)) + "%")

		elif option == 6:
			result = best_home_record(cursor)
			print(result[0][1] + " has the best home record at " + str(round(result[0][0]*100, 2)) + "% of games won")

		elif option == 7:
			result = top_batters_in_terms_of_hits(cursor, team)
			print("These are the batters with the highest hits:bat-sessions ratio who played for the " + team_name)
			for x in result:
				print(x[0] + " " + str(x[1]))

		elif option == 8:
			result = top_batters_in_terms_of_homeruns(cursor, team)
			print("These are the batters with the most homeruns who played for the " + team_name)
			for x in result:
				print(x[0] + " " + str(x[1]))

		elif option == 9:
			result = top_pitchers_in_terms_of_strikeout(cursor, team)
			print("These are the pitchers with the best strikeouts:pitches ratio for the " + team_name)
			for x in result:
				print(x[0] + " " + str(x[1]))

		elif option == 10:
			result = most_player_apps(cursor, team)
			print("These are the players with the most appearances for the " + team_name)
			for x in result:
				print(x[0] + " " + str(x[1]))

		elif option == 11:
			print("\033c", end="")
			return

		print('\n')
