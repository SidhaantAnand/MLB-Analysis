from requestData.request_venue import *
from searchPython.venue_queries import *


def ask_venue(mydb, cursor):
    print("1. avg_attendance_per_venue")
    print("2. venue_with_most_average_attendance")
    print("3. best_game_attendance_per_venue")
    print("4. best_attendance_ever")
    print("5. most_games_played_at_venue")
    print("6. total_games_per_venue")
    print("7. avergae_score_per_venue")
    print("8. highest_average_across_all_venues")
    print("9. highest_scoring_game_for_venue")
    print("10. highest_scoring_games_across_all_venues")
    print("11. delay_games_per_venue")
    print("12. most_delayed_games")
    print("13. avg_temp_per_venue")

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
            result = avg_attendance_per_venue(cursor,venue_name)
            print("Average attendance for " + venue_name + " is " + str(result[0][0]))
        elif option == 2:
            result = venue_with_most_average_attendance(cursor)
            print(result[0][0])
        elif option == 3:
            venue_name = request_venue(cursor)
            result = best_game_attendance_per_venue(cursor,venue_name)
            print('These are the games played at ' + str(venue_name) + ' with the most attendance')
        elif option == 4:
            result = best_attendance_ever(cursor)
            print(result[0][0])
        elif option == 5:
            venue_name = request_venue(cursor)
            result = most_games_played_at_venue(cursor,venue_name)
            print(result[0][0])
        elif option == 6:
            venue_name = request_venue(cursor)
            result = total_games_per_venue(cursor,venue_name)
            print(result[0][0])
        elif option == 7:
            venue_name = request_venue(cursor)
            result = average_score_per_venue(cursor,venue_name)
            print(result[0][0])
        elif option == 8:
            result = highest_average_across_all_venues(cursor)
            print(result[0][0])
        elif option == 9:
            venue_name = request_venue(cursor)
            result = highest_scoring_game_for_venue(cursor,venue_name)
            print(result[0][0])
        elif option == 10:
            result = highest_scoring_games_across_all_venues(cursor)
            print(result[0][0])
        elif option == 11:
            venue_name = request_venue(cursor)
            result = delay_games_per_venue(cursor,venue_name)
            print(result[0][0])
        elif option == 12:
            result = most_delayed_games(cursor)
            print(result[0][0])
        elif option == 13:
            venue_name = request_venue(cursor)
            result = avg_temp_per_venue(cursor,venue_name)
            print(result[0][0])
        continue
