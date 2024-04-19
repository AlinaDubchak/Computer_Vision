import numpy as np

def apply_color_correction(image):
    # Color filtering
    color_filtered = cv2.bilateralFilter(image, 9, 75, 75)  # Bilateral Filter
    # Adjusting brightness and contrast
    brightness = 50
    contrast = 1.5
    bright_contrast = cv2.convertScaleAbs(color_filtered, alpha=contrast, beta=brightness)
    # Image sharpening
    kernel_sharpening = np.array([[-1,-1,-1],
                                  [-1, 9,-1],
                                  [-1,-1,-1]])
    sharpness = cv2.filter2D(bright_contrast, -1, kernel_sharpening)
    # Increase image sharpness
    sharpened = cv2.addWeighted(sharpness, 1.5, cv2.GaussianBlur(sharpness, (0,0), 10), -0.5, 0)
    # Additional sharpness
    sharpness = cv2.addWeighted(sharpened, 1.5, sharpness, -0.5, 0)
    # More sharpness
    enhanced_sharpness = cv2.addWeighted(sharpness, 2, cv2.GaussianBlur(sharpness, (0,0), 10), -1, 0)

    return enhanced_sharpness

import cv2

def enhance_image_quality(image_path):
    # Load image
    image = cv2.imread(image_path)

    # Noise reduction using median filter
    image = cv2.medianBlur(image, 5)

    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Enhance image quality using histogram equalization
    enhanced_image = cv2.equalizeHist(gray_image)

    return enhanced_image

def main():
    input_image_path = 'img/operative.jpg'  # Path to the input image
    input_image_path2 = 'img/pure_img_2.jpg'  # Path to the input image
    output_image_path = 'img_correction/output_image.jpg'  # Path to the output image
    output_image_path4 = 'img_correction/output_image3.jpg'  # Path to the output image
    output_image_path2 = 'img_correction/output_image1.jpg'  # Path to the output image
    output_image_path3 = 'img_correction/output_image2.jpg'  # Path to the output image

    # Read input images
    input_image = cv2.imread(input_image_path)
    input_image2 = cv2.imread(input_image_path2)

    # Apply color correction
    corrected_image = apply_color_correction(input_image)
    corrected_image2 = apply_color_correction(input_image2)
    black_white_img = enhance_image_quality('img/hight_picture.jpg')
    black_white_img2 = enhance_image_quality('img/img_hight.jpg')

    cv2.imwrite(output_image_path2, black_white_img)
    cv2.imwrite(output_image_path3, black_white_img2)
    cv2.imwrite(output_image_path, corrected_image)
    cv2.imwrite(output_image_path4, corrected_image2)

    print("Result saved to", output_image_path)

if __name__ == "__main__":
    main()
