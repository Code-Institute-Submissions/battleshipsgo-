import random
from flask import Flask, request, jsonify

app = Flask(__name__)
app.static_folder = 'static'

# Initialize game board
board_size = 5
player_board = [[0 for x in range(board_size)] for y in range(board_size)]
computer_board = [[0 for x in range(board_size)] for y in range(board_size)]

# Initialize ships
player_ships = []
computer_ships = []
ship_sizes = [2, 3, 3, 4, 5]

# Generate computer's ships
for size in ship_sizes:
    while True:
        orientation = random.randint(0, 1)  # 0 for horizontal, 1 for vertical
        if orientation == 0:
            x = random.randint(0, board_size - size)
            y = random.randint(0, board_size - 1)
            positions = [(x+i, y) for i in range(size)]
        else:
            x = random.randint(0, board_size - 1)
            y = random.randint(0, board_size - size)
            positions = [(x, y+i) for i in range(size)]
        if all(position[0] < board_size and position[1] < board_size and
               computer_board[position[1]][position[0]] == 0 for position in positions):
            for position in positions:
                computer_board[position[1]][position[0]] = 1
            computer_ships.append(positions)
            break

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/place_ship', methods=['POST'])
def place_ship():
    global player_ships
    positions = request.json
    if len(positions) != 2:
        return 'Invalid ship size', 400
    x1, y1 = positions[0]
    x2, y2 = positions[1]
    if x1 != x2 and y1 != y2:
        return 'Invalid ship orientation', 400
    size = max(abs(x1 - x2), abs(y1 - y2)) + 1
    if size not in ship_sizes:
        return 'Invalid ship size', 400
    if x1 != x2:
        positions = [(x, y1) for x in range(min(x1, x2), max(x1, x2)+1)]
    else:
        positions = [(x1, y) for y in range(min(y1, y2), max(y1, y2)+1)]
    if any(player_board[y][x] == 1 for x, y in positions):
        return 'Cannot overlap with other ships', 400
    player_ships.append(positions)
    for x, y in positions:
        player_board[y][x] = 1
    return 'OK'

@app.route('/shoot', methods=['POST'])
def shoot():
    global computer_ships
    x, y = request.json
    if computer_board[y][x] == 1:
        computer_board[y][x] = 2
        for ship in computer_ships:
            if (x, y) in ship:
                ship.remove((x, y))
                if not ship:
                    computer_ships.remove(ship)
                    return jsonify({'status': 'hit', 'sunk': True})
                else:
                    return jsonify({'status': 'hit', 'sunk': False})
    else:
        computer_board[y][x] = 3
        return jsonify({'status': 'miss'})

    # Computer's turn
   
    while True:
        x = random.randint(0, board_size - 1)
        y = random.randint(0, board_size - 1)
        if player_board[y][x] == 0:
            break
    if (x, y) in player_ships:
        player_ships.remove((x, y))
        if not player_ships:
            return jsonify({'status': 'game_over', 'winner': 'computer'})
        else:
            return jsonify({'status': 'hit', 'sunk': False})
    else:
        return jsonify({'status': 'miss'})

if __name__ == '__main__':
    app.run()

