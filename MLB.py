def main():
    print('What would you like to do?')
    print('1. View Stats')
    print('2. Add Data')

    while True:
        option = input('Enter your choice: ')

        try:
            option = int(option)
        except ValueError:
            print('Error: You must enter an integer between 1 and 2')
            continue

        if option < 1 or option > 2:
            print('Invalid option, please choose 1 or 2')
            continue

        break


if __name__ == '__main__':
    main()
