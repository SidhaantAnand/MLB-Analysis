from requestData.request_player import *
from searchPython.batter_queries import *


def ask_batter(mydb, cursor):

    while True:
        print("1. View number of ejections")
        print("2. View outs, hits, and homeruns")
        print("3. Most played inning")
        print("4. Preferred stand")
        print("5. Best pitch type")
        print("6. Worst pitch type")
        print("7. Batters with best ball-strike ratio")
        print("8. Batters with worst ball-strike ratio")
        print("9. Batters with best hits-games ratio")
        print("10. Batters with worst hits-games ratio")
        print("11. Batters with best homeruns-games ratio")
        print("12. Batters with worst homeruns-games ratio")
        print("13. Back")
        option = input('Enter your choice: ')
        print('\n')

        try:
            option = int(option)
        except ValueError:
            print('Error: You must enter an integer between 1 and 13\n')
            continue
        if option < 1 or option > 13:
            print('Invalid option, please choose between 1 and 13\n')
            continue

        if option == 1:
            player_name = request_player(cursor)
            result = player_ejections(cursor, player_name[1])
            print('Total number of ejections for ' + str(player_name[0]) + ' is ' + str(result[0][0]))

        elif option == 2:
            player_name = request_player(cursor)
            result = player_hits_outs(cursor, player_name[1])
            print('Total number of outs for ' + str(player_name[0]) + ' is ' + str(result[0][0]))
            print('Total number of hits for ' + str(player_name[0]) + ' is ' + str(result[0][1]))
            print('Total number of homeruns for ' + str(player_name[0]) + ' is ' + str(result[0][2]))

        elif option == 3:
            player_name = request_player(cursor)
            result = player_inning(cursor, player_name[1])
            print(str(player_name[0]) + ' played the most at inning ' + str(result[0][0]) + ' a total of ' + str(result[0][1]))

        elif option == 4:
            player_name = request_player(cursor)
            result = player_stand(cursor, player_name[1])
            print('Preferred side of ' + str(player_name[0]) + ' is ' + str(result[0][0]))

        elif option == 5:
            player_name = request_player(cursor)
            result = player_best_pitch_type(cursor, player_name[1])
            print('Best pitch for ' + str(player_name[0]) + ' to bat at is ' + str(result[0][0]))

        elif option == 6:
            player_name = request_player(cursor)
            result = player_worst_pitch_type(cursor, player_name[1])
            print('Worst pitch for ' + str(player_name[0]) + ' to bat at is ' + str(result[0][0]))

        elif option == 7:
            result = best_batter_bsratio(cursor)
            print("These are the batters with the best ball-strike ratio")
            for x in result:
                print(x[0] + " with a ball-strike ratio of " + str(x[1]))

        elif option == 8:
            result = worst_batter_bsratio(cursor)
            print("These are the batters with the worst ball-strike ratio")
            for x in result:
                print(x[0] + " with a ball-strike ratio of " + str(x[1]))

        elif option == 9:
            result = best_batter_hgratio(cursor)
            print("These are the batters with the best hits-games ratio")
            for x in result:
                print(x[0] + " with a hits-games ratio of " + str(x[1]))

        elif option == 10:
            result = worst_batter_hgratio(cursor)
            print("These are the batters with the worst hits-games ratio")
            for x in result:
                print(x[0] + " with a hits-games ratio of " + str(x[1]))

        elif option == 11:
            result = best_batter_hrgratio(cursor)
            print("These are the batters with the best homeruns-games ratio")
            for x in result:
                print(x[0] + " with a homeruns-games ratio of " + str(x[1]))

        elif option == 12:
            result = worst_batter_hrgratio(cursor)
            print("These are the batters with the worst homeruns-games ratio")
            for x in result:
                print(x[0] + " with a homeruns-games ratio of " + str(x[1]))

        elif option == 13:
            print("\033c", end="")
            return

        print('\n')
