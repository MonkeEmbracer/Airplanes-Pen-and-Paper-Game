from bogtable import Bogtable

class BoardException(Exception):
    def __init__(self, message):
        self.__message = message
        super().__init__(self.__message)

class OutOfBoundsException(BoardException):
    def __init__(self):
        super().__init__('Plane is out of bounds!')

class InvalidPlacementException(BoardException):
    pass

class AlreadyHitException(BoardException):
    def __init__(self):
        super().__init__('You already hit that cell! Please choose another one.')

class WinException(Exception):
    pass

class LossException(Exception):
    pass


class Board:
    """
    0 - empty
    5 - up head
    6 - down head
    7 - left head
    8 - right head
    9 - body
    10+ - intersection
    negative - hit
    1 - miss
    """
    def __init__(self):
        self._size = 10
        self._board = ([[' '] + [i + 1 for i in range(self._size)]] +
                       [([chr(65 + i)] + [0 for _ in range(self._size)]) for i in range(self._size)])
        self._heads = []

    @property
    def size(self):
        return self._size

    @property
    def board(self):
        return self._board

    def __len__(self):
        return len(self._board)

    def get_last_head(self):
        return self._heads[-1]

    def planes(self):
        return len(self._heads)

    def add(self, x, y, val):
        if x in range(1, self._size + 1) and y in range(1, self._size + 1):
            self._board[x][y] += val

    def set_color(self, table, x, y, val):
        if x in range(1, self._size + 1) and y in range(1, self._size + 1):
            table[x][y] = val

    def flip(self, x, y):
        if x in range(1, self._size + 1) and y in range(1, self._size + 1):
            self._board[x][y] = -self._board[x][y]

    def set(self, x, y, val):
        if x in range(1, self._size + 1) and y in range(1, self._size + 1):
            self._board[x][y] = val

    def place_plane(self, orientation: str, x: int, y: int, removed: bool):
        """
        Places or removes a plane from the board.
        Allows intersections, but marks them as cells with a value >= 10.
        Also allows the plane to be placed partially on the board.
        Raises an OutOfBoundsException if the plane's head is outside the board.
        :param orientation: the direction the plane is facing, string that can be 'up', 'down', 'left', 'right'
        :param x: the x coordinate of the head
        :param y: the y coordinate of the head
        :param removed: whether the plane is to be removed or placed
        :return: None
        """
        if x not in range(1, self._size + 1):
            raise OutOfBoundsException
        if y not in range(1, self._size + 1):
            raise OutOfBoundsException

        if removed:
            b = -9
            c = -1
            self._heads.pop()
        else:
            c = 1
            b = 9
            self._heads.append([x, y, orientation])
        match orientation:
            case 'up' | 'down':
                a = 1
                if orientation == 'down':
                    a = -1
                    self.add(x, y, 6*c)
                else:
                    self.add(x, y, 5*c)
                self.add(x + a, y, b)
                self.add(x + 2 * a, y, b)
                self.add(x + 3 * a, y, b)
                self.add(x + a, y + a, b)
                self.add(x + a, y + 2 * a, b)
                self.add(x + a, y - a, b)
                self.add(x + a, y - 2 * a, b)
                self.add(x + 3 * a, y + a, b)
                self.add(x + 3 * a, y - a, b)

            case 'left' | 'right':
                a = 1
                if orientation == 'right':
                    a = -1
                    self.add(x, y, 8*c)
                else:
                    self.add(x, y, 7*c)
                self.add(x, y + a, b)
                self.add(x + a, y + a, b)
                self.add(x + 2 * a, y + a, b)
                self.add(x - a, y + a, b)
                self.add(x - 2 * a, y + a, b)
                self.add(x, y + 2 * a, b)
                self.add(x, y + 3 * a, b)
                self.add(x + a, y + 3 * a, b)
                self.add(x - a, y + 3 * a, b)

    def preview(self):
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
                    case _:
                        if type(element) == int:
                            element = color('#', 'red')
                row.append(element)
            table.add_row(row)
        print(table)

    def color_table(self):
        table = [['' for _ in range(self._size + 1)] for _ in range(self._size + 1)]
        colors = ['blue', 'yellow', 'green']

        for i in range(len(self._heads)):
            head = self._heads[i]
            x = head[0]
            y = head[1]
            orientation = head[2]
            color = 'blue'
            if i in range(3):
                color = colors[i]

            match orientation:
                case 'up' | 'down':
                    a = 1
                    if orientation == 'down':
                        a = -1
                    self.set_color(table, x, y, color)
                    self.set_color(table, x + a, y, color)
                    self.set_color(table, x + 2 * a, y, color)
                    self.set_color(table, x + 3 * a, y, color)
                    self.set_color(table, x + a, y + a, color)
                    self.set_color(table, x + a, y + 2 * a, color)
                    self.set_color(table, x + a, y - a, color)
                    self.set_color(table, x + a, y - 2 * a, color)
                    self.set_color(table, x + 3 * a, y + a, color)
                    self.set_color(table, x + 3 * a, y - a, color)

                case 'left' | 'right':
                    a = 1
                    if orientation == 'right':
                        a = -1
                    self.set_color(table, x, y, color)
                    self.set_color(table, x, y + a, color)
                    self.set_color(table, x + a, y + a, color)
                    self.set_color(table, x + 2 * a, y + a, color)
                    self.set_color(table, x - a, y + a, color)
                    self.set_color(table, x - 2 * a, y + a, color)
                    self.set_color(table, x, y + 2 * a, color)
                    self.set_color(table, x, y + 3 * a, color)
                    self.set_color(table, x + a, y + 3 * a, color)
                    self.set_color(table, x - a, y + 3 * a, color)
        return table

    def verify_placement(self):
        """
        Checks that there are no intersections on the board and that there all planes are integrally inside the board.
        Raises an InvalidPlacementException if invalid.
        :return: None
        """
        count = 0
        for i in range(1, self._size + 1):
            for j in range(1, self._size + 1):
                element = self._board[i][j]
                if type(element) == int:
                    if 5 <= self._board[i][j] <= 9:
                        count += 1
                    elif 10 <= self._board[i][j]:
                        raise InvalidPlacementException('There must be no intersections between planes!')
        if count % 10 != 0:
            raise InvalidPlacementException('Planes must be integrally inside the table!')

    def generate_positions(self):
        positions = []
        for i in range(1, self._size + 1):
            for j in range(1, self._size + 1):
                if self._board[i][j] == 0:
                    positions.append([i, j])
        return positions

    def hittable_positions(self):
        positions = []
        for i in range(1, self._size + 1):
            for j in range(1, self._size + 1):
                if self._board[i][j] >= 0 and self._board[i][j] != 1:
                    positions.append([i, j])
        return positions

    def propagate_hit(self, head):
        """
        Effectively destroys an entire plane when given its head.
        Replaces the value in the head's cell with the opposite.
        Replaces the value in the plane's body cells with -10.
        :param head: list of format [x: int, y: int, orientation: str]
        :return: None
        """
        x = head[0]
        y = head[1]
        orientation = head[2]

        self.flip(x, y)
        match orientation:
            case 'up' | 'down':
                a = 1
                if orientation == 'down':
                    a = -1
                self.set(x + a, y, -10)
                self.set(x + 2 * a, y, -10)
                self.set(x + 3 * a, y, -10)
                self.set(x + a, y + a, -10)
                self.set(x + a, y + 2 * a, -10)
                self.set(x + a, y - a, -10)
                self.set(x + a, y - 2 * a, -10)
                self.set(x + 3 * a, y + a, -10)
                self.set(x + 3 * a, y - a, -10)

            case 'left' | 'right':
                a = 1
                if orientation == 'right':
                    a = -1
                self.set(x, y + a, -10)
                self.set(x + a, y + a, -10)
                self.set(x + 2 * a, y + a, -10)
                self.set(x - a, y + a, -10)
                self.set(x - 2 * a, y + a, -10)
                self.set(x, y + 2 * a, -10)
                self.set(x, y + 3 * a, -10)
                self.set(x + a, y + 3 * a, -10)
                self.set(x - a, y + 3 * a, -10)


def color(string, color):
    match color:
        case 'blue':
            return f'\033[36m{string}\033[0m'
        case 'red':
            return f'\033[31m{string}\033[0m'
        case 'yellow':
            return f'\033[33m{string}\033[0m'
        case 'green':
            return f'\033[32m{string}\033[0m'
        case 'bright yellow':
            return f'\033[93m{string}\033[0m'
    return string