from searchPython.umpire_queries import *


def ask_umpire(mydb, cursor):
    print("1. Number of games officiated")
    print("2. Ejections by umpire")
    print("3. Most common position")
    print("4. Most common venue")
    print("5. Best umpire")
    print("6. Worst umpire")

    while True:
        option = input('Enter your choice: ')
        try:
            option = int(option)
        except ValueError:
            print('Error: You must enter an integer between 1 and 6')
            continue
        if option < 1 or option > 6:
            print('Invalid option, please choose between 1 and 6')
            continue

        umpire_name = ""
        if option <= 4:
            umpire_name = input("Enter an umpire name: ")

        if option == 1:
            result = umpire_games(cursor, umpire_name)
            print(umpire_name + " has officiated " + str(result[0][0]) + " games")

        elif option == 2:
            result = umpire_ejections(cursor, umpire_name)
            print(umpire_name + " has issued " + str(result[0][0]) + " ejections, with " + str(result[0][1])
                  + " challenges and " + str(result[0][2]) + " correct challenges")

        elif option == 3:
            result = umpire_position(cursor, umpire_name)
            print(umpire_name + " most common position is at " + result[0][0])

        elif option == 4:
            result = umpire_venue(cursor, umpire_name)
            print(umpire_name + " most common venue is at " + result[0][0])

        elif option == 5:
            result = best_umpire(cursor)
            print("The best umpire in terms of ejections:challenges is " + result[0][0] + " with a ratio of " + str(result[0][1]))

        elif option == 6:
            result = worst_umpire(cursor)
            print("The worst umpire in terms of ejections:challenges is " + result[0][0] + " with a ratio of " + str(result[0][1]))

        break