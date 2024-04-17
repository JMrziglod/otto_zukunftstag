import json
import os
from time import time

import cv2
import numpy as np

import simpleaudio as sa

sound_locked_in = sa.WaveObject.from_wave_file("locked_in.wav")
sound_lost = sa.WaveObject.from_wave_file("fail.wav")
sound_victory = sa.WaveObject.from_wave_file("victory.wav")
sound_draw = sa.WaveObject.from_wave_file("draw.wav")


from game import board, draw_tic_tac_toe, check_winner, calculate_ai_move, get_cell


def calibrate(frame, cell_index):
    """Calibrate the pointer detection by detecting the red color in the frame."""
    cell = get_cell(frame, *cell_index)
    cal_color = cell.mean(axis=(0,1)).astype(np.uint8)
    return cal_color.tolist()

def draw_grid(frame, highlight=None):
    """Draw a grid on the frame."""
    cell_size = frame.shape[0]//3
    top = int(frame.shape[0]//2-1.5*cell_size)
    bottom = int(frame.shape[0]//2+1.5*cell_size)
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

    if highlight is not None:
        cv2.rectangle(frame, (left+highlight[1]*cell_size, top+highlight[0]*cell_size), (left+(highlight[1]+1)*cell_size, top+(highlight[0]+1)*cell_size), (0, 255, 0), 2)

def detect_pointer(frame, calibration):
    """Detect a red area in the frame and return the row and column of the cell with the most red pixels."""
    best_cell = (None, 15)

    original_frame = frame.copy()

    for row in range(3):
        for col in range(3):
            cell = get_cell(original_frame, row, col)
            target_error = (np.abs(cell.mean(axis=(0,1))-np.array(calibration["targets"][row][col])).mean())
            default_error = (np.abs(cell.mean(axis=(0,1))-np.array(calibration["defaults"][row][col])).mean())
            cv2.putText(frame, f"{target_error:.2f}, {default_error:.2f}", (int(frame.shape[1]//2-1.5*frame.shape[0]//3+col*frame.shape[0]//3+frame.shape[0]//6), int(frame.shape[0]//2-1.5*frame.shape[0]//3+row*frame.shape[0]//3)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (150, 150, 150), 2)
            if target_error < default_error and target_error < best_cell[1]:
                best_cell = (row, col), target_error

    return best_cell

def save_calibration(calibration):
    with open('calibration_values.json', 'w') as f:
        json.dump(calibration, f)

def load_calibration():
    with open('calibration_values.json', 'r') as f:
        return json.load(f)

# Create a VideoCapture object to capture video from the webcam
cap = cv2.VideoCapture(0)

start_time = time()
last_selected_cell = None
waiting_for_ai = False
played_end_sound = False

# Are we calibrating the pointer detection? And if yes, which cell are we calibrating?
calibrating = [0, 0]
calibration_start = None
calibration = {
    "targets": [[None, None, None], [None, None, None], [None, None, None]],
    "defaults": [[None, None, None], [None, None, None], [None, None, None]],
}
while True:
    # Read the current frame from the webcam
    ret, frame = cap.read()

    # Check if we are calibrating the pointer detection
    if calibrating is not None:
        if calibration["defaults"][0][0] is None:
            for row in range(3):
                for col in range(3):
                    calibration["defaults"][row][col] = get_cell(frame, row, col).mean(axis=(0,1)).astype(np.uint8).tolist()

        cal_target = calibrate(frame, calibrating)
        draw_grid(frame, calibrating)
        cv2.putText(frame, f"CALIBRATION MODE...", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, f"Move your colored object to {calibrating}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, f"Press <W> for next field", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, f"Press <R> to reset", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, f"Press <L> to load", (10, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.imshow('Tic Tac Toe', frame)
        c = cv2.waitKey(1) % 256
        if c == ord('q'):
            calibrating = None
        elif c == ord('w'):
            calibration["targets"][calibrating[0]][calibrating[1]] = cal_target
            calibrating[0] += 1
            if calibrating[0] >= 3:
                calibrating = [0, calibrating[1]+1]
            if calibrating == [0, 3]:
                # save calibration and enter game mode
                save_calibration(calibration)
                calibrating = None
        elif c == ord('r'):
            calibration = {
                "targets": [[None, None, None], [None, None, None], [None, None, None]],
                "defaults": [[None, None, None], [None, None, None], [None, None, None]],
            }
            calibrating = [0, 0]
        elif c == ord('l'):
            calibration = load_calibration()
            calibrating = None
        continue

    winner = check_winner(board)
    if winner is not None or winner == 0:
        if winner == 0:
            if not played_end_sound: 
                sound_draw.play()
                played_end_sound = True
            cv2.putText(frame, "It's a draw!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif winner == 1:
            if not played_end_sound: 
                sound_lost.play()
                played_end_sound = True
            cv2.putText(frame, f"You lost!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif winner == 2:
            if not played_end_sound: 
                sound_victory.play()
                played_end_sound = True
            cv2.putText(frame, f"You won!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, "Press <Q> to quit", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, "Press <A> to play again", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        draw_grid(frame)
        draw_tic_tac_toe(frame, board)

        # Display the frame
        cv2.imshow('Tic Tac Toe', frame)

        # Check for the 'q' key to exit the loop
        c = cv2.waitKey(1) % 256
        if c == ord('q'):
            break
        if c == ord('a'):
            board = [[None, None, None], [None, None, None], [None, None, None]]
            last_selected_cell = None
            played_end_sound = False
        continue

    # Try to detect the pointer
    selected_cell, _ = detect_pointer(frame, calibration)

    # draw a squared tic tac toe board in the center of the board:
    cell_size = frame.shape[0]//3
    draw_grid(frame, highlight=selected_cell)
    draw_tic_tac_toe(frame, board)

    # Highlight the selected cell
    if selected_cell is not None and not waiting_for_ai:
        row, col = selected_cell
        if board[row][col] is not None:
            pass
        elif last_selected_cell != selected_cell:
            last_selected_cell = selected_cell
            start_time = time()
        elif time() - start_time > 3:
            # countdown timer until we log in the move
            board[row][col] = 2
            start_time = time()
            waiting_for_ai = True
            sound_locked_in.play()
        else:
            cv2.putText(frame, f"Locked in {3-int(time()-start_time)}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
    elif waiting_for_ai:
        ai_move = calculate_ai_move(board)
        if ai_move is not None:
            row, col = ai_move
            board[row][col] = 1
            waiting_for_ai = False
            start_time = time()

    # Display the frame
    cv2.imshow('Tic Tac Toe', frame)

    # Check for the 'q' key to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close the window
cap.release()
cv2.destroyAllWindows()