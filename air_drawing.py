import cv2
import mediapipe as mp
import numpy as np


# Mobile camera URL (my IP)
cap = cv2.VideoCapture("http://192.168.0.106:4747/video")


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils


#  Canvas
canvas = np.zeros((480, 640, 3), dtype=np.uint8)

prev_x, prev_y = 0, 0

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (640, 480))

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            h, w, c = frame.shape

            # Index finger  tip
            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)

            # Middle finger tip
            mx = int(hand_landmarks.landmark[12].x * w)
            my = int(hand_landmarks.landmark[12].y * h)

            # Draw finger point
            cv2.circle(frame, (x, y), 8, (0, 255, 0), -1)

            # ✋ Drawing condition:
            # Index up & Middle down = draw
            if y < my:
                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = x, y

                cv2.line(canvas, (prev_x, prev_y), (x, y), (255, 0, 0), 5)
                prev_x, prev_y = x, y
            else:
                prev_x, prev_y = 0, 0

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Merge  canvas + frame
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)

    frame = cv2.bitwise_and(frame, inv)
    frame = cv2.bitwise_or(frame, canvas)

    cv2.imshow("Air Drawing (Mobile Cam)", frame)

    key = cv2.waitKey(1)

    # Press 'c' to clear
    
    if key == ord('c'):
        canvas = np.zeros((480, 640, 3), dtype=np.uint8)

    # Press 'q' to quit
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()