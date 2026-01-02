from game import *
import keyboard

class ExitedException(Exception):
    pass

class ValidationException(Exception):
    def __init__(self):
        super().__init__('Invalid set of coordinates! Please try again.')

class UI:
    def __init__(self):
        self.__human = None
        self.__computer = None

    def print_menu(self):
        print("Welcome to Bogdan's Crazy Planes Game!")
        print("|-----------# CONTROLS # -----------|")
        print("| Up/W - Move plane upwards         |")
        print("| Down/S - Move plane downwards     |")
        print("| Left/A - Move plane to the left   |")
        print("| Right/D - Move plane to the right |")
        print("| R - Rotate plane                  |")
        print("| Enter - Place plane               |")
        print("| Q - Undo plane placement          |")
        print("| Esc - Exit game                   |")
        print("|-----------------------------------|")
        print("Press anything to start.")

    def start(self):
        self.print_menu()

        key = keyboard.read_event()
        while key.event_type != 'down':
            key = keyboard.read_event()
        if key.name == 'enter':
            ignore_input = input()

        try:
            while True:
                self.__human = Human()
                self.__computer = Computer()
                print('Time to place your planes!')
                self.place_planes()
                self.__computer.generate_planes()
                self.game_loop()

                print("Press anything to start.")
                key = keyboard.read_event()
                while key.event_type != 'down':
                    key = keyboard.read_event()
        except ExitedException:
            print('Goodbye, hope you had fun! :D')
    
    def game_loop(self):
        human_turn = True
        message = ''
        try:
            while True:
                if human_turn:
                    self.display_boards()
                    if message != '':
                        print(message)
                    print('Time to attack!')
                    x, y = 0, 0
                    valid_input = False
                    while not valid_input:
                        try:
                            coordinates = input('Choose the position of the attack (e.g. D6): ')
                            x, y = self.validate_coordinates(coordinates)
                            message = self.__computer.hit(x, y)
                            self.display_boards()
                            print(message)
                            ignore_input = input('Press enter to continue...')
                            valid_input = True
                        except ValidationException as e:
                            print(e)
                        except AlreadyHitException as e:
                            print(e)

                else:
                    message = self.__human.hit()
                human_turn = not human_turn

        except LossException:
            self.display_boards()
            print('The computer has bested you, you lose!')

        except WinException:
            self.display_boards()
            print('Congratulations! You win!')


    def place_planes(self):
        i = 0
        while i < 3:
            i += 1
            orientation = 'up'
            x = 1
            y = 3
            self.__human.place_plane(orientation, x, y, False)

            placed = False
            while not placed:
                self.__human.preview()
                old_x = x
                old_y = y
                old_orientation = orientation
                action = False
                while not action:
                    key = keyboard.read_event()
                    if key.event_type != 'down':
                        continue

                    try:
                        if key.name == 'w' or key.name == 'up':
                            x -= 1
                            self.__human.place_plane(old_orientation, old_x, old_y, True)
                            self.__human.place_plane(orientation, x, y, False)
                            action = True
                        elif key.name == 's' or key.name == 'down':
                            x += 1
                            self.__human.place_plane(old_orientation, old_x, old_y, True)
                            self.__human.place_plane(orientation, x, y, False)
                            action = True
                        elif key.name == 'd' or key.name == 'right':
                            y += 1
                            self.__human.place_plane(old_orientation, old_x, old_y, True)
                            self.__human.place_plane(orientation, x, y, False)
                            action = True
                        elif key.name == 'a' or key.name == 'left'\
                                :
                            y -= 1
                            self.__human.place_plane(old_orientation, old_x, old_y, True)
                            self.__human.place_plane(orientation, x, y, False)
                            action = True
                        elif key.name == 'r':
                            match orientation:
                                case 'up':
                                    orientation = 'right'
                                case 'right':
                                    orientation = 'down'
                                case 'down':
                                    orientation = 'left'
                                case 'left':
                                    orientation = 'up'
                            self.__human.place_plane(old_orientation, old_x, old_y, True)
                            self.__human.place_plane(orientation, x, y, False)
                            action = True
                        elif key.name == 'enter':
                            ignore_input = input()
                            self.__human.verify_placement()
                            placed = True
                            action = True
                        elif key.name == 'q':
                            if i > 1:
                                i -= 2
                                self.__human.place_plane(orientation, x, y, True)
                                head = self.__human.get_last_head()
                                self.__human.place_plane(head[2], head[0], head[1], True)
                                placed = True
                            action = True
                        elif key.name == 'esc':
                            raise ExitedException

                    except OutOfBoundsException as e:
                        print(e)
                        x = old_x
                        y = old_y
                        orientation = old_orientation
                        self.__human.place_plane(orientation, x, y, False)
                        action = True

                    except InvalidPlacementException as e:
                        print(e)
                        action = True

    @staticmethod
    def validate_coordinates(coordinates: str):
        if len(coordinates) > 3 or len(coordinates) == 0:
            raise ValidationException

        coordinates = coordinates.strip()
        coordinates = coordinates.lstrip()
        coordinates = coordinates.lower()

        letters = 'abcdefghij'
        if coordinates[0] not in letters:
            raise ValidationException
        x = ord(coordinates[0]) - ord('a') + 1

        coordinates = coordinates[1:]
        try:
            coordinates = int(coordinates)
        except ValueError:
            raise ValidationException

        if coordinates not in range(1, 11):
            raise ValidationException
        y = int(coordinates)

        return x, y

    def display_boards(self):

        human_board = self.__human.visual_table()
        computer_board = self.__computer.visual_table()
        displayed_board = human_board + computer_board
        print(displayed_board)