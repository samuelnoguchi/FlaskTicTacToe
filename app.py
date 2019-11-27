from __future__ import print_function
from flask import Flask, render_template, request, make_response
import game
import board
import sys
import player
import json
import math

app = Flask(__name__)

# Return the String representation of that location
def game_to_json(g: game.Game):
    game_dict = dict()
    if(g.player_x_turn):
        game_dict['player_x_turn'] = 'True'
    else: 
        game_dict['player_x_turn'] = 'False'
    
    game_dict['board_size'] = str(g.game_board.board_size)

    board_state = ''

    # Get the state of the board (X's and O's)
    for row_num in range(0, g.game_board.board_size):
        for col_num in range(0, g.game_board.board_size):
            board_state += str(g.game_board.value_at(row_num, col_num)) + " "

    game_dict['board_state'] = board_state

    return json.dumps(game_dict)


def json_to_game(j, g: game.Game):
    board_state = j['board_state']

    moves = list()

    for cell in board_state:
        if cell == '_':
            moves.append(board.TTTValue.EMPTY)
        if cell == 'X':
            moves.append(board.TTTValue.X)
        if cell == 'Y':
            moves.append(board.TTTValue.O)

    g.set_board(moves)


# Choose number of players
@app.route('/')
def index():
    return render_template('index.html')


# For now, player 1 always X
@app.route('/game/<num_players>', methods=['GET', 'POST'])
def play_game(num_players):
    # Create the players
    player_1 = player.RealPlayer()

    if(num_players == '1-player'):
        player_2 = player.RealPlayer()
    else:
        player_2 = player.CPUPlayer()

    # Create the game
    tic_tac_toe_game = game.Game(True, player_1, player_2)
    game_state_cookie = request.cookies.get('game_state')

    # Initialize the board from last move
    if game_state_cookie:
        game_state_json = json.loads(game_state_cookie)
        # Set up the game based on previous game state
        json_to_game(game_state_json, tic_tac_toe_game)


    if "choice" in request.form:
        x = int(request.form["choice"]) % 3    
        y = math.floor(int(request.form["choice"]) / 3)
        tic_tac_toe_game.make_move([x, y])

    resp = make_response(render_template('game.html', game=tic_tac_toe_game))

    # Store the game state
    resp.set_cookie("game_state", game_to_json(tic_tac_toe_game))
    return resp

# Restart game
@app.route('/start-over')
def start_over():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

