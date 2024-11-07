# Import necessary libraries
import cv2               # OpenCV for image processing and camera interaction
import mediapipe as mp   # Mediapipe for hand tracking
import numpy as np       # Numpy for handling numerical operations (e.g., coordinates)
import random            # For random moves (if needed)
import time              # For handling delays (to control click intervals)
import math              # For mathematical operations (though not used directly here)

# Hand detection class definition
class handDetector():
    # Initialize the detector with optional configurations
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode  # Mode for static or dynamic image (False for dynamic, True for static)
        self.maxHands = maxHands  # Max number of hands to detect
        self.detectionCon = detectionCon  # Minimum detection confidence
        self.trackCon = trackCon  # Minimum tracking confidence

        self.mpHands = mp.solutions.hands  # Hand module from Mediapipe
        self.hands = self.mpHands.Hands(static_image_mode=self.mode,
                                        max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)  # Initialize the hands module
        self.mpDraw = mp.solutions.drawing_utils  # Drawing utilities for rendering landmarks

    # Function to find and draw hands in the image
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert image to RGB (required by Mediapipe)
        self.results = self.hands.process(imgRGB)  # Process the image for hand landmarks
        if self.results.multi_hand_landmarks:  # If hands are detected
            for handLms in self.results.multi_hand_landmarks:  # For each hand
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)  # Draw landmarks and connections
        return img  # Return the image with the hand landmarks drawn

    # Function to find the positions of hand landmarks
    def findPosition(self, img, handNo=0):
        lmList = []  # Initialize an empty list to store landmarks
        if self.results.multi_hand_landmarks:  # If hands are detected
            myHand = self.results.multi_hand_landmarks[handNo]  # Get the landmarks of the selected hand
            for id, lm in enumerate(myHand.landmark):  # Loop through each landmark (id, position)
                h, w, c = img.shape  # Get the dimensions of the image
                cx, cy = int(lm.x * w), int(lm.y * h)  # Calculate the (x, y) coordinates in the image
                lmList.append((id, cx, cy))  # Append the landmark id and its coordinates to the list
        return lmList  # Return the list of landmarks

# Function to draw the Tic-Tac-Toe grid on the screen
def draw_grid(img):
    h, w, _ = img.shape  # Get image dimensions (height, width)
    step_x = w // 3  # Divide the width into 3 equal steps (for columns)
    step_y = h // 3  # Divide the height into 3 equal steps (for rows)
    
    # Draw vertical lines to create columns
    for i in range(1, 3):
        cv2.line(img, (i * step_x, 0), (i * step_x, h), (255, 255, 255), 2)
        # Draw horizontal lines to create rows
        cv2.line(img, (0, i * step_y), (w, i * step_y), (255, 255, 255), 2)
    
    return step_x, step_y  # Return the step size in x and y directions for grid cells

# Function to calculate the grid cell where a point (x, y) falls
def get_cell(x, y, step_x, step_y):
    row, col = y // step_y, x // step_x  # Calculate row and column by integer division
    return int(row), int(col)  # Return the row and column as integers

# Function to draw X or O symbols in the grid cells
def draw_symbol(img, symbol, cell, step_x, step_y):
    x_center = cell[1] * step_x + step_x // 2  # Calculate the center x-coordinate of the cell
    y_center = cell[0] * step_y + step_y // 2  # Calculate the center y-coordinate of the cell
    if symbol == 'X':  # Draw an 'X' symbol (cross)
        cv2.line(img, (x_center - 20, y_center - 20), (x_center + 20, y_center + 20), (0, 0, 255), 3)
        cv2.line(img, (x_center + 20, y_center - 20), (x_center - 20, y_center + 20), (0, 0, 255), 3)
    elif symbol == 'O':  # Draw an 'O' symbol (circle)
        cv2.circle(img, (x_center, y_center), 20, (255, 0, 0), 3)

# Function to check if a player has won
def check_win(board, player):
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],  # Top row
        [board[1][0], board[1][1], board[1][2]],  # Middle row
        [board[2][0], board[2][1], board[2][2]],  # Bottom row
        [board[0][0], board[1][0], board[2][0]],  # Left column
        [board[0][1], board[1][1], board[2][1]],  # Middle column
        [board[0][2], board[1][2], board[2][2]],  # Right column
        [board[0][0], board[1][1], board[2][2]],  # Diagonal (top-left to bottom-right)
        [board[0][2], board[1][1], board[2][0]],  # Diagonal (top-right to bottom-left)
    ]
    return [player, player, player] in win_conditions  # Check if the player has a winning combination

# Function to check if the game is tied (no empty spaces left)
def check_tie(board):
    return all(cell != "" for row in board for cell in row)  # Return True if all cells are filled

# Function to calculate the computer's move (AI)
def computer_move(board):
    # First, check if the computer can win in the next move
    for r in range(3):
        for c in range(3):
            if board[r][c] == '':
                board[r][c] = 'O'
                if check_win(board, 'O'):
                    return (r, c)
                board[r][c] = ''  # Undo the move

    # Then, block the player if they are about to win
    for r in range(3):
        for c in range(3):
            if board[r][c] == '':
                board[r][c] = 'X'
                if check_win(board, 'X'):
                    board[r][c] = 'O'  # Undo the move
                    return (r, c)
                board[r][c] = ''  # Undo the move

    # If no immediate winning or blocking moves, take the center if available
    if board[1][1] == '':
        return (1, 1)

    # Otherwise, pick a random corner
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for (r, c) in corners:
        if board[r][c] == '':
            return (r, c)

    # If no corners, pick a random edge
    edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
    for (r, c) in edges:
        if board[r][c] == '':
            return (r, c)

    return None  # Return None if no move can be made (should not happen)

# Function to reset the game state
def reset_game():
    return [["" for _ in range(3)] for _ in range(3)], False, True, False  # Return an empty board and reset flags

# Main function
def main():
    cap = cv2.VideoCapture(0)  # Initialize the video capture (camera)
    cap.set(3, 1280)  # Set the width of the camera feed
    cap.set(4, 720)   # Set the height of the camera feed
    detector = handDetector()  # Initialize the hand detector
    board, game_over, player_turn, is_tie = reset_game()  # Reset the game state
    step_x, step_y = 0, 0  # Initialize step size for grid cells
    last_click_time = 0  # Initialize the last click time to control delays
    click_delay = 1.0  # Set the click delay in seconds

    # Game loop
    while True:
        success, img = cap.read()  # Capture a frame from the camera
        img = cv2.flip(img, 1)  # Flip the image horizontally for better interaction (mirroring)
        img = detector.findHands(img)  # Detect and draw hands
        lmList = detector.findPosition(img)  # Get the positions of hand landmarks

        if step_x == 0 or step_y == 0:  # Initialize grid step sizes if not already set
            step_x, step_y = draw_grid(img)

        # Display player and computer information on the screen
        cv2.putText(img, "Computer: O", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(img, "Player: X", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if game_over:  # If the game is over, display the result and a restart button
            message = "Game Tied!" if is_tie else ("You Win!" if not player_turn else "You Lose!")
            cv2.putText(img, message, (100, 250), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0) if not player_turn else (0, 0, 255), 3)
            button_x1, button_y1 = 150, 300  # Set the coordinates for the restart button
            button_x2, button_y2 = 350, 350
            cv2.rectangle(img, (button_x1, button_y1), (button_x2, button_y2), (200, 200, 200), -1)  # Draw the button
            cv2.putText(img, "Restart", (button_x1 + 30, button_y1 + 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

            # Check if the player clicks the restart button
            if lmList and button_x1 < lmList[8][1] < button_x2 and button_y1 < lmList[8][2] < button_y2:
                board, game_over, player_turn, is_tie = reset_game()

        else:
            draw_grid(img)  # Draw the grid

            # Handle player move
            if player_turn and lmList:
                index_finger_pos = lmList[8][1:3]  # Get the position of the index finger
                cv2.circle(img, (index_finger_pos[0], index_finger_pos[1]), 10, (255, 0, 0), cv2.FILLED)  # Draw a circle at fingertip

                fingertip = lmList[8][1:3]  # Get fingertip position
                cell = get_cell(fingertip[0], fingertip[1], step_x, step_y)  # Find the corresponding cell

                # Define margin for fingertip selection
                margin = 20
                cell_x_start, cell_y_start = cell[1] * step_x + margin, cell[0] * step_y + margin
                cell_x_end, cell_y_end = (cell[1] + 1) * step_x - margin, (cell[0] + 1) * step_y - margin

                # Check if the fingertip is inside the cell
                if cell_x_start <= fingertip[0] <= cell_x_end and cell_y_start <= fingertip[1] <= cell_y_end:
                    # If the cell is empty and enough time has passed since the last click
                    if board[cell[0]][cell[1]] == "" and time.time() - last_click_time > click_delay:
                        board[cell[0]][cell[1]] = 'X'  # Mark the cell with 'X'
                        last_click_time = time.time()  # Update the click time
                        draw_symbol(img, 'X', cell, step_x, step_y)  # Draw the 'X' symbol in the cell
                        if check_win(board, 'X'):  # Check if the player wins
                            game_over = True
                        elif check_tie(board):  # Check if the game is a tie
                            game_over = True
                            is_tie = True
                        player_turn = False  # Switch to computer's turn

            # Handle computer move
            elif not player_turn:
                move = computer_move(board)  # Calculate computer's move
                if move:
                    board[move[0]][move[1]] = 'O'  # Mark the cell with 'O'
                    draw_symbol(img, 'O', move, step_x, step_y)  # Draw the 'O' symbol in the cell
                    if check_win(board, 'O'):  # Check if the computer wins
                        game_over = True
                    elif check_tie(board):  # Check if the game is a tie
                        game_over = True
                        is_tie = True
                player_turn = True  # Switch to player's turn

            # Draw the current board state
            for r in range(3):
                for c in range(3):
                    if board[r][c] != "":  # If a cell is not empty
                        draw_symbol(img, board[r][c], (r, c), step_x, step_y)

        # Show the updated image in the window
        cv2.imshow("Tic-Tac-Toe", img)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()  # Release the camera
    cv2.destroyAllWindows()  # Close the window

# Main entry point to start the game
if __name__ == "__main__":
    main()
