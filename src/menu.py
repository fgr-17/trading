class Menu:

    menu_options = {
        1: 'Start session',
        2: 'End Session',
        3: 'Get data from ticker',
        4: 'Exit',
    }

    @classmethod
    def print(cls):
        for key in cls.menu_options.keys():
            print (key, '--', cls.menu_options[key] )

    @classmethod
    def option1(cls):
        print('Handle option \'Option 1\'')

    @classmethod
    def option2(cls):
        print('Handle option \'Option 2\'')

    @classmethod
    def option3(cls):
        print('Handle option \'Option 3\'')

    @classmethod
    def loop(cls):
        while(True):
            cls.print()
            option = ''
            try:
                option = int(input('Enter your choice: '))
            except:
                print('Wrong input. Please enter a number ...')
            #Check what choice was entered and act accordingly
            if option == 1:
                cls.option1()
            elif option == 2:
                cls.option2()
            elif option == 3:
                cls.option3()
            elif option == 4:
                print('Exiting...')
                exit()
            else:
                print('Invalid option. Please enter a number between 1 and 4.')