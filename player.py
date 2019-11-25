import board
import copy


class Player:
    def __init__(self):
        self.game = None

    # Virtual method which will be overridden
    def get_move(self):
        pass

    # Attach the game
    def attach_game(self, g):
        self.game = g


class RealPlayer(Player):
    # Get the players move, returning [x, y]
    def get_move(self) -> list:
        x_input_invalid = True

        while x_input_invalid:
            x = input("Enter x coordinate: ")
            if len(x) > 0 and x.isdigit():
                x_input_invalid = False

        y_input_invalid = True

        while y_input_invalid:
            y = input("Enter y coordinate: ")
            if len(y) > 0 and y.isdigit():
                y_input_invalid = False

        return [int(x), int(y)]


class CPUPlayer(Player):
    # Compute the best move, returning [x, y]
    def get_move(self) -> list:
        # Get the available moves
        moves = self.game.game_board.available_moves()

        # Determine whose turn it currently is
        player_x_turn = self.game.player_x_turn

        # Determine the value of the next move
        if player_x_turn:
            val = board.TTTValue.X
        else:
            val = board.TTTValue.O

        # Find the score of the moves using minimax algorithm
        scores = list()

        for move in moves:
            trial_board: board.GameBoard = copy.deepcopy(self.game.game_board)
            trial_board.make_move(move, val)
            scores.append(self.minimax(trial_board, True, player_x_turn))

        # Get the index of the max score
        max_index = scores.index(max(scores))
        return moves[max_index]

    # Compute minimax score of multiple move options
    def minimax(self, game_board: board.GameBoard, cpu_turn: bool, player_x_turn: bool) -> int:
        # If the game is over return the score
        s = self.score(game_board, cpu_turn)
        if s != 0:
            return s

        # Create the list of scores of all further possible moves
        scores = list()
        moves = game_board.available_moves()

        # Check for no available moves left, in which case tie
        if len(moves) == 0:
            return 0

        # Parity the turn
        player_x_turn = not player_x_turn

        # Get the score of each possible move
        for move in moves:
            trial_board: board.GameBoard = copy.deepcopy(game_board)

            # Determine the value of the play
            if player_x_turn:
                val = board.TTTValue.X
            else:
                val = board.TTTValue.O

            trial_board.make_move(move, val)

            # Find the minimax score of this new move
            scores.append(self.minimax(trial_board, not cpu_turn, player_x_turn))

        # Do the minimax calculation
        if not cpu_turn:
            return max(scores)
        else:
            return min(scores)

    # Calculate the score of a board given whether the previous move was done by the cpu_player
    def score(self, game_board: board.GameBoard, cpu_turn: bool) -> int:
        if game_board.is_won():
            if cpu_turn:
                return 10
            else:
                return -10
        return 0
