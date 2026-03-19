"""Requirements:
1. Two players take turns dropping discs into a 7-column, 6-row board
2. A disc falls to the lowest available row in the chosen column
3. The game ends when:
    - A player gets four discs in a row (vertical, horizontal, or diagonal). They win.
    - The board is full. It's a draw.
4. Invalid moves should be rejected clearly:
    - Dropping in a full column.
    - Moving out of turn.
    - Moving after the game is over.

Out of scope: 
- UI support
- Concurrent games
- Move history
- Undo
- Board size configuration"""
from enum import Enum

class States(Enum):
    ON_GOING = "OnGoing"
    WON = "Won"
    DRAW = "Draw"

class Player:
    colorCount = 1
    @classmethod
    def resetColorCount(cls):
        cls.colorCount = 1

    def __init__(self, name, color=None):
        if color is None:
            color = Player.colorCount
            Player.colorCount += 1
        self.name = name
        self.color = color
class Board:
    def __init__(self, rows=6, columns=7):
        self.rows = rows
        self.columns = columns
        self.board = [ [0]*rows for i in range(columns) ]
class GameEngine:
    def __init__(self, player1, player2, board):
        self.player1 = player1
        self.player2 = player2
        self.state = States.ON_GOING
        self.currentPlayerTurn = player1
        self.board = board
        self.totalMoves = board.rows * board.columns
    def makeMove(self):
        playerToMove = self.currentPlayerTurn
        # self.currentPlayerTurn = self.playerList[(self.playerList.index(playerToMove) + 1) % len(self.playerList)]
        if( self.currentPlayerTurn == self.player1):
            self.currentPlayerTurn = self.player2
        else:
            self.currentPlayerTurn = self.player1
        userInput = input("Enter coordinates (x,y): ")
        userInput = userInput.strip("()")
        userInput = userInput.replace(" ", "")
        userInput = userInput.replace("(", "")
        userInput = userInput.replace(")", "")
        try:
            coordinates = list(map(int, userInput.split(",")))
            if len(coordinates) != 2 or coordinates[0] < 1 or coordinates[0] > 7 or coordinates[1] < 1 or coordinates[1] > 6:
                raise ValueError("Invalid coordinates")
            if self.board.board[coordinates[1]-1][coordinates[0]-1] != 0:
                raise ValueError("Invalid coordinates")
            print("Inputes were ", coordinates)
            self.totalMoves -= 1
            lowestRow = coordinates[1]
            while( lowestRow >= 0) :
                if self.board.board[coordinates[1]-1][lowestRow] != 0:
                    break
                lowestRow -= 1
            if lowestRow < 0: print("this col is filled till " + str(lowestRow)); return
            print(f"color changes lowestRow:{lowestRow}", self.board.board[coordinates[1]-1][lowestRow], playerToMove.color)
            self.board.board[coordinates[1]-1][lowestRow] = playerToMove.color
            checkForWin = self.checkForWin(coordinates[0]-1, coordinates[1]-1, playerToMove.color)
            if checkForWin:
                self.state = States.WON
                print(f"{playerToMove.name} wins!")
            elif self.totalMoves == 0:
                self.state = States.DRAW
                print("Draw!")
        except ValueError:
            print("Invalid coordinates. Please enter a valid x,y pair")
            return
    def getCurrentState(self):
        return self.state
    def getCurrentPlayer(self):
        return self.currentPlayerTurn
    def checkForWin(self, x, y, color):
        return False
    
game = GameEngine(player1=Player("Alice"), player2=Player("Bob"), board=Board())
while(game.getCurrentState() == States.ON_GOING): game.makeMove()
