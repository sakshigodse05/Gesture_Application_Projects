import cv2
import mediapipe as mp
import numpy as np
import winsound  # Beep sound
import pyttsx3
import streamlit as st
import threading

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# Initialize MediaPipe Face Mesh & Hands
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.7, min_tracking_confidence=0.7)
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# **Eye Landmark Indices (Updated for Better Accuracy)**
LEFT_EYE = [33, 160, 158, 133]  
RIGHT_EYE = [362, 385, 387, 263]

# Function to Calculate Eye Aspect Ratio (EAR)
def calculate_ear(landmarks, eye_points):
    p1 = np.array([landmarks[eye_points[1]].x, landmarks[eye_points[1]].y])
    p2 = np.array([landmarks[eye_points[2]].x, landmarks[eye_points[2]].y])
    p3 = np.array([landmarks[eye_points[0]].x, landmarks[eye_points[0]].y])
    p4 = np.array([landmarks[eye_points[3]].x, landmarks[eye_points[3]].y])
    
    vertical = np.linalg.norm(p1 - p2)  # Vertical Distance
    horizontal = np.linalg.norm(p3 - p4)  # Horizontal Distance

    return vertical / horizontal  # EAR Ratio

# Function to Generate Beep Sound
def generate_beep():
    winsound.Beep(1000, 500)

# Function for Voice Alert
def speak_alert(message):
    engine.say(message)
    engine.runAndWait()

# Streamlit UI
st.title("🚗 Driver Behavior Monitoring & Drowsiness Detection")
st.sidebar.header("Live Dashboard")
st.sidebar.write("👀 Monitoring Driver's Face & Hands")

# Open Webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # Reduce frame size (Faster)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)  # Set FPS (Reduce lag)

stframe = st.empty()
frame_count = 0  # To skip frames

drowsy_frame_threshold = 15  # Number of frames to confirm drowsiness
drowsy_counter = 0  # Count frames with eyes closed

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        st.sidebar.error("❌ Error: Couldn't read frame.")
        break

    frame = cv2.flip(frame, 1)  # Flip for mirror effect
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # **SKIP FRAMES** (Process every 2nd frame for speed)
    frame_count += 1
    if frame_count % 2 != 0:
        stframe.image(frame, channels="BGR")
        continue

    drowsy_detected = False
    gesture_detected = False

    # Detect Face and Eyes Using MediaPipe Face Mesh
    face_results = face_mesh.process(rgb_frame)

    if face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
            mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS)
            
            left_ear = calculate_ear(face_landmarks.landmark, LEFT_EYE)
            right_ear = calculate_ear(face_landmarks.landmark, RIGHT_EYE)
            avg_ear = (left_ear + right_ear) / 2  # Average EAR

            if avg_ear < 0.2:  # Adjusted EAR Threshold
                drowsy_counter += 1
            else:
                drowsy_counter = 0  # Reset if eyes open

            if drowsy_counter >= drowsy_frame_threshold:  # Confirm drowsiness
                drowsy_detected = True

    # Process Frame for Hand Detection
    hand_results = hands.process(rgb_frame)

    # Draw Hand Landmarks if Detected
    if hand_results.multi_hand_landmarks:
        gesture_detected = True
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Show Detection Status on Sidebar
    if drowsy_detected:
        st.sidebar.warning("⚠️ Drowsiness Detected!")
        threading.Thread(target=generate_beep).start()  # Run Beep in Background
        threading.Thread(target=speak_alert, args=("Alert! Wake up!",)).start()  # Voice Alert

    if gesture_detected:
        st.sidebar.success("✋ Hand Gesture Detected")

    # Show Output on Dashboard
    stframe.image(frame, channels="BGR")

    # Press 'q' to Exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release Resources
cap.release()
cv2.destroyAllWindows()
st.sidebar.info("🛑 Webcam Stopped")
