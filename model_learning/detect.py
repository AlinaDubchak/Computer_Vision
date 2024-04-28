import cv2
import numpy as np
import tensorflow as tf

# Load the trained model
model = tf.keras.models.load_model("eyes_detection_model.h5")

target_size = (100, 100)

cap = cv2.VideoCapture("video.mp4")

while True:
    ret, frame = cap.read()

    # Check if frame is obtained
    if not ret:
        break

    resized_frame = cv2.resize(frame, target_size)

    # Expand the dimensions of the frame (add batch dimension)
    input_frame = np.expand_dims(resized_frame, axis=0)

    # Normalize pixel values
    input_frame = input_frame / 255.0

    # Predict using the loaded model
    prediction = model.predict(input_frame)

    # Display the prediction on the frame
    if prediction[0][0] > 0.5:
        cv2.putText(frame, "Open Eyes", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Closed Eyes", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Video", frame)

cap.release()
cv2.destroyAllWindows()
