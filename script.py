import random

class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.ships = []

    def place_ship(self, x, y):
        if len(self.ships) >= 5:
            return False
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return False
        if self.grid[y][x] != 0:
            return False
        self.grid[y][x] = 1
        self.ships.append((x, y))
        return True

    def check_shot(self, x, y):
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return 'off_grid'
        if self.grid[y][x] == 1:
            self.grid[y][x] = 2
            self.ships.remove((x, y))
            if not self.ships:
                return 'game_over'
            else:
                return 'hit'
        elif self.grid[y][x] == 0:
            self.grid[y][x] = -1
            return 'miss'
        else:
            return 'repeat'

class Game:
    def __init__(self, size):
        self.board_size = size
        self.player_board = Board(size)
        self.computer_board = Board(size)
        self.turn = 'player'

    def play(self, x, y):
        if self.turn == 'player':
            result = self.computer_board.check_shot(x, y)
            if result == 'off_grid':
                return 'off_grid'
            elif result == 'game_over':
                return 'player_wins'
            elif result == 'hit':
                return 'hit'
            elif result == 'miss':
                self.turn = 'computer'
                return 'miss'
            else:
                return 'repeat'
        else:
            result = self.player_board.check_shot(x, y)
            if result == 'off_grid':
                return 'off_grid'
            elif result == 'game_over':
                return 'computer_wins'
            elif result == 'hit':
                return 'hit'
            elif result == 'miss':
                self.turn = 'player'
                return 'miss'
            else:
                return 'repeat'

    def computer_play(self):
        while True:
            x = random.randint(0, self.board_size - 1)
            y = random.randint(0, self.board_size - 1)
            result = self.player_board.check_shot(x, y)
            if result == 'miss':
                self.turn = 'player'
                break



