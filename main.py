import board
import player
import game
import observer


player_x = player.RealPlayer()
player_y = player.CPUPlayer()

game = game.Game(True, player_x, player_y)

obs = observer.TextObserver(game)

game.play()


