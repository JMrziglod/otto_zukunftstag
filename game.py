import json
from time import time

import cv2
import numpy as np
import simpleaudio as sa



def get_cell(frame, row, col):
    """Return the frame conntent at the given row and column of the tic tac toe board."""
    cell_size = frame.shape[0]//3
    left = int(frame.shape[1]//2-1.5*cell_size)
    right = int(frame.shape[1]//2+1.5*cell_size)
    top = int(frame.shape[0]//2-1.5*cell_size)
    return frame[top+row*cell_size:top+(row+1)*cell_size, left+col*cell_size:right+(col+1)*cell_size]

class TicTacToe:
    def __init__(self):
        # Create a 3x3 tic tac toe board, there are two players: 1 and 2
        self.board = [[None, None, None], [None, None, None], [None, None, None]]
        self.last_selected_cell = None
        self.played_end_sound = False
        self.waiting_for_ai = False
        self.calibration = {
            "targets": [[None, None, None], [None, None, None], [None, None, None]],
            "defaults": [[None, None, None], [None, None, None], [None, None, None]],
        }
        self.calibrating = [0, 0]
        self.start_time = time()
        self.sound_locked_in = sa.WaveObject.from_wave_file("locked_in.wav")
        self.sound_lost = sa.WaveObject.from_wave_file("fail.wav")
        self.sound_victory = sa.WaveObject.from_wave_file("victory.wav")
        self.sound_draw = sa.WaveObject.from_wave_file("draw.wav")

    def update(self, frame, key):
        if self.calibrating is not None:
            self.calibration_mode(frame, key)
            return
        
        winner = self.check_winner()
        if winner is not None or winner == 0:
            if winner == 0:
                if not self.played_end_sound: 
                    self.sound_draw.play()
                    self.played_end_sound = True
                cv2.putText(frame, "It's a draw!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            elif winner == 1:
                if not self.played_end_sound: 
                    self.sound_lost.play()
                    self.played_end_sound = True
                cv2.putText(frame, f"You lost!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            elif winner == 2:
                if not self.played_end_sound: 
                    self.sound_victory.play()
                    self.played_end_sound = True
                cv2.putText(frame, f"You won!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, "Press <Q> to quit", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, "Press <A> to play again", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            self.draw_board(frame)

            if key == ord('a'):
                self.reset()
            return

        # Try to detect the pointer
        selected_cell = self.detect_pointer(frame)

        # draw a squared tic tac toe board in the center of the board:
        self.draw_board(frame, highlight=selected_cell)

        # Lock in the move after 3 seconds
        if selected_cell is not None and not self.waiting_for_ai:
            row, col = selected_cell
            if self.board[row][col] is not None:
                pass
            elif self.last_selected_cell != selected_cell:
                self.last_selected_cell = selected_cell
                self.start_time = time()
            elif time() - self.start_time > 3:
                # countdown timer until we log in the move
                self.board[row][col] = 2
                self.start_time = time()
                self.waiting_for_ai = True
                self.sound_locked_in.play()
            else:
                cv2.putText(frame, f"Locked in {3-int(time()-self.start_time)}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
        elif self.waiting_for_ai:
            ai_move = self.calculate_ai_move()
            if ai_move is not None:
                row, col = ai_move
                self.board[row][col] = 1
                self.waiting_for_ai = False
                start_time = time()

    def reset(self):
        self.board = [[None, None, None], [None, None, None], [None, None, None]]
        self.last_selected_cell = None
        self.played_end_sound = False
        self.waiting_for_ai = False
        self.start_time = time()

    def reset_calibration(self):
        self.calibration = {
            "targets": [[None, None, None], [None, None, None], [None, None, None]],
            "defaults": [[None, None, None], [None, None, None], [None, None, None]],
        }
        self.calibrating = [0, 0]

    def calibration_mode(self, frame, key):
        if self.calibration["defaults"][0][0] is None:
            for row in range(3):
                for col in range(3):
                    self.calibration["defaults"][row][col] = get_cell(frame, row, col).mean(axis=(0,1)).astype(np.uint8).tolist()

        cell = get_cell(frame, *self.calibrating)
        cal_target = cell.mean(axis=(0,1)).astype(np.uint8).tolist()
        self.draw_board(frame, highlight=self.calibrating)
        cv2.putText(frame, f"CALIBRATION MODE...", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, f"Move your colored object to {self.calibrating}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, f"Press <W> for next field", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, f"Press <R> to reset", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, f"Press <L> to load", (10, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        if key == ord('w'):
            self.calibration["targets"][self.calibrating[0]][self.calibrating[1]] = cal_target
            self.calibrating[0] += 1
            if self.calibrating[0] >= 3:
                self.calibrating = [0, self.calibrating[1]+1]
            if self.calibrating == [0, 3]:
                # save calibration and enter game mode
                self.save_calibration()
                self.calibrating = None
        elif key == ord('r'):
            self.reset_calibration()
        elif key == ord('l'):
            self.load_calibration()
            self.calibrating = None

    def draw_board(self, frame, highlight=None):
        """Draw a grid on the frame."""
        cell_size = frame.shape[0]//3
        top = int(frame.shape[0]//2-1.5*cell_size)
        left = int(frame.shape[1]//2-1.5*cell_size)
        right = int(frame.shape[1]//2+1.5*cell_size)
        # draw vertical lines
        cv2.line(frame, (int(frame.shape[1]//2-1.5*cell_size), 0), (int(frame.shape[1]//2-1.5*cell_size), frame.shape[0]), (0, 0, 255), 2)
        cv2.line(frame, (int(frame.shape[1]//2-.5*cell_size), 0), (int(frame.shape[1]//2-.5*cell_size), frame.shape[0]), (0, 0, 255), 2)
        cv2.line(frame, (int(frame.shape[1]//2+.5*cell_size), 0), (int(frame.shape[1]//2+.5*cell_size), frame.shape[0]), (0, 0, 255), 2)
        cv2.line(frame, (int(frame.shape[1]//2+1.5*cell_size), 0), (int(frame.shape[1]//2+1.5*cell_size), frame.shape[0]), (0, 0, 255), 2)
        # draw horizontal lines
        cv2.line(frame, (left, int(frame.shape[0]//2-1.5*cell_size)), (right,  int(frame.shape[0]//2-1.5*cell_size)), (0, 0, 255), 2)
        cv2.line(frame, (left, int(frame.shape[0]//2-.5*cell_size)), (right, int(frame.shape[0]//2-.5*cell_size)), (0, 0, 255), 2)
        cv2.line(frame, (left, int(frame.shape[0]//2+.5*cell_size)), (right, int(frame.shape[0]//2+.5*cell_size)), (0, 0, 255), 2)
        cv2.line(frame, (left, int(frame.shape[0]//2+1.5*cell_size)), (right,  int(frame.shape[0]//2+1.5*cell_size)), (0, 0, 255), 2)

        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 1:
                    cv2.circle(frame, (int(frame.shape[1]//2-1.5*cell_size+cell_size//2+col*cell_size), int(frame.shape[0]//2-1.5*cell_size+cell_size//2+row*cell_size)), cell_size//3, (0, 0, 255), 2)
                elif self.board[row][col] == 2:
                    cv2.line(frame, (int(frame.shape[1]//2-1.5*cell_size+col*cell_size+cell_size//4), int(frame.shape[0]//2-1.5*cell_size+row*cell_size+cell_size//4)), (int(frame.shape[1]//2-1.5*cell_size+col*cell_size+3*cell_size//4), int(frame.shape[0]//2-1.5*cell_size+row*cell_size+3*cell_size//4)), (0, 0, 255), 2)
                    cv2.line(frame, (int(frame.shape[1]//2-1.5*cell_size+col*cell_size+cell_size//4), int(frame.shape[0]//2-1.5*cell_size+row*cell_size+3*cell_size//4)), (int(frame.shape[1]//2-1.5*cell_size+col*cell_size+3*cell_size//4), int(frame.shape[0]//2-1.5*cell_size+row*cell_size+cell_size//4)), (0, 0, 255), 2)

        if highlight is not None:
            cv2.rectangle(frame, (left+highlight[1]*cell_size, top+highlight[0]*cell_size), (left+(highlight[1]+1)*cell_size, top+(highlight[0]+1)*cell_size), (0, 255, 0), 2)

    def detect_pointer(self, frame):
        """Detect a red area in the frame and return the row and column of the cell with the most red pixels."""
        best_cell = (None, 15)

        original_frame = frame.copy()

        for row in range(3):
            for col in range(3):
                cell = get_cell(original_frame, row, col)
                target_error = (np.abs(cell.mean(axis=(0,1))-np.array(self.calibration["targets"][row][col])).mean())
                default_error = (np.abs(cell.mean(axis=(0,1))-np.array(self.calibration["defaults"][row][col])).mean())
                cv2.putText(frame, f"{target_error:.2f}, {default_error:.2f}", (int(frame.shape[1]//2-1.5*frame.shape[0]//3+col*frame.shape[0]//3+frame.shape[0]//6), int(frame.shape[0]//2-1.5*frame.shape[0]//3+row*frame.shape[0]//3)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (150, 150, 150), 2)
                if target_error < default_error and target_error < best_cell[1]:
                    best_cell = (row, col), target_error

        return best_cell[0]

    def save_calibration(self):
        with open('calibration_values.json', 'w') as f:
            json.dump(self.calibration, f)

    def load_calibration(self):
        with open('calibration_values.json', 'r') as f:
            self.calibration = json.load(f)

    def check_winner(self):
        """Return the winner of the game, 0 if it is a draw or None if there is no winner yet."""
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] and self.board[row][0] is not None:
                return self.board[row][0]
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] is not None:
                return self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            return self.board[0][2]
        
        if all(item is not None for row in self.board for item in row):
            return 0

        return None
    
    def calculate_ai_move(self):
        """Simple AI that tries to win, then tries to block the opponent, then makes a random move.
        
        Returns:
            - row, col
            - or None if the board is full
        """
        # Try to win
        for row in range(3):
            for col in range(3):
                if self.board[row][col] is None:
                    self.board[row][col] = 1
                    if self.check_winner() == 1:
                        return row, col
                    self.board[row][col] = None

        # Try to block the opponent
        for row in range(3):
            for col in range(3):
                if self.board[row][col] is None:
                    self.board[row][col] = 2
                    if self.check_winner() == 2:
                        self.board[row][col] = 1
                        return row, col
                    self.board[row][col] = None

        # Make a random move, start from the top left corner
        for row in range(3):
            for col in range(3):
                if self.board[row][col] is None:
                    self.board[row][col] = 1
                    return row, col

        return None