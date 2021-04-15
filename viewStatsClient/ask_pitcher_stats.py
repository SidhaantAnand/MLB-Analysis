from requestData.request_player import *
from searchPython.pitcher_queries import *


def ask_pitcher(mydb, cursor):
    print("1. Throwing stats")
    print("2. Number of strikeouts")
    print("3. Number of home runs allowed")
    print("4. Most common zone pitched")
    print("5. Preferred throwing side")
    print("6. Most common pitch type")
    print("7. Best pitcher (strikeouts:pitches)")
    print("8. Worst pitcher (strikeouts:pitches)")

    while True:
        option = input('Enter your choice: ')
        try:
            option = int(option)
        except ValueError:
            print('Error: You must enter an integer between 1 and 8')
            continue
        if option < 1 or option > 8:
            print('Invalid option, please choose between 1 and 8')
            continue

        if option == 1:
            player = request_player(cursor)
            result = consolidated_stats_pitcher(cursor, player[1])
            strikes = str(result[0])
            balls = str(result[1])
            pitches = str(result[2])
            spin_rate = str(result[3])
            spin_direction = str(result[4])
            speed = str(result[5])

            print(player[0] + ' has pitched ' + strikes + ' strikes and ' + balls + ' balls from ' + pitches + ' total pitches.')
            print('He pitches at an average speed of ' + speed + ' mph, with the average pitch ' +
                  'spinning at ' + spin_rate + ' revolutions per minute at an angle of ' + spin_direction + ' degrees.')

        elif option == 2:
            player = request_player(cursor)
            result = Number_of_strikeouts(cursor, player[1])
            print(player[0] + ' has a total of ' + str(result[0][0]) + ' strikeouts')

        elif option == 3:
            player = request_player(cursor)
            result = Number_of_home_runs_allowed(cursor, player[1])
            print(player[0] + ' has allowed a total of ' + str(result[0][0]) + ' homeruns')

        elif option == 4:
            player = request_player(cursor)
            result = Most_common_zone_pitched(cursor, player[1])
            print(player[0] + ' pitches the most to zone ' + str(result[0][0]) + ' with a total of ' + str(result[0][1]) + ' pitches')

        elif option == 5:
            player = request_player(cursor)
            result = Preferred_throwing_side(cursor, player[1])
            print(player[0] + '\'s preferred throwing side is ' + str(result[0][0]))

        elif option == 6:
            player = request_player(cursor)
            result = Most_common_pitch_type(cursor, player[1])
            print(player[0] + '\'s most common pitche type is ' + str(result[0][0]) + ' with a total of ' + str(result[0][1]) + ' pitches')

        elif option == 7:
            result = best_pitcher(cursor)
            print('5 pitchers with the best strikeouts:pitches ratio')
            for x in result:
                print(str(x[0]) + ' with ratio ' + str(x[1]))

        elif option == 8:
            result = Worst_pitcher(cursor)
            print('5 pitchers with the worst strikeouts:pitches ratio')
            for x in result:
                print(str(x[0]) + ' with ratio ' + str(x[1]))

        return
