import random

class AI:
    def __init__(self):
        self.__map = [[0 for _ in range(11)]]
        self.load_file()

    def print_map(self):
        for row in self.__map:
            print(row)

    def load_file(self):
        file = open('heatmap.txt', 'rt')
        lines = file.readlines()
        self.__map = [[0 for _ in range(11)]]
        for line in lines:
            values = line.split(' ')
            row = [0]
            for value in values:
                row.append(int(value))
            self.__map.append(row)
        file.close()

    def __len__(self):
        return len(self.__map)

    def valid_coordinates(self, x, y):
        if x not in range(1, len(self.__map)) and y not in range(1, len(self.__map)):
            return False
        return True

    def hit_body(self, x, y):
        if not self.valid_coordinates(x, y): return
        self.__map[x][y] = -10000
        neighbors = [[x+1, y], [x-1, y], [x, y+1], [x, y-1]]
        for neighbor in neighbors:
            x = neighbor[0]; y = neighbor[1]
            if self.valid_coordinates(x, y):
                self.__map[x][y] += 500

    def hit_head(self, board):
        self.load_file()
        for i in range(1, len(self)):
            for j in range(1, len(self)):
                if board[i][j] == -9:
                    self.hit_body(i, j)
                if board[i][j] == 1 or board[i][j] == -10 or -8 <= board[i][j] <= -5:
                    self.miss(i, j)

    def miss(self, x, y):
        if not self.valid_coordinates(x, y): return
        self.__map[x][y] = -10000

    def best_guess(self):
        coordinates = []
        maximum = -1
        for i in range(1, len(self)):
            for j in range(1, len(self)):
                if self.__map[i][j] > maximum:
                    maximum = self.__map[i][j]
                    coordinates = [[i, j]]
                elif self.__map[i][j] == maximum:
                    coordinates.append([i, j])
        result = random.choice(coordinates)
        x = result[0]; y = result[1]
        return x, y