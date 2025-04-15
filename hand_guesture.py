import cv2
import mediapipe as mp
import time
import pyttsx3  # For voice alert

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Adjust speech speed

# Load Haar cascade for eye detection
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Open webcam
cap = cv2.VideoCapture(0)  # Use 1 if external webcam

# Timer variables for hand and eye detection
last_hand_detected_time = time.time()
last_eye_open_time = time.time()
ALERT_THRESHOLD = 5  # Alert if hand or eyes are not detected for 5 seconds
alert_triggered = False  # Prevents continuous alerts

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't read frame.")
        break

    frame = cv2.flip(frame, 1)  # Flip for mirror effect
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale for eye detection
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # === Hand Detection ===
    result = hands.process(rgb_frame)
    hand_detected = False

    if result.multi_hand_landmarks:
        hand_detected = True  # Hand is detected
        last_hand_detected_time = time.time()  # Reset timer

        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # === Eye Detection ===
    eyes = eye_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    eye_detected = len(eyes) > 0  # True if at least one eye is detected

    if eye_detected:
        last_eye_open_time = time.time()  # Reset eye timer

        for (x, y, w, h) in eyes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw rectangle around eyes

    # === Alert System (No Hand or Eyes Closed) ===
    if (time.time() - last_hand_detected_time > ALERT_THRESHOLD) or (time.time() - last_eye_open_time > ALERT_THRESHOLD):
        cv2.putText(frame, "ALERT! Drowsiness Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 0, 255), 3, cv2.LINE_AA)

        if not alert_triggered:
            engine.say("Wake up! Drowsiness detected!")  # Speak alert
            engine.runAndWait()
            alert_triggered = True  # Prevent continuous speaking

    else:
        alert_triggered = False  # Reset alert if eyes and hands are detected

    # Show output
    cv2.imshow("Drowsiness Detection (Hand + Eye Tracking)", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
