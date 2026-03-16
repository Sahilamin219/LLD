import java.util.Scanner;


enum GameState {
    IN_PROGRESS,
    WIN,
    DRAW
}


class Player {
    String name;
    char colour;

    public Player(String name, char colour) {
        this.name = name;
        this.colour = colour;
    }

}


class Board {
    int row;
    int col;
    char[][] grid;

    public Board() {
    
        this.row = 6;
        this.col = 7;
        this.grid = new char[row][col];
        // Initialize the grid with empty spaces
        for (int i = 0; i < row; i++) {
            for (int j = 0; j < col; j++) {
                grid[i][j] = ' ';
            }
        }
    }

    public void printBoard() {
        for (int i = 0; i < row; i++) {
            for (int j = 0; j < col; j++) {
                System.out.print("| " + grid[i][j] + " ");
            }
            System.out.println("|");
        }
        
        System.out.println();
    }


}


public class Game {
    private Board board;
    private Player player1;
    private Player player2;
    private Player currentPlayer;
    private GameState gameState;
    private Player winner;

    private int moveCount;

    public Game(Player player1, Player player2) {
        this.board = new Board();
        this.player1 = player1;
        this.player2 = player2;
        this.currentPlayer = player1; // Player 1 starts
        this.gameState = GameState.IN_PROGRESS;
        this.winner = null;
    }

    public void printBoard() {
        board.printBoard();
    }
    public Player getCurrentPlayer() {
        return currentPlayer;
    }

    public void makeMove(int column) {

        if(gameState != GameState.IN_PROGRESS) {
            System.out.println("Game is already over. Please start a new game.");
            return;
        }
        
        if( column < 0 || column >= board.col) {
            System.out.println("Invalid column. Please choose a column between 0 and " + (board.col - 1));
            return;
        }

        if(board.grid[0][column] != ' ') {
            System.out.println("Column is full. Please choose a different column.");
            return;
        }

        for (int i = board.row - 1; i >= 0; i--) {

            if (board.grid[i][column] == ' ') {
                board.grid[i][column] = currentPlayer.colour;
                moveCount+=1;
                // After placing the token, check for a win or draw
                if (checkWin(i, column)) {
                    gameState = GameState.WIN;
                    winner = currentPlayer;
                } else if (checkDraw()) {
                    gameState = GameState.DRAW;
                } else {
                    switchPlayer();
                }
                break;
            }
        }
    }

    public Player getWinner() {
        return winner;
    }

    public void switchPlayer() {
        currentPlayer = (currentPlayer == player1) ? player2 : player1;
    }

    public boolean checkWin(int row, int col) {
        char token = currentPlayer.colour;
        // Check horizontal, vertical, and diagonal directions for a win
        return (checkDirection(row, col, 0, 1, token) || // Horizontal
                checkDirection(row, col, 1, 0, token) || // Vertical
                checkDirection(row, col, 1, 1, token) || // Diagonal \
                checkDirection(row, col, 1, -1, token));  // Diagonal /
    }

    private boolean checkDirection(int row, int col, int deltaRow, int deltaCol, char token) {
        int count = 0;
        int r = row;
        int c = col;

        // Check in the positive direction
        while (r >= 0 && r < board.row && c >= 0 && c < board.col && board.grid[r][c] == token) {
            count++;
            r += deltaRow;
            c += deltaCol;
        }

        // Check in the negative direction
        r = row - deltaRow;
        c = col - deltaCol;
        while (r >= 0 && r < board.row && c >= 0 && c < board.col && board.grid[r][c] == token) {
            count++;
            r -= deltaRow;
            c -= deltaCol;
        }

        return count >= 4;
    }

    public boolean checkDraw() {
        if(moveCount >= board.row * board.col) {
            return true;
        }   
        return false;
    }

    public static void main(String[] args) {
        Player player1 = new Player("Alice", 'R');
        Player player2 = new Player("Bob", 'Y');
        Game game = new Game(player1, player2);
        Scanner scanner = new Scanner(System.in);

        while (game.gameState == GameState.IN_PROGRESS) {
            game.printBoard();
            System.out.println("Current player: " + game.getCurrentPlayer().name);
            System.out.println("Please enter a column (0-6): ");
            int column = scanner.nextInt();
            game.makeMove(column);
        }

        if (game.gameState == GameState.WIN) {
            System.out.println("Game Over! Winner: " + game.getWinner().name);
        } else {
            System.out.println("Game Over! It's a draw.");
        }
        scanner.close();
    }
}
