# a3-old.py Tic-Tac-Toe
# Goal of Tic-Tac-Toe: Obtain three consecutive tiles, along any row, column or diagonal in a 3x3 matrix.


# Each turn a player places either a 'X' or 'O' tile. Assuming X wins there must be one more 'X' than 'O" (where player
# using 'X' tile had the first turn), Equal numbers of 'X' and 'O' result in 'O' Player winning.

# Win:  First to three
# Lose: Opponent first to three
# Tie:  Both reach three, none reach three, all tiles filled.

# Computer should never lose to a smart player (not perfect) end conditions: winning, and tie are acceptable but cannot
# lose

# 1) List all legal moves
# 2) For each move in legal moves generate random number 'n' play-outs.
# 3) From n play-outs chose the next move that resulted in the largest number of winning play-outs.

# Random play-out:
# 1) Select random tile to play from legal moves.
# 2) Repeat (1) until W,T,or L.

import random


class TicTacToe:
    def __init__(self):
        self.activePlayer = 1
        self.gameBoard = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.AI = 1

    def getAI(self):
        return self.AI

    def setAI(self, first):
        if first:
            return self.AI
        else:
            self.AI = 2
            return self.AI

    def copyGameState(self):
        """Provide a copy of the current game's state"""
        copyGame = TicTacToe()
        copyGame.activePlayer = self.activePlayer
        copyGame.gameBoard = self.gameBoard[:]
        copyGame.AI = self.AI
        return copyGame

    def getGameBoard(self):
        return self.gameBoard

    def currentPlayer(self):
        return self.activePlayer

    def switchPlayerState(self):
        if self.activePlayer == 2:
            self.activePlayer = 1
        else:
            self.activePlayer = 2
        return self.activePlayer

    def placeMove(self, index, player):
        """index is where on the matrix the move will be placed, and player
        tracks which player placed the move"""
        if self.gameBoard[index] is not 0:
            print('that space has already been taken, start a new game')
            play_a_new_game()
        else:
            self.gameBoard[index] = player
            return self.gameBoard

    def checkMove(self, index):
        if self.gameBoard[index] is not 0:
            print('that space has already been taken, start a new game')
            play_a_new_game()
        return True

    def gameState(self):
        """checks the state of the game to see if there is a winner"""
        gameState = False
        if self.GameWinState() == -1:
            gameState = True
        return gameState

    def zeroCheck(self, numArr):
        """Checks indices provided for zero's returns true if zero's are
        present."""
        noZero = True
        for x in numArr:
            if self.gameBoard[x] == 0:
                noZero = False
        return noZero

    def GameWinState(self):
        """checks for win states. 0 is a draw, 1, P1 wins, 2, P2 wins. If a game is in progress the state will be -1.
        There are 8 win states in the game, all three rows, all three columns two diagonals."""

        if self.gameBoard[0] == self.gameBoard[3] and self.gameBoard[0] == self.gameBoard[6] and self.zeroCheck(
                [0, 3, 6]):
            if self.gameBoard[0] == 1:
                winFlag = 1
            else:
                winFlag = 2
        elif self.gameBoard[1] == self.gameBoard[4] and self.gameBoard[1] == self.gameBoard[7] and self.zeroCheck(
                [1, 4, 7]):
            if self.gameBoard[1] == 1:
                winFlag = 1
            else:
                winFlag = 2
        elif self.gameBoard[2] == self.gameBoard[5] and self.gameBoard[2] == self.gameBoard[8] and self.zeroCheck(
                [2, 5, 8]):
            if self.gameBoard[2] == 1:
                winFlag = 1
            else:
                winFlag = 2
        elif self.gameBoard[0] == self.gameBoard[1] and self.gameBoard[0] == self.gameBoard[2] and self.zeroCheck(
                [0, 1, 2]):
            if self.gameBoard[0] == 1:
                winFlag = 1
            else:
                winFlag = 2
        elif self.gameBoard[3] == self.gameBoard[4] and self.gameBoard[3] == self.gameBoard[5] and self.zeroCheck(
                [3, 4, 5]):
            if self.gameBoard[3] == 1:
                winFlag = 1
            else:
                winFlag = 2
        elif self.gameBoard[6] == self.gameBoard[7] and self.gameBoard[6] == self.gameBoard[8] and self.zeroCheck(
                [6, 7, 8]):
            if self.gameBoard[6] == 1:
                winFlag = 1
            else:
                winFlag = 2
        elif self.gameBoard[0] == self.gameBoard[4] and self.gameBoard[0] == self.gameBoard[8] and self.zeroCheck(
                [0, 4, 8]):
            if self.gameBoard[0] == 1:
                winFlag = 1
            else:
                winFlag = 2
        elif self.gameBoard[2] == self.gameBoard[4] and self.gameBoard[2] == self.gameBoard[6] and self.zeroCheck(
                [2, 4, 6]):
            if self.gameBoard[2] == 1:
                winFlag = 1
            else:
                winFlag = 2
        elif 0 not in self.gameBoard:
            winFlag = 0

        else:
            winFlag = -1

        return winFlag

    def display(self):
        """Displays current game board"""
        matrix = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
        for i in range(9):
            if self.gameBoard[i] == 1:
                matrix[i] = 'X'
            if self.gameBoard[i] == 2:
                matrix[i] = 'O'
        print('', matrix[0], '|', matrix[1], '|', matrix[2], '\n', '- + - + -\n',
              matrix[3], '|', matrix[4], '|', matrix[5], '\n', '- + - + -\n',
              matrix[6], '|', matrix[7], '|', matrix[8], '\n')

    def legalMoves(self):
        legalIndex = []
        for i in range(9):
            if self.gameBoard[i] == 0:
                legalIndex.append(i)
        return legalIndex


class monteCarloTreeSearch:
    def __init__(self, game, randPlayOutNum):
        self.game = game
        self.board = self.game.getGameBoard()
        self.state = self.game.gameState()
        self.randPlayOutNum = randPlayOutNum

    def makeMove(self):
        legalMoves = self.game.legalMoves()
        moveWinCounts = {}
        for m in legalMoves:  # for each legal moves
            moveWinCounts[m] = 0
        for m in legalMoves:
            for i in range(self.randPlayOutNum):
                moveWinCounts[m] += self.randomPlayOut(m)
        movechoice = legalMoves[0]
        choiceWinCount = moveWinCounts[movechoice]
        for win in moveWinCounts:
            if moveWinCounts[win] >= choiceWinCount:
                movechoice = win
                choiceWinCount = moveWinCounts[win]
        self.game.placeMove(int(movechoice), self.game.activePlayer)

    def randomPlayOut(self, move):
        copyCurrentGame = self.game.copyGameState()
        copyCurrentGame.placeMove(move, copyCurrentGame.activePlayer)  # make the move
        copyCurrentGame.switchPlayerState()  # switch player

        while copyCurrentGame.gameState():
            legalMoves = copyCurrentGame.legalMoves()
            randMove = random.randint(0, 8)
            while randMove not in legalMoves:
                randMove = random.randint(0, 8)
            copyCurrentGame.placeMove(randMove, copyCurrentGame.activePlayer)
            copyCurrentGame.switchPlayerState()
            copyCurrentGame.state = copyCurrentGame.gameState()
        if copyCurrentGame.getAI() == 1:
            if copyCurrentGame.GameWinState() == 2:
                return -5
            elif copyCurrentGame.GameWinState() == 1:
                return 2
            else:
                return 1
        else:
            if copyCurrentGame.GameWinState() == 2:
                return 2
            elif copyCurrentGame.GameWinState() == 1:
                return -5
            else:
                return 1


def BoardInfo():
    """ qwe
        asd
        zxc
    was chosen as not everyone has a numpad"""
    print("Welcome to Tic Tac Toe.")
    print('''You are either O or X.
You choose where to place your mark with 

      q|w|e
      -+-+-
      a|s|d
      -+-+-
      z|x|c''')
    print()
    return 0


def play_a_new_game():
    translation = {
        "q": 0,
        "w": 1,
        "e": 2,
        "a": 3,
        "s": 4,
        "d": 5,
        "z": 6,
        "x": 7,
        "c": 8
    }

    game = TicTacToe()
    aiMonte = monteCarloTreeSearch(game, 6789)
    gameState = game.gameState()
    BoardInfo()
    turn = input("Chose if you want to go first (Y/n): ")
    if turn.upper() == 'N':
        aiMonte.makeMove()
        game.switchPlayerState()
        game.display()
        playerMove = input('Choose your next move... ')
        playerMove = translation[playerMove]
    else:
        game.setAI(False)
        game.display()
        playerMove = input('Choose your next move... ')
        playerMove = translation[playerMove]
    while gameState:
        game.placeMove(playerMove, game.activePlayer)
        game.display()
        game.switchPlayerState()
        aiMonte.makeMove()
        gameState = game.gameState()
        if gameState:
            game.switchPlayerState()
            game.display()
            playerMove = input('Choose your next move... ')
            playerMove = translation[playerMove]
            game.checkMove(int(playerMove))
            gameCheck = game.copyGameState()
            gameCheck.placeMove(int(playerMove), gameCheck.activePlayer)
            gameState = gameCheck.gameState()

    game.placeMove(int(playerMove), game.activePlayer)
    print('\n')
    game.display()
    print('Game Finished')


if __name__ == '__main__':
    play_a_new_game()
