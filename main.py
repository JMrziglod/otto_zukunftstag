import cv2
from time import time

# Create a 3x3 tic tac toe board
# There are two players: 1 and 2
board = [[None, None, None], [None, None, None], [None, None, None]]

def draw_tic_tac_toe(frame, board):
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
    return None

def ai_move(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                board[row][col] = 1
                if check_winner(board) == 1:
                    return row, col
                board[row][col] = None
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                board[row][col] = 2
                if check_winner(board) == 2:
                    board[row][col] = 1
                    return row, col
                board[row][col] = None
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                board[row][col] = 1
                return row, col

def get_cell(frame, row, col):
    """Return the cell at the given row and column of the tic tac toe board."""
    cell_size = frame.shape[0]//3
    left = int(frame.shape[1]//2-1.5*cell_size)
    right = int(frame.shape[1]//2+1.5*cell_size)
    top = int(frame.shape[0]//2-1.5*cell_size)
    bottom = int(frame.shape[0]//2+1.5*cell_size)
    return frame[top+row*cell_size:top+(row+1)*cell_size, left+col*cell_size:right+(col+1)*cell_size]

def detect_pointer(frame):
    """Detect a red area in the frame and return the row and column of the cell with the most red pixels."""
    best_red = (None, 20)

    for row in range(3):
        for col in range(3):
            cell = get_cell(frame, row, col)
            red = cell[..., 2].mean() - cell[..., :2].mean()
            if best_red[1] < red:
                best_red = (row, col), red
            
    return best_red

# Create a VideoCapture object to capture video from the webcam
cap = cv2.VideoCapture(0)
start_time = time()
waiting_for_ai = False

while True:
    # Read the current frame from the webcam
    ret, frame = cap.read()

    winner = check_winner(board)
    if winner is not None:
        cv2.putText(frame, f"Player {winner} wins!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display the frame
        cv2.imshow('Webcam', frame)

        # Check for the 'q' key to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    # Try to detect the pointer
    selected_cell = detect_pointer(frame)

    # draw a squared tic tac toe board in the center of the board:
    cell_size = frame.shape[0]//3
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

    # Highlight the selected cell
    if selected_cell[0] is not None:
        top = int(frame.shape[0]//2-1.5*cell_size)
        bottom = int(frame.shape[0]//2+1.5*cell_size)
        left = int(frame.shape[1]//2-1.5*cell_size)
        right = int(frame.shape[1]//2+1.5*cell_size)
        cv2.rectangle(frame, (left+selected_cell[0][1]*cell_size, top+selected_cell[0][0]*cell_size), (left+(selected_cell[0][1]+1)*cell_size, top+(selected_cell[0][0]+1)*cell_size), (0, 255, 0), 2)

        # countdown timer until we log in the move
        if time() - start_time > 2 and not waiting_for_ai:
            row, col = selected_cell[0]
            if board[row][col] is None:
                board[row][col] = 2
                waiting_for_ai = True
            
            start_time = time()

    else:
        start_time = time()

    if waiting_for_ai:
        row, col = ai_move(board)
        board[row][col] = 1
        waiting_for_ai = False

    draw_tic_tac_toe(frame, board)

    # Display the frame
    cv2.imshow('Webcam', frame)

    # Check for the 'q' key to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close the window
cap.release()
cv2.destroyAllWindows()