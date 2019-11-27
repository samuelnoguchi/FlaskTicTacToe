from __future__ import print_function
from flask import Flask, render_template
import game
import player

app = Flask(__name__)

tic_tac_toe_game: game.Game
player_x: player.Player
player_y: player.Player


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game/<num_players>')
def startGame(num_players):
    if(num_players == '1-player'):
        player_x = player.RealPlayer()
        player_y = player.CPUPlayer()
        tic_tac_toe_game = game.Game(True, player_x, player_y)
        
    return render_template('game.html')



if __name__ == "__main__":
    app.run(debug=True)
 