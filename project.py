"""
Controls:
- Move index fingertip: move cursor
- Pinch thumb + index finger: left click
- Raise index + middle finger (with other fingers folded): right click
- Hold index + middle fingers up and move hand vertically: scroll
- Press Q in the camera window to quit

Note:
Gesture thresholds can need tuning for different hands/cameras.
"""

import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import math

# ---------- Configuration ----------
CAMERA_INDEX = 0
FRAME_REDUCTION = 100       # smaller active area = more responsive cursor
SMOOTHING = 5               # higher = smoother, but slower
CLICK_DISTANCE = 35         # pinch threshold in camera pixels
CLICK_COOLDOWN = 0.45       # seconds between clicks
SCROLL_SENSITIVITY = 3
SHOW_LANDMARKS = True

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01

screen_width, screen_height = pyautogui.size()
cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    raise RuntimeError(
        "Could not open the laptop camera. Close other camera apps and check camera permissions."
    )

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

previous_x, previous_y = 0, 0
current_x, current_y = 0, 0
last_click_time = 0.0
last_right_click_time = 0.0
previous_scroll_y = None
scroll_mode_active = False

def distance(p1, p2):
    """Euclidean distance between two (x, y) points."""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def finger_is_up(hand_landmarks, tip_id, pip_id):
    """Basic finger-up test based on vertical landmark positions."""
    return hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[pip_id].y

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.65,
    min_tracking_confidence=0.6
) as hands:

    while True:
        success, frame = cap.read()
        if not success:
            print("Could not read a frame from the camera.")
            break

        # Mirror the preview so movements feel natural.
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape

        # Active area where the hand controls the cursor.
        left = FRAME_REDUCTION
        top = FRAME_REDUCTION
        right = frame_width - FRAME_REDUCTION
        bottom = frame_height - FRAME_REDUCTION

        cv2.rectangle(frame, (left, top), (right, bottom), (80, 220, 120), 2)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        status = "Show your hand to the camera"

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]

            if SHOW_LANDMARKS:
                mp_drawing.draw_landmarks(
                    frame, hand, mp_hands.HAND_CONNECTIONS
                )

            landmarks = hand.landmark

            # Pixel coordinates for fingertip landmarks.
            index_tip = (
                int(landmarks[8].x * frame_width),
                int(landmarks[8].y * frame_height)
            )
            thumb_tip = (
                int(landmarks[4].x * frame_width),
                int(landmarks[4].y * frame_height)
            )
            middle_tip = (
                int(landmarks[12].x * frame_width),
                int(landmarks[12].y * frame_height)
            )

            # Cursor movement: index fingertip mapped to screen coordinates.
            if left < index_tip[0] < right and top < index_tip[1] < bottom:
                mapped_x = np.interp(
                    index_tip[0], (left, right), (0, screen_width - 1)
                )
                mapped_y = np.interp(
                    index_tip[1], (top, bottom), (0, screen_height - 1)
                )

                current_x = previous_x + (mapped_x - previous_x) / SMOOTHING
                current_y = previous_y + (mapped_y - previous_y) / SMOOTHING

                pyautogui.moveTo(int(current_x), int(current_y))
                previous_x, previous_y = current_x, current_y
                status = "Cursor moving"

            # Left-click: thumb and index fingertips close together.
            pinch_distance = distance(thumb_tip, index_tip)
            now = time.time()
            if pinch_distance < CLICK_DISTANCE and now - last_click_time > CLICK_COOLDOWN:
                pyautogui.click()
                last_click_time = now
                status = "LEFT CLICK"

            # Finger states. Landmark ids: index tip 8/PIP 6; middle 12/PIP 10;
            # ring 16/PIP 14; pinky 20/PIP 18.
            index_up = finger_is_up(hand, 8, 6)
            middle_up = finger_is_up(hand, 12, 10)
            ring_up = finger_is_up(hand, 16, 14)
            pinky_up = finger_is_up(hand, 20, 18)

            # Right-click: pinch thumb and middle fingertip together.
            right_pinch_distance = distance(thumb_tip, middle_tip)
            if right_pinch_distance < CLICK_DISTANCE and now - last_right_click_time > CLICK_COOLDOWN:
                pyautogui.rightClick()
                last_right_click_time = now
                status = "RIGHT CLICK"

            # Scroll mode: raise index + middle fingers, then move hand vertically.
            two_fingers_up = index_up and middle_up and not ring_up and not pinky_up
            if two_fingers_up and pinch_distance >= CLICK_DISTANCE and right_pinch_distance >= CLICK_DISTANCE:
                hand_y = int((landmarks[9].y) * frame_height)
                if previous_scroll_y is not None:
                    delta_y = previous_scroll_y - hand_y
                    if abs(delta_y) > 8:
                        amount = int(np.clip(delta_y / 8, -SCROLL_SENSITIVITY, SCROLL_SENSITIVITY))
                        pyautogui.scroll(amount)
                        status = "SCROLL UP" if amount > 0 else "SCROLL DOWN"
                previous_scroll_y = hand_y
                scroll_mode_active = True
            else:
                previous_scroll_y = None
                scroll_mode_active = False

            cv2.circle(frame, index_tip, 10, (0, 255, 255), cv2.FILLED)
            cv2.circle(frame, thumb_tip, 8, (255, 100, 0), cv2.FILLED)

            cv2.putText(
                frame, f"Pinch distance: {int(pinch_distance)}",
                (10, frame_height - 45), cv2.FONT_HERSHEY_SIMPLEX,
                0.55, (255, 255, 255), 2
            )

        cv2.putText(
            frame, status, (10, 35), cv2.FONT_HERSHEY_SIMPLEX,
            0.75, (0, 255, 255), 2
        )
        cv2.putText(
            frame, "Q = Quit", (10, 65), cv2.FONT_HERSHEY_SIMPLEX,
            0.55, (255, 255, 255), 1
        )

        cv2.imshow("AI Hand Gesture Virtual Mouse", frame)

        # Press Q while the camera window is active to exit.
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
