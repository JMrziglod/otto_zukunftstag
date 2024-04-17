import cv2

from game import TicTacToe

# Create a VideoCapture object to capture video from the webcam
cap = cv2.VideoCapture(0)

# Most of the logic is in the TicTacToe class
game = TicTacToe()

while True:
    # quit the game
    key = cv2.waitKey(1) % 256
    if key == ord('q'):
        break

    # Read the current frame from the webcam
    ret, frame = cap.read()

    # update the game state
    game.update(frame, key)

    # Display the frame
    cv2.imshow('Tic Tac Toe', frame)

# Release the VideoCapture object and close the window
cap.release()
cv2.destroyAllWindows()