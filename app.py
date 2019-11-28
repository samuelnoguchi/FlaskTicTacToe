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
        if cell == 'O':
            moves.append(board.TTTValue.O)

    g.set_board(moves)

    # Set the correct player to whoever just moved
    if j['player_x_turn'] == 'False':
        g.player_x_turn = False


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
        player_2 = player.CPUPlayer()
    else:
        player_2 = player.RealPlayer()

    # Create the game
    tic_tac_toe_game = game.Game(True, player_1, player_2)
    game_state_cookie = request.cookies.get('game_state')

    # Initialize the board from last move
    if game_state_cookie:
        game_state_json = json.loads(game_state_cookie)
        # Set up the game based on previous game state
        json_to_game(game_state_json, tic_tac_toe_game)

      
    # Get the new move
    if "choice" in request.form:
        x = int(request.form["choice"]) % 3    
        y = math.floor(int(request.form["choice"]) / 3)
        tic_tac_toe_game.make_move([x, y])

        # Check for game win
        if tic_tac_toe_game.game_board.is_won():
            tic_tac_toe_game.game_over = True

            if tic_tac_toe_game.player_x_turn:
                tic_tac_toe_game.player_x_wins = True
            else:
                tic_tac_toe_game.player_y_wins = True
        # Check for board full (tie)
        elif len(tic_tac_toe_game.game_board.available_moves()) == 0:
            tic_tac_toe_game.game_over = True
        else:
            # parity the turn
            tic_tac_toe_game.player_x_turn = not tic_tac_toe_game.player_x_turn

            # Make computer move in 1 player mode
            if(num_players == '1-player'):
                move_location = tic_tac_toe_game.player_y.get_move()
                tic_tac_toe_game.make_move(move_location)

                # parity the turn
                tic_tac_toe_game.player_x_turn = not tic_tac_toe_game.player_x_turn
                
                # check for CPU win
                if tic_tac_toe_game.game_board.is_won():
                    tic_tac_toe_game.game_over = True
                    tic_tac_toe_game.player_y_wins = True

                # Check for tie
                elif len(tic_tac_toe_game.game_board.available_moves()) == 0:
                    tic_tac_toe_game.game_over = True

    # Determine the message to display on screen
    if tic_tac_toe_game.game_over:
        if tic_tac_toe_game.player_x_wins and num_players == '2-player':
            message = "Player 1 wins!"
        elif tic_tac_toe_game.player_y_wins and num_players == '2-player':
            message = "Player 2 wins!"
        elif tic_tac_toe_game.player_x_wins and num_players == '1-player':
            message = "You won??"
        elif tic_tac_toe_game.player_y_wins and num_players == '1-player':
            message = "You lost to the computer..."
        else:
            message = "It's a Tie!"
    else:
        if tic_tac_toe_game.player_x_turn and num_players == '1-player':
            message = "Your Turn (X)"
        elif tic_tac_toe_game.player_x_turn and num_players == '2-player':
            message = "Player 1's Turn (X)"
        elif not tic_tac_toe_game.player_x_turn and num_players == '2-player':
            message = "Player 2's Turn (O)"

    resp = make_response(render_template('game.html', game=tic_tac_toe_game, message=message))
    # Store the game state
    resp.set_cookie("game_state", game_to_json(tic_tac_toe_game))
    return resp

# Restart game
@app.route('/start-over')
def start_over():
    resp = make_response(render_template('index.html'))
    # Reset the game state
    resp.set_cookie('game_state', '', expires=0)
    return resp


if __name__ == "__main__":
    app.run(debug=True)

