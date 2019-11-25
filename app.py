from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game/<int:num_players>')
def playGame(num_players):
    return render_template('game.html')


if __name__ == "__main__":
    app.run(debug=True)
