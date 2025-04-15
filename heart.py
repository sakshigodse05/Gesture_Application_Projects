import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)

def is_heart_shape(landmarks):
    """Detect if fingers form a heart shape"""
    if len(landmarks) < 2:
        return False

    # Get tip positions of index fingers and thumbs
    left_index = landmarks[0][8]
    right_index = landmarks[1][8]
    left_thumb = landmarks[0][4]
    right_thumb = landmarks[1][4]

    # Calculate distances
    index_distance = np.linalg.norm(np.array(left_index) - np.array(right_index))
    thumb_distance = np.linalg.norm(np.array(left_thumb) - np.array(right_thumb))

    # Condition for heart shape
    return index_distance < 50 and thumb_distance < 50

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    hand_landmarks = []
    if result.multi_hand_landmarks:
        for hand_landmark in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)
            
            # Store finger tip coordinates
            landmarks = []
            for id, lm in enumerate(hand_landmark.landmark):
                h, w, _ = frame.shape
                landmarks.append((int(lm.x * w), int(lm.y * h)))
            hand_landmarks.append(landmarks)

    # Check for heart shape gesture
    if len(hand_landmarks) == 2 and is_heart_shape(hand_landmarks):
        cv2.putText(frame, "love u dhabbu", (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)

    cv2.imshow("Hand Gesture - Heart Shape", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
