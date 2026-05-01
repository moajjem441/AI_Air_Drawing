# import cv2
# import mediapipe as mp
# import numpy as np

# # Camera (mobile)
# cap = cv2.VideoCapture("http://192.168.0.106:4747/video")

# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
# draw_utils = mp.solutions.drawing_utils

# canvas = np.zeros((480, 640, 3), dtype=np.uint8)

# prev_x, prev_y = 0, 0

# color = (255, 0, 0)   # default blue

# def finger_count(hand_landmarks):
#     tips = [8, 12, 16, 20]
#     count = 0
#     for tip in tips:
#         if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
#             count += 1
#     return count

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     frame = cv2.flip(frame, 1)
#     frame = cv2.resize(frame, (640, 480))

#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     result = hands.process(rgb)

#     if result.multi_hand_landmarks:
#         for hand_landmarks in result.multi_hand_landmarks:

#             h, w, _ = frame.shape

#             draw_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#             x = int(hand_landmarks.landmark[8].x * w)
#             y = int(hand_landmarks.landmark[8].y * h)

#             fingers = finger_count(hand_landmarks)

#             # ✋ FIST → ERASE MODE
#             if fingers == 0:
#                 cv2.circle(frame, (x, y), 20, (0, 0, 255), -1)
#                 canvas = np.zeros((480, 640, 3), dtype=np.uint8)
#                 prev_x, prev_y = 0, 0

#             # ☝️ DRAW MODE
#             else:
#                 cv2.circle(frame, (x, y), 8, (0, 255, 0), -1)

#                 if prev_x == 0 and prev_y == 0:
#                     prev_x, prev_y = x, y

#                 cv2.line(canvas, (prev_x, prev_y), (x, y), color, 5)

#                 prev_x, prev_y = x, y

#                 # 🎨 COLOR CHANGE
#                 if fingers == 1:
#                     color = (255, 0, 255)   # Blue
#                 elif fingers == 2:
#                     color = (0, 255, 0)   # Green
#                 elif fingers == 3:
#                     color = (0, 0, 255)   # Red

#     else:
#         prev_x, prev_y = 0, 0

#     # merge canvas + frame
#     gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
#     _, inv = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
#     inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)

#     frame = cv2.bitwise_and(frame, inv)
#     frame = cv2.bitwise_or(frame, canvas)

#     cv2.imshow("🔥 AI Air Drawing PRO", frame)

#     key = cv2.waitKey(1)

#     if key == ord('c'):
#         canvas = np.zeros((480, 640, 3), dtype=np.uint8)

#     if key == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()






import cv2
import mediapipe as mp
import numpy as np

# Camera (mobile)
cap = cv2.VideoCapture("http://192.168.0.106:4747/video")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
draw_utils = mp.solutions.drawing_utils

canvas = np.zeros((480, 640, 3), dtype=np.uint8)

prev_x, prev_y = 0, 0
color = (255, 0, 255)  # default magenta (clear visible)

def finger_count(hand_landmarks):
    tips = [8, 12, 16, 20]
    count = 0
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            count += 1
    return count

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (640, 480))

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            h, w, _ = frame.shape
            draw_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)

            fingers = finger_count(hand_landmarks)

            # ✋ FIST = pause only (NO erase)
            if fingers == 0:
                prev_x, prev_y = 0, 0
                cv2.putText(frame, "PAUSE", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # 🧽 ERASER MODE (4 fingers open)
            elif fingers == 4:
                canvas[:] = 0
                prev_x, prev_y = 0, 0
                cv2.putText(frame, "ERASING...", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # ✍️ DRAW MODE
            else:
                cv2.circle(frame, (x, y), 8, (0, 255, 0), -1)

                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = x, y

                cv2.line(canvas, (prev_x, prev_y), (x, y), color, 5)

                prev_x, prev_y = x, y

                # 🎨 COLOR CHANGE
                if fingers == 1:
                    color = (255, 0, 255)   # magenta
                elif fingers == 2:
                    color = (0, 255, 0)     # green
                elif fingers == 3:
                    color = (0, 0, 255)     # red

    else:
        prev_x, prev_y = 0, 0

    # merge canvas + frame
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)

    frame = cv2.bitwise_and(frame, inv)
    frame = cv2.bitwise_or(frame, canvas)

    cv2.imshow("🔥 AI Air Drawing PRO", frame)

    key = cv2.waitKey(1)

    if key == ord('c'):
        canvas = np.zeros((480, 640, 3), dtype=np.uint8)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()