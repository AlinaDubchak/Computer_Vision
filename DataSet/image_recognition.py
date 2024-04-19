import cv2
from matplotlib import pyplot as plt
import numpy as np

def image_read(FileIm):
    image = cv2.imread(FileIm)
    plt.imshow(image)
    plt.show()
    return image

def kmeans_clustering(image):
    # Convert color space from BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convert pixel array to one-dimensional array
    pixel_values = image_rgb.reshape((-1, 3))

    # K-Means clustering
    k = 3  # Number of clusters
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(np.float32(pixel_values), k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert cluster centers to integer type and transform them to BGR format
    centers = np.uint8(centers)
    segmented_image = centers[labels.flatten()]

    # Convert image back to original shape
    segmented_image = segmented_image.reshape(image_rgb.shape)

    return segmented_image

def image_processing(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    sharpened = cv2.addWeighted(gray, 1.5, blurred, -0.5, 0)
    _, thresh = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    return closed

def image_processing_window(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(gray, 10, 250)
    plt.imshow(edged)
    plt.show()
    return edged

def image_contours(image_entrance):
    cnts = cv2.findContours(image_entrance.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    return cnts

def image_recognition(image_entrance, image_cont, file_name):
    for c in image_cont:
        # Calculate contour area
        area = cv2.contourArea(c)

        # Discard contours with small area
        if area < 100:
            continue

        # Get coordinates of the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(c)

        # Discard rectangles with relatively large aspect ratio
        if w > 3 * h:
            continue

        # Draw contour
        cv2.drawContours(image_entrance, [c], -1, (0, 255, 0), 2)

    cv2.imwrite(file_name, image_entrance)
    plt.imshow(cv2.cvtColor(image_entrance, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

def find_keypoints_and_descriptors(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Initialize descriptor
    orb = cv2.ORB_create()

    # Find keypoints and their descriptors
    keypoints, descriptors = orb.detectAndCompute(gray, None)

    return keypoints, descriptors

def match_keypoints(descriptors1, descriptors2):
    # Initialize BFMatcher with default settings
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Find best matches between descriptors
    matches = bf.match(descriptors1, descriptors2)

    # Sort matches by distance
    matches = sorted(matches, key=lambda x: x.distance)

    return matches

def draw_matches(image1, image2, keypoints1, keypoints2, matches):
    # Display matches between keypoints on images
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
    # Read and display the first input image
    image_entrance1 = image_read("img_correction/output_image1.jpg")

    # Cluster the first image
    clustered_image1 = kmeans_clustering(image_entrance1)

    # Display the clustering results of the first image
    plt.imshow(clustered_image1)
    plt.title("Clustering Result (Image 1)")
    plt.axis('off')
    plt.show()

    # Process the first image
    image_exit1 = image_processing(clustered_image1)

    # Display the segmentation results of the first image
    plt.imshow(image_exit1, cmap='gray')
    plt.title("Segmentation Result (Image 1)")
    plt.axis('off')
    plt.show()

    # Find contours for the first image
    image_cont1 = image_contours(image_exit1)

    # Recognize and display objects for the first image
    image_recognition(clustered_image1.copy(), image_cont1, "img_identification/image_recognition1.jpg")

    # Read and display the second input image
    image_entrance2 = image_read("img_correction/output_image2.jpg")

    # Cluster the second image
    clustered_image2 = kmeans_clustering(image_entrance2)

    # Display the clustering results of the second image
    plt.imshow(clustered_image2)
    plt.title("Clustering Result (Image 2)")
    plt.axis('off')
    plt.show()

    # Process the second image
    image_exit2 = image_processing(clustered_image2)

    # Display the segmentation results of the second image
    plt.imshow(image_exit2, cmap='gray')
    plt.title("Segmentation Result (Image 2)")
    plt.axis('off')
    plt.show()

    # Find contours for the second image
    image_cont2 = image_contours(image_exit2)

    # Recognize and display objects for the second image
    image_recognition(clustered_image2.copy(), image_cont2, "img_identification/image_recognition2.jpg")

    # Find keypoints and descriptors for both images
    keypoints1, descriptors1 = find_keypoints_and_descriptors(clustered_image1)
    keypoints2, descriptors2 = find_keypoints_and_descriptors(clustered_image2)

    # Compare descriptors
    matches = match_keypoints(descriptors1, descriptors2)

    # Display matches between keypoints on images
    draw_matches(clustered_image1, clustered_image2, keypoints1, keypoints2, matches)

    # Save the result to a file
    matched_image = cv2.drawMatches(clustered_image1, keypoints1, clustered_image2, keypoints2, matches, None,
                                    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv2.imwrite("img_identification/matched_image.jpg", matched_image)

    # Calculate matching probability
    matching_probability = calculate_matching_probability(matches, keypoints1, keypoints2)
    print("Matching Probability:", matching_probability, "%")