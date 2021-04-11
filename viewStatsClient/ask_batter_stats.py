from request_player import *
from batter_queries import *
def ask_batter(mydb,cursor):
    print("1. player_ejections")
    print("2. player_hits_outs")
    print("3. player_inning")
    print("4. player_stand")
    print("5. player_best_pitch_type")
    print("6. player_worst_pitch_type")
    print("7. best_batter_bsratio")
    print("8. worst_batter_bsratio")
    print("9. best_batter_hgratio")
    print("10. worst_batter_hgratio")
    print("11. best_batter_hrgratio")
    print("12. worst_batter_hrgratio")

    while(True):
        option = input('Enter your choice: ')
        try:
            option = int(option)
        except ValueError:
            print('Error: You must enter an integer between 1 and 12')
            continue
        if option < 1 or option > 12:
            print('Invalid option, please choose between 1 and 12')
            continue
        if(option == 1):
            player_name = request_player(cursor)
            result = player_ejections(cursor, player_name[0])
            print('Total number of ejections for ' + str(player_name[0]) + ' is ' + str(result[0][0]))
        elif(option == 2):
            player_name = request_player(cursor)
            result = player_hits_outs(cursor, player_name[0])
            print('Total number of outs for ' + str(player_name[0]) + ' is ' + str(result[0][0]))
            print('Total number of hits for ' + str(player_name[0]) + ' is ' + str(result[0][1]))
            print('Total number of homeruns for ' + str(player_name[0]) + ' is ' + str(result[0][2]))
        elif(option == 3):
            player_name = request_player(cursor)
            result = player_inning(cursor, player_name[0])
            print(str(player_name[0]) + ' played the most at inning' + str(result[0][0]) + ' a total of ' + str(result[0][1]))
        elif (option == 4):
            player_name = request_player(cursor)
            result = player_stand(cursor, player_name[0])
            print('Prefered side of ' + str(player_name[0]) + ' is ' + str(result[0][0]))
        elif (option == 5):
            player_name = request_player(cursor)
            result = player_best_pitch_type(cursor, player_name[0])
            print('Best pitch for ' + str(player_name[0]) + ' to bat at is ' + str(result[0][0]))
        elif (option == 6):
            player_name = request_player(cursor)
            result = player_worst_pitch_type(cursor, player_name[0])
            print('Worst pitch for ' + str(player_name[0]) + ' to bat at is ' + str(result[0][0]))
        elif (option == 7):
            result = best_batter_bsratio(cursor)
            print("These are the batters with the best bs ratio")
            for x in result:
                print(x[0] + " with a BS ratio of " + str(x[1]))
        elif (option == 8):
            result = worst_batter_bsratio(cursor)
            print("These are the batters with the worst bs ratio")
            for x in result:
                print(x[0] + " with a BS ratio of " + str(x[1]))
        elif (option == 9):
            result = best_batter_hgratio(cursor)
            print("These are the batters with the best hgr ratio")
            for x in result:
                print(x[0] + " with a hgr ratio of " + str(x[1]))
        elif (option == 10):
            result = worst_batter_hgratio(cursor)
            print("These are the batters with the worst hgr ratio")
            for x in result:
                print(x[0] + " with a hgr ratio of " + str(x[1]))
        elif (option == 11):
            result = best_batter_hrgratio(cursor)
            print("These are the batters with the best hrg ratio")
            for x in result:
                print(x[0] + " with a hrg ratio of " + str(x[1]))
        elif (option == 12):
            result = worst_batter_hrgratio(cursor)
            print("These are the batters with the worst hrg ratio")
            for x in result:
                print(x[0] + " with a hrg ratio of " + str(x[1]))
