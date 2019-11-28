from enum import Enum


# Enum class representing the different states a tic tac toe location can be in
class TTTValue(Enum):
    EMPTY = 0
    X = 1
    O = 2


class GameBoard:
    def __init__(self, board_size):
        self.board = list()
        self.board_size = board_size

        # Initialize the board empty
        for num in range(self.board_size):
            self.board.append([TTTValue.EMPTY] * self.board_size)

    # Determine whether a given moveLocation (x,y) is valid (empty) return true if valid, false otherwise
    def valid_move(self, move_location, value: TTTValue) -> bool:
        if move_location[0] < self.board_size and move_location[1] < self.board_size and \
                (value == TTTValue.X or value == TTTValue.O):
            return True
        else:
            return False

    # Make a move at moveLocation (x,y) returns true if the move was successful, otherwise returns false
    def make_move(self, move_location, value: TTTValue) -> bool:
        # Check for bounds of move
        if not self.valid_move(move_location, value):
            return False

        # Check location is empty
        if self.board[move_location[1]][move_location[0]] != TTTValue.EMPTY:
            return False

        # Make the move
        self.board[move_location[1]][move_location[0]] = value

        return True

    # Return the list of available moves [(x,y), (x,y), ...]
    def available_moves(self):
        moves = list()

        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.board[y][x] == TTTValue.EMPTY:
                    moves.append([x, y])

        return moves

    # Return true if a row is filled with val
    def homogeneous_row(self, row_num, val: TTTValue):
        for i in range(self.board_size):
            if self.board[row_num][i] != val:
                return False

        return True

    # Return true if a col is filled with val
    def homogeneous_col(self, col_num, val: TTTValue):
        for i in range(self.board_size):
            if self.board[i][col_num] != val:
                return False

        return True

    # Return true if the game is won
    def is_won(self):
        # Keep track of the diagonal
        diagonal_homogeneous = True

        for i in range(self.board_size):
            if self.board[i][i] != TTTValue.EMPTY:
                # Check the row and column for a win
                if self.homogeneous_row(i, self.board[i][i]) or self.homogeneous_col(i, self.board[i][i]):
                    return True

            # Check the diagonal
            if diagonal_homogeneous and i != 0:
                if self.board[i][i] == TTTValue.EMPTY or (self.board[i][i] != TTTValue.EMPTY and self.board[i][i]
                                                          != self.board[i-1][i-1]):
                    diagonal_homogeneous = False

        # If the first diagonal is homogeneous return true
        if diagonal_homogeneous:
            return True

        # Check other diagonal
        for i in range(self.board_size):
            if self.board[i][self.board_size-1-i] == TTTValue.EMPTY:
                return False
            if i != 0:
                if self.board[i][self.board_size-1-i] != self.board[i-1][self.board_size-i]:
                    return False

        return True

    # Get the string representation of the value at position (row, col)
    def value_at(self, row, col):
        if self.board[row][col] == TTTValue.EMPTY:
            return '_'
        elif self.board[row][col] == TTTValue.X:
            return 'X'    
        else:
            return 'O'