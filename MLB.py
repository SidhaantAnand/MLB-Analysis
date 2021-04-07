from add_data import add_user_data 
from create_connection import get_cursor

def main():
    mydb, cursor = get_cursor()

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
        
        if option == 2:
            add_user_data(mydb, cursor)
            continue

        break


if __name__ == '__main__':
    main()
