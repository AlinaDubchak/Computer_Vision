import cv2
from matplotlib import pyplot as plt
import numpy as np

def image_read(FileIm):
    image = cv2.imread(FileIm)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()
    return image

# Image Segmentation
def image_processing(image):
    # Applying filters to improve image quality
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

    # Selecting parameters for Canny edge detection
    low_threshold = 50
    high_threshold = 150
    edged = cv2.Canny(gray, low_threshold, high_threshold)

    plt.imshow(edged, cmap='gray')
    plt.axis('off')
    plt.show()
    return edged

# Image Clustering
def kmeans_clustering(image):
    k = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    pixels = image.reshape((-1, 3))
    _, labels, centers = cv2.kmeans(np.float32(pixels), k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    clustered_image = centers[labels.flatten()]
    clustered_image = clustered_image.reshape(image.shape)
    return clustered_image, labels

def image_contours(image_entrance):
    # Applying parameters to find contours
    contours, _ = cv2.findContours(image_entrance.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def image_recognition(image_entrance, image_cont, file_name):
    total = 0
    for c in image_cont:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.05 * peri, True)  # Changed epsilon coefficient
        if len(approx) == 4:  # Checking if contour is a rectangle
            x, y, w, h = cv2.boundingRect(approx)
            if w > 30 and h > 30:  # Adjusting object size parameters
                area = cv2.contourArea(c)
                image_area = image_entrance.shape[0] * image_entrance.shape[1]
                if area / image_area < 0.9:  # Checking object area ratio to total image area
                    cv2.rectangle(image_entrance, (x, y), (x + w, y + h), (0, 255, 0), 4)
                    cv2.putText(image_entrance, 'Rectangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    total += 1
    print("Found {0} segment(s) of rectangular objects".format(total))
    cv2.imwrite(file_name, image_entrance)
    plt.imshow(cv2.cvtColor(image_entrance, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

def find_keypoints_and_descriptors(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Descriptor initialization
    orb = cv2.ORB_create()

    # Finding keypoints and their descriptors
    keypoints, descriptors = orb.detectAndCompute(gray, None)

    return keypoints, descriptors

def match_keypoints(descriptors1, descriptors2):
    # Initializing BFMatcher with default settings
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Finding best matches between descriptors
    matches = bf.match(descriptors1, descriptors2)

    # Sorting matches by distance
    matches = sorted(matches, key=lambda x: x.distance)

    return matches

def draw_matches(image1, image2, keypoints1, keypoints2, matches):
    # Displaying matches between keypoints on images
    matched_image = cv2.drawMatches(image1, keypoints1, image2, keypoints2, matches, None,
                                    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    plt.imshow(cv2.cvtColor(matched_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

def calculate_matching_probability(matches, keypoints1, keypoints2):
    # Calculate total number of keypoints in both images
    total_keypoints = len(keypoints1) + len(keypoints2)

    # Calculate matching probability
    matching_probability = (len(matches) / total_keypoints) * 100

    return matching_probability

if __name__ == '__main__':
    # Clustering image
    image_entrance = image_read("img_correction/output_image.jpg")
    # Image quality enhancement and processing
    image_exit = image_processing(image_entrance)
    # Getting clustering results and labels
    clustered_image, labels = kmeans_clustering(image_exit)
    # Displaying clustering results
    plt.imshow(clustered_image)
    plt.axis('off')
    plt.title("Clustering Result")
    plt.show()

    # Getting image contours
    image_cont = image_contours(image_exit)
    # Object recognition and drawing on the image
    image_recognition(image_entrance.copy(), image_cont, "img_identification/image_recognition.jpg")

    # Displaying segmented image result
    plt.imshow(cv2.cvtColor(clustered_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title("Segmentation Result")
    plt.show()

    # Reading images
    image1 = cv2.imread("img_correction/output_image.jpg")
    image2 = cv2.imread("img_correction/output_image3.jpg")

    # Finding keypoints and descriptors for both images
    keypoints1, descriptors1 = find_keypoints_and_descriptors(image1)
    keypoints2, descriptors2 = find_keypoints_and_descriptors(image2)

    # Comparing descriptors
    matches = match_keypoints(descriptors1, descriptors2)

    # Displaying matches between keypoints on images
    draw_matches(image1, image2, keypoints1, keypoints2, matches)

    # Saving result to file
    matched_image = cv2.drawMatches(image1, keypoints1, image2, keypoints2, matches, None,
                                    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv2.imwrite("img_identification/matched_image.jpg", matched_image)

    # Calculate matching probability
    matching_probability = calculate_matching_probability(matches, keypoints1, keypoints2)
    print("Matching Probability:", matching_probability, "%")