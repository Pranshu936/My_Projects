import java.util.Scanner;

public class TicTacToe {
    private static final int SIZE = 3; // Size of the Tic-Tac-Toe board
    private static final char EMPTY = ' '; // Empty cell representation
    private static char[][] board = new char[SIZE][SIZE]; // Game board

    private static char currentPlayer = 'X'; // Player X starts first

    public static void main(String[] args) {
        initializeBoard();

        Scanner scanner = new Scanner(System.in);
        boolean gameRunning = true;

        while (gameRunning) {
            displayBoard();

            int row, col;
            do {
                System.out.println("Player " + currentPlayer + ", enter your move (row [1-3] column [1-3]):");
                row = scanner.nextInt() - 1;
                col = scanner.nextInt() - 1;
            } while (!isValidMove(row, col));

            board[row][col] = currentPlayer;

            if (checkWin()) {
                displayBoard();
                System.out.println("Player " + currentPlayer + " wins!");
                gameRunning = false;
            } else if (checkDraw()) {
                displayBoard();
                System.out.println("It's a draw!");
                gameRunning = false;
            } else {
                currentPlayer = (currentPlayer == 'X') ? 'O' : 'X'; // Switch player
            }
        }

        scanner.close();
    }

    private static void initializeBoard() {
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                board[i][j] = EMPTY;
            }
        }
    }

    private static void displayBoard() {
        System.out.println("-------------");
        for (int i = 0; i < SIZE; i++) {
            System.out.print("| ");
            for (int j = 0; j < SIZE; j++) {
                System.out.print(board[i][j] + " | ");
            }
            System.out.println("\n-------------");
        }
    }

    private static boolean isValidMove(int row, int col) {
        if (row < 0 || row >= SIZE || col < 0 || col >= SIZE) {
            System.out.println("Invalid move! Row and column should be between 1 and " + SIZE);
            return false;
        }
        if (board[row][col] != EMPTY) {
            System.out.println("Invalid move! Cell already occupied.");
            return false;
        }
        return true;
    }

    private static boolean checkWin() {
        // Check rows and columns
        for (int i = 0; i < SIZE; i++) {
            if (board[i][0] == currentPlayer && board[i][1] == currentPlayer && board[i][2] == currentPlayer) {
                return true; // Row win
            }
            if (board[0][i] == currentPlayer && board[1][i] == currentPlayer && board[2][i] == currentPlayer) {
                return true; // Column win
            }
        }

        // Check diagonals
        if (board[0][0] == currentPlayer && board[1][1] == currentPlayer && board[2][2] == currentPlayer) {
            return true; // Top-left to bottom-right diagonal win
        }
        if (board[0][2] == currentPlayer && board[1][1] == currentPlayer && board[2][0] == currentPlayer) {
            return true; // Top-right to bottom-left diagonal win
        }

        return false;
    }

    private static boolean checkDraw() {
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                if (board[i][j] == EMPTY) {
                    return false; // There's an empty cell, game is not a draw yet
                }
            }
        }
        return true; // All cells are filled, game is a draw
    }
}
