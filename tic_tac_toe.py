import cv2
import mediapipe as mp
import numpy as np
import random
import time
import math

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode,
                                        max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))
        return lmList

def draw_grid(img):
    h, w, _ = img.shape
    step_x = w // 3
    step_y = h // 3
    for i in range(1, 3):
        cv2.line(img, (i * step_x, 0), (i * step_x, h), (255, 255, 255), 2)
        cv2.line(img, (0, i * step_y), (w, i * step_y), (255, 255, 255), 2)
    return step_x, step_y

def get_cell(x, y, step_x, step_y):
    row, col = y // step_y, x // step_x
    return int(row), int(col)

def draw_symbol(img, symbol, cell, step_x, step_y):
    x_center = cell[1] * step_x + step_x // 2
    y_center = cell[0] * step_y + step_y // 2
    if symbol == 'X':
        cv2.line(img, (x_center - 20, y_center - 20), (x_center + 20, y_center + 20), (0, 0, 255), 3)
        cv2.line(img, (x_center + 20, y_center - 20), (x_center - 20, y_center + 20), (0, 0, 255), 3)
    elif symbol == 'O':
        cv2.circle(img, (x_center, y_center), 20, (255, 0, 0), 3)

def check_win(board, player):
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    ]
    return [player, player, player] in win_conditions

def check_tie(board):
    return all(cell != "" for row in board for cell in row)

def computer_move(board):
    for r in range(3):
        for c in range(3):
            if board[r][c] == '':
                board[r][c] = 'O'
                if check_win(board, 'O'):
                    return (r, c)
                board[r][c] = ''

    for r in range(3):
        for c in range(3):
            if board[r][c] == '':
                board[r][c] = 'X'
                if check_win(board, 'X'):
                    board[r][c] = 'O'
                    return (r, c)
                board[r][c] = ''

    if board[1][1] == '':
        return (1, 1)

    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for (r, c) in corners:
        if board[r][c] == '':
            return (r, c)

    edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
    for (r, c) in edges:
        if board[r][c] == '':
            return (r, c)

    return None

def reset_game():
    return [["" for _ in range(3)] for _ in range(3)], False, True, False

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    detector = handDetector()
    board, game_over, player_turn, is_tie = reset_game()
    step_x, step_y = 0, 0
    last_click_time = 0
    click_delay = 1.0

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)  
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if step_x == 0 or step_y == 0:
            step_x, step_y = draw_grid(img)

        cv2.putText(img, "Computer: O", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(img, "Player: X", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if game_over:
            message = "Game Tied!" if is_tie else ("You Win!" if not player_turn else "You Lose!")
            cv2.putText(img, message, (100, 250), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0) if not player_turn else (0, 0, 255), 3)
            button_x1, button_y1 = 150, 300
            button_x2, button_y2 = 350, 350
            cv2.rectangle(img, (button_x1, button_y1), (button_x2, button_y2), (200, 200, 200), -1)
            cv2.putText(img, "Restart", (button_x1 + 30, button_y1 + 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

            if lmList and button_x1 < lmList[8][1] < button_x2 and button_y1 < lmList[8][2] < button_y2:
                board, game_over, player_turn, is_tie = reset_game()

        else:
            draw_grid(img)

            if player_turn and lmList:
                index_finger_pos = lmList[8][1:3]
                cv2.circle(img, (index_finger_pos[0], index_finger_pos[1]), 10, (255, 0, 0), cv2.FILLED)

                fingertip = lmList[8][1:3]
                cell = get_cell(fingertip[0], fingertip[1], step_x, step_y)

                margin = 20
                cell_x_start, cell_y_start = cell[1] * step_x + margin, cell[0] * step_y + margin
                cell_x_end, cell_y_end = (cell[1] + 1) * step_x - margin, (cell[0] + 1) * step_y - margin

                if cell_x_start <= fingertip[0] <= cell_x_end and cell_y_start <= fingertip[1] <= cell_y_end:
                    if board[cell[0]][cell[1]] == "" and time.time() - last_click_time > click_delay:
                        board[cell[0]][cell[1]] = 'X'
                        last_click_time = time.time()
                        draw_symbol(img, 'X', cell, step_x, step_y)
                        if check_win(board, 'X'):
                            game_over = True
                        elif check_tie(board):
                            game_over = True
                            is_tie = True
                        player_turn = False

            elif not player_turn:
                move = computer_move(board)
                if move:
                    board[move[0]][move[1]] = 'O'
                    draw_symbol(img, 'O', move, step_x, step_y)
                    if check_win(board, 'O'):
                        game_over = True
                    elif check_tie(board):
                        game_over = True
                        is_tie = True
                player_turn = True

            for r in range(3):
                for c in range(3):
                    if board[r][c] != "":
                        draw_symbol(img, board[r][c], (r, c), step_x, step_y)

        cv2.imshow("Tic-Tac-Toe", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
