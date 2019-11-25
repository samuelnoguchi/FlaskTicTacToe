import board


class Observer:
    def notify(self):
        pass


class TextObserver(Observer):
    def __init__(self, g):
        self.game = g
        g.attach(self)

    def notify(self):
        print("-------------")
        for row in self.game.game_board.board:
            print("|", end='')
            for col in row:
                if col == board.TTTValue.EMPTY:
                    print("   |", end='')
                elif col == board.TTTValue.X:
                    print(" X |", end='')
                else:
                    print(" O |", end='')

            print("\n-------------")
