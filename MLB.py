import sys


sys.path.insert(1, './viewStatsClient')

from ask_batter_stats import ask_batter
from ask_game_queries import ask_game
from ask_pitcher_stats import ask_pitcher
from ask_team_stats import ask_team
from ask_umpire_queries import ask_umpire
from ask_venue_queries import ask_venue
from add_data import add_user_data 
from create_connection import get_cursor

def main():
    mydb, cursor = get_cursor()

    stats_dict = {
        1 : ask_batter,
        2: ask_game,
        3: ask_pitcher,
        4: ask_umpire,
        5: ask_venue
    }

    stats_print_dict = {
        1 : ". View Batter stats",
        2: ". View Game stats",
        3: ". View Pitcher stats",
        4: ". View Umpire stats",
        5: ". View Venue stats"
    }

    while True:
        option = 0
        print('\n')
        print('What would you like to do?')
        print('1. View Stats')
        print('2. Add Data')
        option = input('Enter your choice: ')
        print('\n')
        try:
            option = int(option)
        except ValueError:
            print('Error: You must enter an integer between 1 and 2')
            continue

        if option < 1 or option > 2:
            print('Invalid option, please choose 1 or 2')
            continue
        
        if option == 1:
            print('What Stats would you like to view')
            for x in stats_print_dict:
                print(str(x) + " " + stats_print_dict[x])

            while(True):
                try:
                    option = int(option)
                except ValueError:
                    print('Error: You must enter an integer between 1 and 5')
                    continue
                if(not option in stats_dict):
                    print('Error: You must enter an integer between 1 and 5')
                    continue
                stats_dict[option](mydb,cursor)
                break
        if option == 2:
            add_user_data(mydb, cursor)
            continue

        break


if __name__ == '__main__':
    main()
