from requestData.request_venue import *
from searchPython.venue_queries import *


def ask_venue(mydb, cursor):
    print("1. Average attendance per venue")
    print("2. Venue with the highest average attendance")
    print("3. Highest game attendance per venue")
    print("4. Game and venue with the highest attendance ever")
    print("5. Venue with the highest number of games played")
    print("6. Total games played per venue")
    print("7. Average score per venue")
    print("8. Venue with average score")
    print("9. Highest scoring game per venue")
    print("10. Venue with highest scoring game")
    print("11. Number of delayed games per venue")
    print("12. Venue with the most delayed games")
    print("13. Average temperature per venue")

    while True:
        option = input('Enter your choice: ')
        try:
            option = int(option)
        except ValueError:
            print('Error: You must enter an integer between 1 and 13')
            continue
        if option < 1 or option > 13:
            print('Invalid option, please choose between 1 and 13')
            continue

        if option == 1:
            venue_name = request_venue(cursor)
            result = avg_attendance_per_venue(cursor, venue_name)
            print("Average attendance at " + venue_name + " is " + str(result[0][0]))
        elif option == 2:
            result = venue_with_most_average_attendance(cursor)
            print(result[0][0])
        elif option == 3:
            venue_name = request_venue(cursor)
            result = best_game_attendance_per_venue(cursor, venue_name)
            print(result[0][0])
        elif option == 4:
            result = best_attendance_ever(cursor)
            print(result[0][0])
        elif option == 5:
            result = most_games_played_at_venue(cursor)
            print(result[0][0])
        elif option == 6:
            venue_name = request_venue(cursor)
            result = total_games_per_venue(cursor, venue_name)
            print(result[0][0])
        elif option == 7:
            venue_name = request_venue(cursor)
            result = average_score_per_venue(cursor, venue_name)
            print(result[0][0])
        elif option == 8:
            result = highest_average_across_all_venues(cursor)
            print(result[0][0])
        elif option == 9:
            venue_name = request_venue(cursor)
            result = highest_scoring_game_for_venue(cursor, venue_name)
            print(result[0][0])
        elif option == 10:
            result = highest_scoring_games_across_all_venues(cursor)
            for x in result:
                print(x[0])
        elif option == 11:
            venue_name = request_venue(cursor)
            result = delay_games_per_venue(cursor, venue_name)
            print(str(result[0][0]) + " game(s) have been delayed at " + venue_name)
        elif option == 12:
            result = most_delayed_games(cursor)
            print(result[0][0])
        elif option == 13:
            venue_name = request_venue(cursor)
            result = avg_temp_per_venue(cursor, venue_name)
            print("Average temperature at " + venue_name + " is " + str(result[0][0]))

        continue
