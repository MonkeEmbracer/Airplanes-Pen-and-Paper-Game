from board import *
from ai import AI
import random

class PlayerBoard(Board):
    def __init__(self):
        super().__init__()
        self.__ai = AI()

    def visual_table(self):
        table = Bogtable(11)
        table.add_row(self._board[0])
        color_table = self.color_table()
        for i in range(1, len(self._board)):
            row = []
            for j in range(len(self._board[i])):
                element = self._board[i][j]
                match element:
                    case 0:
                        element = ' '
                    case 1:
                        element = color('*', 'bright yellow')
                    case 5:
                        element = color('^', color_table[i][j])
                    case 6:
                        element = color('V', color_table[i][j])
                    case 7:
                        element = color('<', color_table[i][j])
                    case 8:
                        element = color('>', color_table[i][j])
                    case 9:
                        element = color('O', color_table[i][j])
                    case -5:
                        element = color('^', 'red')
                    case -6:
                        element = color('V', 'red')
                    case -7:
                        element = color('<', 'red')
                    case -8:
                        element = color('>', 'red')
                    case _:
                        if type(element) == int:
                            if element < 0:
                                element = color('X', 'red')
                            else:
                                element = color('#', 'red')
                row.append(element)
            table.add_row(row)
        return table

    def hit(self, x, y):
        """
        Simulates a hit on the human player's table.
        In case of a miss, the cell's value is set to 1.
        In case of a body hit, the cell's value is set to -9.
        In case of a head hit, the cell's value is set to its opposite, and function propagate_hit is called to destroy the plane.
        Also updates the computer's 'AI' based on the outcome.
        Assumes that the cell has not already been hit.
        Raises a LossException if the human's last plane is destroyed.
        :param x: the x coordinate of the hit
        :param y: the y coordinate of the hit
        :return: a message to be displayed to the player regarding the outcome
        """
        message = ''
        match self._board[x][y]:
            case 0:
                message = f'Your enemy {color('missed', 'green')}! Hell yeah!'
                self._board[x][y] = 1
                self.__ai.miss(x, y)

            case 5 | 6 | 7 | 8:
                message = f'Oh... They {color('destroyed', 'red')} your '
                match len(self._heads):
                    case 3:
                        message += 'first plane'
                    case 2:
                        message += 'second plane'
                    case 1:
                        message += 'third plane'
                    case _:
                        message += 'plane'
                message += '!'

                head = None
                for element in self._heads:
                    if x == element[0] and y == element[1]:
                        self._heads.remove(element)
                        head = element
                self.propagate_hit(head)
                self.__ai.hit_head(self._board)
                if len(self._heads) == 0:
                    raise LossException

            case 9:
                message = f'They {color('hit', 'red')} one of your planes! Unfortunate...'
                self.flip(x, y)
                self.__ai.hit_body(x, y)

            case _:
                message = 'Miss!'
        return message

    def best_guess(self):
        #self.__ai.print_map()
        return self.__ai.best_guess()


class ComputerBoard(Board):
    def visual_table(self):
        table = Bogtable(11)
        table.add_row(self._board[0])
        for i in range(1, len(self._board)):
            row = []
            for j in range(len(self._board[i])):
                element = self._board[i][j]
                match element:
                    case 0:
                        element = ' '
                    case 1:
                        element = color('*', 'bright yellow')
                    case _:
                        if type(element) == int:
                            if element <= -9:
                                element = color('X', 'red')
                            elif element >= 10:
                                element = color('#', 'red')
                            elif element == -5:
                                element = color('^', 'red')
                            elif element == -6:
                                element = color('V', 'red')
                            elif element == -7:
                                element = color('<', 'red')
                            elif element == -8:
                                element = color('>', 'red')
                            else:
                                element = ' '
                row.append(element)
            table.add_row(row)
        return table

    def hit(self, x, y):
        """
        Simulates a hit on the computer's table.
        In case of a miss, the cell's value is set to 1.
        In case of a body hit, the cell's value is set to -9.
        In case of a head hit, the cell's value is set to its opposite, and function propagate_hit is called to destroy the plane.
        Raises an AlreadyHitException if the cell has already been hit.
        Raises a WinException if the computer's last plane is destroyed.
        :param x: the x coordinate of the hit
        :param y: the y coordinate of the hit
        :return: a message to be displayed to the player regarding the outcome
        """
        message = ''
        match self._board[x][y]:
            case 0:
                message = f'You {color('missed', 'red')}! Bad luck!'
                self._board[x][y] = 1

            case 5 | 6 | 7 | 8:
                message = color(random.choice(['Headshot! ', 'Bullseye! ', 'Boom! ']), 'yellow')
                match len(self._heads):
                    case 3:
                        message += 'First plane'
                    case 2:
                        message += 'Second plane'
                    case 1:
                        message += 'Third plane'
                    case _:
                        message += 'Plane'
                message += ' destroyed!'

                head = None
                for element in self._heads:
                    if x == element[0] and y == element[1]:
                        self._heads.remove(element)
                        head = element
                self.propagate_hit(head)
                if len(self._heads) == 0:
                    raise WinException

            case 9:
                message = f'You {color('hit', 'green')} a plane! Good job!'
                self.flip(x, y)

            case _:
                raise AlreadyHitException
        return message