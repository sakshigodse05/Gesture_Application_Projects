import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

def run_zoom_gesture():
    cap = cv2.VideoCapture(0)
    zoom_factor = 1.0  # Initial zoom level

    def calculate_distance(p1, p2):
        """Calculate Euclidean distance between two points"""
        return np.linalg.norm(np.array(p1) - np.array(p2))

    # Create a full-screen window
    cv2.namedWindow("Hand Gesture Zoom", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Hand Gesture Zoom", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get thumb & index finger tip positions
                thumb_tip = hand_landmarks.landmark[4]
                index_tip = hand_landmarks.landmark[8]

                # Convert to pixel coordinates
                thumb_pos = (int(thumb_tip.x * w), int(thumb_tip.y * h))
                index_pos = (int(index_tip.x * w), int(index_tip.y * h))

                # Calculate distance
                distance = calculate_distance(thumb_pos, index_pos)

                # Adjust zoom based on pinch gesture
                if distance < 50:  # Pinched (Zoom In)
                    zoom_factor = min(2.0, zoom_factor + 0.05)
                elif distance > 150:  # Fingers Apart (Zoom Out)
                    zoom_factor = max(1.0, zoom_factor - 0.05)

        # Apply zoom
        new_w, new_h = int(w / zoom_factor), int(h / zoom_factor)
        x1, y1 = (w - new_w) // 2, (h - new_h) // 2
        zoomed_frame = frame[y1:y1 + new_h, x1:x1 + new_w]
        zoomed_frame = cv2.resize(zoomed_frame, (w, h))

        cv2.putText(zoomed_frame, f"Zoom: {zoom_factor:.2f}x", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Hand Gesture Zoom", zoomed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the function
run_zoom_gesture()
