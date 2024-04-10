import cv2
from matplotlib import pyplot as plt
import numpy as np


def image_read(FileIm):
    image = cv2.imread(FileIm)
    plt.imshow(image)
    plt.show()
    return image


def kmeans_clustering(image):
    # Перетворення кольорового простору BGR в RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Перетворення масиву пікселів в одномірний масив
    pixel_values = image_rgb.reshape((-1, 3))

    # Кластеризація методом K-Means
    k = 3  # Кількість кластерів
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(np.float32(pixel_values), k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Конвертування центрів кластерів в цілочисельний тип та перетворення їх в формат BGR
    centers = np.uint8(centers)
    segmented_image = centers[labels.flatten()]

    # Перетворення зображення знову у форму вихідного розміру
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
        # Обчислення площі контуру
        area = cv2.contourArea(c)

        # Відкидання контурів з невеликою площею
        if area < 100:
            continue

        # Отримання координат прямокутника, обмежуючого контур
        x, y, w, h = cv2.boundingRect(c)

        # Відкидання прямокутників, які мають відносно великий відносний розмір
        if w > 3 * h:
            continue

        # Малювання контуру
        cv2.drawContours(image_entrance, [c], -1, (0, 255, 0), 2)

    cv2.imwrite(file_name, image_entrance)
    plt.imshow(cv2.cvtColor(image_entrance, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    # Зчитування та відображення вхідного зображення
    image_entrance = image_read("output_image1.jpg")

    # Кластеризація зображення
    clustered_image = kmeans_clustering(image_entrance)

    # Відображення результатів кластеризації
    plt.imshow(clustered_image)
    plt.title("Результат кластеризації")
    plt.axis('off')
    plt.show()

    # Обробка зображення
    image_exit = image_processing(clustered_image)

    # Відображення результатів сегментації
    plt.imshow(image_exit, cmap='gray')
    plt.title("Результат сегментації")
    plt.axis('off')
    plt.show()

    # Знаходження контурів
    image_cont = image_contours(image_exit)

    # Розпізнавання та відображення об'єктів
    image_recognition(clustered_image.copy(), image_cont, "image_recognition.jpg")

