import numpy as np

def apply_color_correction(image):
    # Фільтрація кольорів
    color_filtered = cv2.bilateralFilter(image, 9, 75, 75)  # Фільтр Білатеральний
    # Зміна яскравості та контрасту
    brightness = 50
    contrast = 1.5
    bright_contrast = cv2.convertScaleAbs(color_filtered, alpha=contrast, beta=brightness)
    # Зміна чіткості зображення
    kernel_sharpening = np.array([[-1,-1,-1],
                                  [-1, 9,-1],
                                  [-1,-1,-1]])
    sharpness = cv2.filter2D(bright_contrast, -1, kernel_sharpening)
    # Збільшення чіткості зображення
    sharpened = cv2.addWeighted(sharpness, 1.5, cv2.GaussianBlur(sharpness, (0,0), 10), -0.5, 0)
    # Додавання додаткового параметру sharpness
    sharpness = cv2.addWeighted(sharpened, 1.5, sharpness, -0.5, 0)
    # Додавання більше чіткості
    enhanced_sharpness = cv2.addWeighted(sharpness, 2, cv2.GaussianBlur(sharpness, (0,0), 10), -1, 0)

    return enhanced_sharpness

import cv2

def enhance_image_quality(image_path):
    # Завантаження зображення
    image = cv2.imread(image_path)

    # Фільтрація шуму за допомогою медіанного фільтру
    image = cv2.medianBlur(image, 5)

    # Перетворення зображення на відтінки сірого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Підвищення чіткості за допомогою алгоритму утворення гістограми рівня яскравості
    enhanced_image = cv2.equalizeHist(gray_image)

    return enhanced_image

def main():
    input_image_path = 'operative.jpg'  # Шлях до вхідного зображення
    output_image_path = 'output_image.jpg'  # Шлях до вихідного зображення
    output_image_path2 = 'output_image1.jpg'  # Шлях до вихідного зображення

    # Зчитуємо вхідне зображення
    input_image = cv2.imread(input_image_path)

    # Застосовуємо кольорову корекцію
    corrected_image = apply_color_correction(input_image)
    black_white_img = enhance_image_quality('hight_picture.jpg')

    cv2.imwrite(output_image_path2, black_white_img)
    cv2.imwrite(output_image_path, corrected_image)

    print("Результат збережено в", output_image_path)

if __name__ == "__main__":
    main()
