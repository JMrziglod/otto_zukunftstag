import cv2


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

while True:
    # Read the current frame from the webcam
    ret, frame = cap.read()

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

    # Display the frame
    cv2.imshow('Webcam', frame)

    # Check for the 'q' key to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close the window
cap.release()
cv2.destroyAllWindows()