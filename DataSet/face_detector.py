import cv2

# Using a classifier to detect faces
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Opening a video file
video_file = 'V_1.mp4'
cap = cv2.VideoCapture(video_file)

# Parameters for face detection
scale_factor = 1.1
min_neighbors = 5
min_size = (30, 30)

while True:
    # Reading a frame from the video file
    ret, frame = cap.read()

    # Checking for the end of the video
    if not ret:
        break

    # Converting the frame to grayscale (for better performance)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Performing face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=scale_factor, minNeighbors=min_neighbors, minSize=min_size)

    # Drawing rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Displaying the result
    cv2.imshow('Face Detection', frame)

    # Exiting the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Releasing resources and closing windows
cap.release()
cv2.destroyAllWindows()
