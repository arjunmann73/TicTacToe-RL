class GameBoard():
    def __init__(self, size=3):
        self.size = size
        self.positions = [x for x in range(1, size*size + 1)]
        self.board = [['-','-','-'],
                      ['-','-','-'],
                      ['-','-','-']]
        self.player = 'O' # we train for O winning!

    def player(self):
        return self.player

    def win(self):
        for i in range(self.size):
            if self.board[i] == ['X', 'X', 'X'] or self.board[i] == ['O', 'O', 'O']:
                return True
        if (self.board[0][0] == 'X' and self.board[1][0] == 'X' and self.board[2][0] == 'X') or (self.board[0][0] == 'O' and self.board[1][0] == 'O' and self.board[2][0] == 'O'):
            return True
        if (self.board[0][1] == 'X' and self.board[1][1] == 'X' and self.board[2][1] == 'X') or (self.board[0][1] == 'O' and self.board[1][1] == 'O' and self.board[2][1] == 'O'):
            return True
        if (self.board[0][2] == 'X' and self.board[1][2] == 'X' and self.board[2][2] == 'X') or (self.board[0][2] == 'O' and self.board[1][2] == 'O' and self.board[2][2] == 'O'):
            return True
        if (self.board[0][0] == 'X' and self.board[1][1] == 'X' and self.board[2][2] == 'X') or (self.board[0][0] == 'O' and self.board[1][1] == 'O' and self.board[2][2] == 'O'):
            return True
        if (self.board[0][2] == 'X' and self.board[1][1] == 'X' and self.board[2][0] == 'X') or (self.board[0][2] == 'O' and self.board[1][1] == 'O' and self.board[2][0] == 'O'):
            return True
        return False

    def openPositions(self):
        return self.positions

    def chance(self, position):
        self.positions.remove(position)
        if position == 1:
            self.board[0][0] = self.player
        elif position == 2:
            self.board[0][1] = self.player
        elif position == 3:
            self.board[0][2] = self.player
        elif position == 4:
            self.board[1][0] = self.player
        elif position == 5:
            self.board[1][1] = self.player
        elif position == 6:
            self.board[1][2] = self.player
        elif position == 7:
            self.board[2][0] = self.player
        elif position == 8:
            self.board[2][1] = self.player
        elif position == 9:
            self.board[2][2] = self.player

    def currentState(self):
        string = ''
        for i in range(self.size):
            for j in range(self.size):
                string += self.board[i][j]
        return string


    def playerChange(self):
        if self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'

    def printState(self):
        for i in range(self.size):
            print(self.board[i])
