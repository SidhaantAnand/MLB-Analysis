from requestData.request_team import request_team_name
from searchPython.game_queries import *


def ask_game(mydb, cursor):
    print("1. Game with the highest home score")
    print("2. Game with the highest away score")
    print("3. Game with the highest combined score")
    print("4. Game with the highest attendance")
    print("5. Game with the lowest attendance")
    print("6. Games with minimum home score")
    print("7. Games with minimum away score")
    print("8. Longest game")
    print("9. Most innings in a game")
    print("10. Shortest game")
    print("11. Longest winning streak")
    print("12. Longest losing streak")

    while True:
        option = input('Enter your choice: ')
        try:
            option = int(option)
        except ValueError:
            print('Error: You must enter an integer between 1 and 9')
            continue
        if option < 1 or option > 12:
            print('Invalid option, please choose 1 or 2')
            continue

        if option == 1:
            result = highest_home_score(cursor)
            print("These are the games with the highest home scores:")
            for x in result:
                print(str(x[0]) + " vs " + str(x[1]) + " on " + str(x[2]) + " with score " + str(x[3]) + " : " + str(x[4]))

        elif option == 2:
            result = higher_than_away_score(cursor)
            print("These are the games with the highest away scores:")
            for x in result:
                print(str(x[0]) + " vs " + str(x[1]) + " on " + str(x[2]) + " with score " + str(x[3]) + " : " + str(x[4]))

        elif option == 3:
            result = highest_combined_score(cursor)
            print("These are the games with the highest combined scores:")
            for x in result:
                print(str(x[0]) + " vs " + str(x[1]) + " on " + str(x[2]) + " with score " + str(x[3]) + " : " + str(x[4]))

        elif option == 4:
            result = highest_attendance(cursor)
            print("These are games with highest attendance ie " + str(result[0][3]) + " : ")
            for x in result:
                print(str(x[0]) + " vs " + str(x[1]) + " on " + str(x[2]))

        elif option == 5:
            result = lowest_attendance(cursor)
            print("These are games with lowest attendance ie " + str(result[0][3]) + " : ")
            for x in result:
                print(str(x[0]) + " vs " + str(x[1]) + " on " + str(x[2]))

        elif option == 6:
            score = input("Enter minimum score: ")
            try:
                score = int(score)
            except ValueError:
                print("Error: Score needs to be an integer")
                continue

            result = higher_than_home_score_val(cursor, score)
            print("There have been " + str(result[0][0]) + " games with a home score equal to or higher than " + str(score))

        elif option == 7:
            score = input("Enter minimum score: ")
            try:
                score = int(score)
            except ValueError:
                print("Error: Score needs to be an integer")
                continue

            result = higher_than_home_score_val(cursor, score)
            print("There have been " + str(result[0][0]) + " games with an away score equal to or higher than " + str(score))

        elif option == 8:
            result = Longest_game_elapsed_time(cursor)
            away_team = request_team_name(cursor, result[1])
            home_team = request_team_name(cursor, result[0])
            print("The game with the longest elapsed time was the " + away_team + " at the " + home_team + " for " + str(result[3]) + " minutes, on " + str(result[2].date()))

        elif option == 9:
            result = Longest_game_innings(cursor)
            print("There have been " + str(len(result)) + " games with a high of " + str(result[0][1]) + " innings. They are: ")
            for x in result:
                away_team = request_team_name(cursor, x[3])
                home_team = request_team_name(cursor, x[2])
                print(away_team + " at " + home_team + " on " + str(x[4].date()))

        elif option == 10:
            result = Shortest_game_elapsed_time(cursor)
            away_team = request_team_name(cursor, result[1])
            home_team = request_team_name(cursor, result[0])
            print("The game with the shortest elapsed time was the " + away_team + " at the " + home_team + " for " + str(result[3]) + " minutes, on " + str(result[2].date()))

        elif option == 11:
            result = Longest_winning_streak(mydb, cursor)
            team = request_team_name(cursor, result[0])
            print("The longest winning streak was by the " + team + " for " + str(result[1]) + " games")

        elif option == 12:
            result = Longest_losing_streak(mydb, cursor)
            team = request_team_name(cursor, result[0])
            print("The longest losing streak was by the " + team + " for " + str(result[1]) + " games")

        continue
