from __future__ import print_function
from flask import Flask, render_template, request, make_response
import game
import sys
import player

app = Flask(__name__)

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

    if game_state_cookie:
        pass

    resp = make_response(render_template('game.html', game=tic_tac_toe_game))
    #c = ",".join(map(str, ttt.board))
    #resp.set_cookie("game_board", c)
    return resp

if __name__ == "__main__":
    app.run(debug=True)

