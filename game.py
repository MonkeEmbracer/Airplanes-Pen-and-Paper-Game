from players import *
import random


class Player:
    def __init__(self):
        self._board = PlayerBoard()

    def place_plane(self, orientation, x, y, removed):
        self._board.place_plane(orientation, x, y, removed)

    def preview(self):
        self._board.preview()

    def verify_placement(self):
        self._board.verify_placement()

    def get_last_head(self):
        return self._board.get_last_head()

    def visual_table(self):
        return self._board.visual_table()

class Human(Player):
    def hit(self):
        #self._board.generate_positions()
        #positions = self._board.hittable_positions()
        #coordinates = random.choice(positions)

        coordinates = self._board.best_guess()
        x = coordinates[0]; y = coordinates[1]
        return self._board.hit(x, y)

class Computer(Player):
    def __init__(self):
        super().__init__()
        self._board = ComputerBoard()

    def generate_planes(self):
        """
        Randomly places 3 planes on an empty board.
        :return: None
        """
        orientations = ['up', 'down', 'left', 'right']
        i = 0
        while i < 3:
            orientation = random.choice(orientations)
            positions = self._board.generate_positions()
            valid = False
            while not valid:
                coordinates = random.choice(positions)
                x = coordinates[0]; y = coordinates[1]
                positions.remove(coordinates)
                self._board.place_plane(orientation, x, y, False)
                self._board.preview()
                try:
                    self._board.verify_placement()
                    i += 1
                    self._board.preview()
                    valid = True
                except InvalidPlacementException:
                    self._board.place_plane(orientation, x, y, True)

    def hit(self, x, y):
        return self._board.hit(x, y)