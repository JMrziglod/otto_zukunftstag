import cv2
from time import time

# Create a 3x3 tic tac toe board, there are two players: 1 and 2
board = [[None, None, None], [None, None, None], [None, None, None]]

def draw_tic_tac_toe(frame, board):
    """Draw the tic tac toe board on the frame."""
    cell_size = frame.shape[0]//3
    left = int(frame.shape[1]//2-1.5*cell_size)
    right = int(frame.shape[1]//2+1.5*cell_size)
    top = int(frame.shape[0]//2-1.5*cell_size)
    bottom = int(frame.shape[0]//2+1.5*cell_size)
    for row in range(3):
        for col in range(3):
            if board[row][col] == 1:
                cv2.circle(frame, (int(frame.shape[1]//2-1.5*cell_size+cell_size//2+col*cell_size), int(frame.shape[0]//2-1.5*cell_size+cell_size//2+row*cell_size)), cell_size//3, (0, 0, 255), 2)
            elif board[row][col] == 2:
                cv2.line(frame, (int(frame.shape[1]//2-1.5*cell_size+col*cell_size+cell_size//4), int(frame.shape[0]//2-1.5*cell_size+row*cell_size+cell_size//4)), (int(frame.shape[1]//2-1.5*cell_size+col*cell_size+3*cell_size//4), int(frame.shape[0]//2-1.5*cell_size+row*cell_size+3*cell_size//4)), (0, 0, 255), 2)
                cv2.line(frame, (int(frame.shape[1]//2-1.5*cell_size+col*cell_size+cell_size//4), int(frame.shape[0]//2-1.5*cell_size+row*cell_size+3*cell_size//4)), (int(frame.shape[1]//2-1.5*cell_size+col*cell_size+3*cell_size//4), int(frame.shape[0]//2-1.5*cell_size+row*cell_size+cell_size//4)), (0, 0, 255), 2)

def check_winner(board):
    """Return the winner of the game, 0 if it is a draw or None if there is no winner yet."""
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    
    if all(item is not None for row in board for item in row):
        return 0

    return None

def calculate_ai_move(board):
    """Simple AI that tries to win, then tries to block the opponent, then makes a random move.
    
    Returns:
        - row, col
        - or None if the board is full
    """
    # Try to win
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                board[row][col] = 1
                if check_winner(board) == 1:
                    return row, col
                board[row][col] = None

    # Try to block the opponent
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                board[row][col] = 2
                if check_winner(board) == 2:
                    board[row][col] = 1
                    return row, col
                board[row][col] = None

    # Make a random move, start from the top left corner
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                board[row][col] = 1
                return row, col

def get_cell(frame, row, col):
    """Return the frame conntent at the given row and column of the tic tac toe board."""
    cell_size = frame.shape[0]//3
    left = int(frame.shape[1]//2-1.5*cell_size)
    right = int(frame.shape[1]//2+1.5*cell_size)
    top = int(frame.shape[0]//2-1.5*cell_size)
    bottom = int(frame.shape[0]//2+1.5*cell_size)
    return frame[top+row*cell_size:top+(row+1)*cell_size, left+col*cell_size:right+(col+1)*cell_size]