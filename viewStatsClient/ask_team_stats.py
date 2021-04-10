import sys
from team_queries import *
from request_team import *

def ask_team(mydb,cursor):
	print("1: Win ratio for every team")
	print("2: Best win ratio amongst all teams")
	print("3: A team of your choosings win ratio vs all other teams")
	print("4: Which team does a team of your choosing has the best win record against")
	print("5: Home record for every team")
	print("6: Which team has the best home record")
	print("7: Top 5 batters with the best homeruns:bat sessions ratio for any team of your choosing")
	print("8: Top 5 pitchers with the best homeruns:pitches ratio for any team of your choosing")
	print("9: Top 5 players with the most appearences for any team of your choosing")
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
			result = win_ratio_per_team(cursor)
			print("These are the win ratios of all the MLB teams")
			for x in result:
				print(x[1] + " " + str(x[0]))
		elif(option == 2):
			result = best_win_ratio(cursor)
			print(result[0][1] + " has the best win ratio amongst all teams = " + str(result[0][1]))
		elif(option == 3):
			team = request_team(cursor)
			result = win_ratio_vs_every_team(cursor,team)
			print("These are the win ratio of " + str(team) + " vs all MLB teams")
			for x in result:
				print(x[1] + " " + str(x[0]))
		elif(option == 4):
			team = request_team(cursor)
			result = best_team_to_play_against(cursor,team)
			print("Best win record of " + str(team) + " is with " + result[0][1] + " = " + str(result[0][0]))
		elif(option == 5):
			print("These are the home record of every team")
			result =  home_record_every_team(cursor)
			for x in result:
				print(x[1] + " " + str(x[0]))
		elif(option == 6):
			result = best_home_record(cursor)
			print(result[0][1] + " has the best home record = " + str(result[0][0]))
		elif(option == 7):
			team = request_team(cursor)
			result = top_batters_in_terms_of_homeruns(cursor,team)
			print("These are the batters with the highest homeruns:bat sessions ratio who played for " + str(team))
			for x in result:
				print(x[0] + " " + str(x[1]))
		elif(option == 8):
			team = request_team(cursor)
			result =  top_pitchers_in_terms_of_strikeout(cursor,team)
			print("These are the batters with the highest strikeouts:pitches ratio who played for " + str(team))
			for x in result:
				print(x[0] + " " + str(x[1]))
		elif(option == 9):
			team = request_team(cursor)
			result =  most_player_apps(cursor,team)
			print("These are the players with the most appearences for " + str(team))
			for x in result:
				print(x[0] + " " + str(x[1]))
		break