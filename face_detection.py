import cv2

# Load the pre-trained Haar Cascade model for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open webcam (0 for default webcam, 1 for external)
cap = cv2.VideoCapture(0)

# Create a named window with a resizable property
cv2.namedWindow("Face Detection", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Face Detection", 1280, 720)  # Increase window size
    
while True:
    ret, frame = cap.read()  # Capture frame
    if not ret:
        print("Error: Couldn't access webcam.")
        break

    # Convert to grayscale (Haar cascade works better on grayscale images)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Show the output
    cv2.imshow("Face Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
