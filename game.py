import board
import subject


class Game(subject.Subject):
    def __init__(self, player_x_turn: bool, player_x, player_y):
        super().__init__()

        player_x.attach_game(self)
        player_y.attach_game(self)

        # Initialize the board
        self.game_board = board.GameBoard(3)

        # Initialize the game state
        self.player_x_turn = player_x_turn
        self.player_x_wins = False
        self.player_y_wins = False
        self.game_over = False
        self.previous_move_successful = True

        # Initialize the players
        self.player_x = player_x
        self.player_y = player_y

    def set_board(self, moves: list):
        for row_num in range(0, self.game_board.board_size):
            for col_num in range(0, self.game_board.board_size):
                self.game_board.board[row_num][col_num] = moves[self.game_board.board_size * row_num + col_num]

    # Code to make a single move, given the move_location
    def make_move(self, move_location):
        if self.player_x_turn:
            val = board.TTTValue.X
        else:
            val = board.TTTValue.O

        self.game_board.make_move(move_location, val)

