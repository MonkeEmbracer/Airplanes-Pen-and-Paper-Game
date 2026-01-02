from ui import *
import unittest

class TestsBoard(unittest.TestCase):
    def test_place_plane(self):
        board = Board()
        with self.assertRaises(OutOfBoundsException):
            board.place_plane('up', 1, 11, False)
        board.place_plane('up', 3, 3, False)
        cells = 0
        for i in range(1, len(board)):
            for j in range(1, len(board)):
                if board._board[i][j] != 0:
                    cells += 1
        self.assertEqual(cells, 10)
        board.place_plane('up', 3, 3, True)
        cells = 0
        for i in range(1, len(board)):
            for j in range(1, len(board)):
                if board._board[i][j] != 0:
                    cells += 1
        self.assertEqual(cells, 0)

    def test_verify_placement(self):
        board = Board()
        board.place_plane('up', 3, 3, False)
        board.verify_placement()
        board.place_plane('up', 3, 3, False)
        with self.assertRaises(InvalidPlacementException):
            board.verify_placement()
        board.place_plane('up', 3, 3, True)
        board.verify_placement()
        board.place_plane('left', 10, 10, False)
        with self.assertRaises(InvalidPlacementException):
            board.verify_placement()

    def test_propagate_hit(self):
        board = Board()
        board.place_plane('up', 3, 3, False)
        board.place_plane('right', 8, 10, False)
        board.propagate_hit([3, 3, 'up'])
        cells = 0
        for i in range(1, len(board)):
            for j in range(1, len(board)):
                if board._board[i][j] == -10:
                    cells += 1
        self.assertEqual(cells, 9)

        cells = 0
        for i in range(1, len(board)):
            for j in range(1, len(board)):
                if board._board[i][j] > 0:
                    cells += 1
        self.assertEqual(cells, 10)


class TestsComputer(unittest.TestCase):
    def test_generate_planes(self):
        for _ in range(10):
            computer = Computer()
            computer.generate_planes()
            cells = 0
            for i in range(1, len(computer._board)):
                for j in range(1, len(computer._board)):
                    if computer._board.board[i][j] != 0:
                        cells += 1
            self.assertEqual(cells, 30)

    def test_hit(self):
        board = ComputerBoard()
        board.place_plane('up', 3, 3, False)
        board.hit(1, 1)
        board.hit(5, 3)
        cells = 0
        for i in range(1, len(board)):
            for j in range(1, len(board)):
                if board._board[i][j] == 9:
                    cells += 1
        self.assertEqual(cells, 8)
        board.place_plane('down', 9, 8, False)
        board.hit(3, 3)
        cells = 0
        for i in range(1, len(board)):
            for j in range(1, len(board)):
                if board._board[i][j] == 9:
                    cells += 1
        self.assertEqual(cells, 9)

        with self.assertRaises(AlreadyHitException):
            board.hit(3, 3)
        with self.assertRaises(WinException):
            board.hit(9, 8)



class TestsPlayer(unittest.TestCase):
    def test_hit(self):
        board = PlayerBoard()
        board.place_plane('up', 3, 3, False)
        board.hit(1, 1)
        board.hit(4, 3)
        cells = 0
        for i in range(1, len(board)):
            for j in range(1, len(board)):
                if board._board[i][j] == 9:
                    cells += 1
        self.assertEqual(cells, 8)
        board.place_plane('down', 10, 8, False)
        board.hit(3, 3)
        cells = 0
        for i in range(1, len(board)):
            for j in range(1, len(board)):
                if board._board[i][j] == 9:
                    cells += 1
        self.assertEqual(cells, 9)

        with self.assertRaises(LossException):
            board.hit(10, 8)