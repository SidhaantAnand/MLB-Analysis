from request_player import *
from pitcher_queries import *
def ask_pitcher(mydb,cursor):
    print("1. Number_of_strikes_pitched")
    print("2. Number_of_strikeouts")
    print("3. Number_of_balls_pitched")
    print("4. Number_of_home_runs_allowed")
    print("5. Total_pitches")
    print("6. Average_spin_rate_and_direction")
    print("7. Average_pitch_speed")
    print("8. Most_common_zone_pitched")
    print("9. Preferred_throwing_side")
    print("10. Most_common_pitch_type")
    print("11. consolidated_stats_pitcher")
    print("12. best_pitcher")
    print("13. Worst_pitcher")

    while (True):
        option = input('Enter your choice: ')
        try:
            option = int(option)
        except ValueError:
            print('Error: You must enter an integer between 1 and 13')
            continue
        if option < 1 or option > 13:
            print('Invalid option, please choose between 1 and 13')
            continue

        if(option == 1):
            player_name = request_player(cursor)
            result = Number_of_strikes_pitched(cursor,player_name[1])
            print(player_name[0] + ' has pitched a total of ' + str(result[0][0]) + ' strikes')
        elif(option == 2):
            player_name = request_player(cursor)
            result = Number_of_strikeouts(cursor,player_name[1])
            print(player_name[0] + ' has a total of ' + str(result[0][0]) + ' strikeouts')
        elif(option == 3):
            player_name = request_player(cursor)
            result = Number_of_balls_pitched(cursor,player_name[1])
            print(player_name[0] + ' has a total of ' + str(result[0][0]) + ' pitches')
        elif (option == 4):
            player_name = request_player(cursor)
            result = Number_of_home_runs_allowed(cursor,player_name[1])
            print(player_name[0] + ' has allowed a total of ' + str(result[0][0]) + ' homeruns')
        elif (option == 5):
            player_name = request_player(cursor)
            result = Total_pitches(cursor,player_name[1])
            print(player_name[0] + ' has allowed a total of ' + str(result[0][0]) + ' pitches')
        elif (option == 6):
            player_name = request_player(cursor)
            result = Average_spin_rate_and_direction(cursor,player_name[1])
            print(player_name[0] + ' has an average spin rate of ' + str(result[0][0]))
            print(player_name[0] + ' has an average spin direction of ' + str(result[0][1]))
        elif (option == 7):
            player_name = request_player(cursor)
            result = Average_pitch_speed(cursor,player_name[1])
            print(player_name[0] + ' has an average spin speed of ' + str(result[0][0]))
        elif (option == 8):
            player_name = request_player(cursor)
            result = Most_common_zone_pitched(cursor,player_name[1])
            print(player_name[0] + ' pitches the most at zone ' + str(result[0][0]) + ' with a total of ' + str(result[0][1]) + 'pitches')
        elif (option == 9):
            player_name = request_player(cursor)
            result = Preferred_throwing_side(cursor,player_name[1])
            print(player_name[0] + ' preferred throwing side is ' + str(result[0][0]))
        elif (option == 10):
            player_name = request_player(cursor)
            result = Most_common_pitch_type(cursor,player_name[1])
            print(player_name[0] + ' pitches the most of type ' + str(result[0][0]) + ' with a total of ' + str(result[0][1]) + 'pitches')
        elif (option == 11):
            player_name = request_player(cursor)
            result = consolidated_stats_pitcher(cursor,player_name[1])
        elif (option == 12):
            result = best_pitcher(cursor)
            print('Top 5 pitchers with the best strikeouts:pitches ratio')
            for x in result:
                print(str(x[0]) + ' with ratio ' + str(x[1]))
        elif(option == 13):
            result = Worst_pitcher(cursor)
            print('Worst 5 pitchers with the best strikeouts:pitches ratio')
            for x in result:
                print(str(x[0]) + ' with ratio ' + str(x[1]))
        return