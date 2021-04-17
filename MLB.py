from mysql.connector.errors import DatabaseError, ProgrammingError

from addData.add_data import add_user_data
from create_connection import get_cursor
from viewStatsClient.ask_batter_stats import ask_batter
from viewStatsClient.ask_game_queries import ask_game
from viewStatsClient.ask_pitcher_stats import ask_pitcher
from viewStatsClient.ask_team_stats import ask_team
from viewStatsClient.ask_umpire_queries import ask_umpire
from viewStatsClient.ask_venue_queries import ask_venue


def main():
    try:
        mydb, cursor = get_cursor()
    except ProgrammingError:
        print('Invalid credentials! Please fix and try again')
        return
    except DatabaseError:
        print('Connection timed out. IP address may be incorrect. Please fix and try again')
        return

    stats_dict = {
        1: ask_batter,
        2: ask_game,
        3: ask_pitcher,
        4: ask_umpire,
        5: ask_venue,
        6: ask_team,
        7: lambda var1, var2: None
    }

    stats_print_dict = {
        1: ". View Batter stats",
        2: ". View Game stats",
        3: ". View Pitcher stats",
        4: ". View Umpire stats",
        5: ". View Venue stats",
        6: ". View Team stats",
        7: ". Back"
    }

    while True:
        print('What would you like to do?')
        print('1. View Stats')
        print('2. Add Data')
        print('3. Exit')
        option = input('Enter your choice: ')
        try:
            option = int(option)
        except ValueError:
            print('Error: You must enter an integer between 1 and 3')
            continue

        if option < 1 or option > 3:
            print('Invalid option, please choose 1, 2, or 3')
            continue

        if option == 1:
            print('What Stats would you like to view')
            for x in stats_print_dict:
                print(str(x) + stats_print_dict[x])

            while True:
                option = input('Enter your choice: ')
                try:
                    option = int(option)
                except ValueError:
                    print('Error: You must enter an integer between 1 and 7')
                    continue

                if option not in stats_dict.keys():
                    print('Error: You must enter an integer between 1 and 7')
                    continue

                print("\033c", end="")
                stats_dict[option](mydb, cursor)
                break

        elif option == 2:
            add_user_data(mydb, cursor)
            continue

        elif option == 3:
            return


if __name__ == '__main__':
    main()
