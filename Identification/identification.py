import cv2
import numpy as np

# Function to enhance contrast
def enhance_contrast(frame, alpha=1.5, beta=50):
    enhanced_frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
    return enhanced_frame

# Function for image processing
def image_processing(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply histogram equalization
    equalized_gray = cv2.equalizeHist(gray)

    gray_blur = cv2.GaussianBlur(equalized_gray, (3, 3), 0)
    edged = cv2.Canny(gray_blur, 10, 250)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    return closed

# Function to find and filter contours
def image_contours(image_entrance, min_contour_area=1000):
    cnts, _ = cv2.findContours(image_entrance.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_cnts = [cnt for cnt in cnts if cv2.contourArea(cnt) > min_contour_area]
    return filtered_cnts

# Function for image recognition
def image_recognition(image_entrance, image_cont):
    total = 0
    for c in image_cont:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.05 * peri, True)  # Approximate the contour with less vertices
        if len(approx) >= 4:
            cv2.drawContours(image_entrance, [approx], -1, (0, 255, 0), 4)  # Draw the contour on the input image
            total += 1
    return total, image_entrance

# Function to display histogram
def display_histogram(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Calculate the histogram
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist /= hist.sum()  # Normalize histogram

    hist_image = np.zeros((400, 512, 3), dtype=np.uint8)
    for i in range(256):
        cv2.line(hist_image, (i * 2, 400), (i * 2, 400 - int(hist[i] * 400)), (255, 255, 255))

    cv2.imshow('Histogram', hist_image)

# Function to process video
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Failed to open video.")
        return

    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Video', 800, 600)

    cv2.namedWindow('Histogram', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Histogram', 512, 400)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video or error while reading.")
            break

        enhanced_frame = enhance_contrast(frame)

        # Process the frame for object detection
        processed_frame = image_processing(enhanced_frame)

        # Find and filter contours in the processed frame
        contours = image_contours(processed_frame)

        # Recognize objects and count them
        count, recognized_frame = image_recognition(frame, contours)

        cv2.putText(recognized_frame, f"Number of buildings: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow('Video', recognized_frame)

        display_histogram(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    video_path = 'house.mp4'
    process_video(video_path)
