from game_queries import *
def ask_game(mydb,cursor):
    print("1. highest_home_score")
    print("2. higher_than_away_score")
    print("3. highest_combined_score")
    print("4. highest_attendance")
    print("5. lowest_attendance")
    print("6. higher_than_home_score")
    print("7. higher_than_away_score")
    print("8. Longest_game_elapsed_time")
    print("9. Longest_game_innings")
    print("10. Shortest_game_elapsed_time")
    print("11. Longest_winning_streak")
    print("12. Longest_losing_streak")

    while (True):
        option = input('Enter your choice: ')
        try:
            option = int(option)
        except ValueError:
            print('Error: You must enter an integer between 1 and 9')
            continue
        if option < 1 or option > 12:
            print('Invalid option, please choose 1 or 2')
            continue

        if (option == 1):
            result = highest_home_score(cursor)
            print("These are the games with the highest home scores:")
            for x in result:
                print(str(x[0]) + " vs " + str(x[1]) + " on " + str(x[2]) + " with score " + str(x[3]) + " : " + str(x[4]))
        elif (option == 2):
            result = higher_than_away_score(cursor)
            print("These are the games with the highest away scores:")
            for x in result:
                print(str(x[0]) + " vs " + str(x[1]) + " on " + str(x[2]) + " with score " + str(x[3]) + " : " + str(x[4]))
        elif (option == 3):
            result = highest_combined_score(cursor)
            print("These are the games with the highest combined scores:")
            for x in result:
                print(str(x[0]) + " vs " + str(x[1]) + " on " + str(x[2]) + " with score " + str(x[3]) + " : " + str(x[4]))
        elif (option == 4):
            result = highest_attendance(cursor)
            print("These are games with highest attendance:")
            for x in result:
                print(str(x[0]) + " vs " + str(x[1]) + " on " + str(x[2]) + " with attedance " + str(x[3]))
        elif (option == 5):
            result = lowest_attendance(cursor)
            print(str(x[0]) + " vs " + str(x[1]) + " on " + str(x[2]) + " with attedance " + str(x[3]))
        elif (option == 6):
            result = higher_than_home_score_val(cursor)
        elif (option == 7):
            result = higher_than_away_score_val(cursor)
        elif (option == 8):
            result = Longest_game_elapsed_time(cursor)
        elif (option == 9):
            result = Longest_game_innings(cursor)
        elif (option == 9):
            result = Longest_game_innings(cursor)
        elif (option == 10):
            result = Shortest_game_elapsed_time(cursor)
        elif (option == 11):
            result = Longest_winning_streak(cursor)
        elif (option == 12):
            result = Longest_losing_streak(cursor)
        continue