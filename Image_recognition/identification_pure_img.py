import cv2
from matplotlib import pyplot as plt
import numpy as np

def image_read(FileIm):
    image = cv2.imread(FileIm)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()
    return image


# Сегментація зображення
def image_processing(image):
    # Застосування фільтрів для поліпшення якості зображення
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

    # Вибір параметрів для Canny edge detection
    low_threshold = 50
    high_threshold = 150
    edged = cv2.Canny(gray, low_threshold, high_threshold)

    plt.imshow(edged, cmap='gray')
    plt.axis('off')
    plt.show()
    return edged


# Кластеризація зображення
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
    # Застосування параметрів для знаходження контурів
    contours, _ = cv2.findContours(image_entrance.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def image_recognition(image_entrance, image_cont, file_name):
    total = 0
    for c in image_cont:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.05 * peri, True)  # Змінено коефіцієнт epsilon
        if len(approx) == 4:  # Перевірка, чи контур - це прямокутник
            x, y, w, h = cv2.boundingRect(approx)
            if w > 30 and h > 30:  # Виправлення параметрів розміру об'єктів
                area = cv2.contourArea(c)
                image_area = image_entrance.shape[0] * image_entrance.shape[1]
                if area / image_area < 0.9:  # Перевірка відношення площі об'єкта до загальної площі зображення
                    cv2.rectangle(image_entrance, (x, y), (x + w, y + h), (0, 255, 0), 4)
                    cv2.putText(image_entrance, 'Rectangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    total += 1
    print("Знайдено {0} сегмент(а) прямокутних об'єктів".format(total))
    cv2.imwrite(file_name, image_entrance)
    plt.imshow(cv2.cvtColor(image_entrance, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    # Зображення, що кластеризується
    image_entrance = image_read("output_image.jpg")
    # Поліпшення якості та обробка зображення
    image_exit = image_processing(image_entrance)
    # Отримання результатів кластеризації та міток
    clustered_image, labels = kmeans_clustering(image_exit)
    # Відображення результатів кластеризації
    plt.imshow(clustered_image)
    plt.axis('off')
    plt.title("Результат кластеризації")
    plt.show()

    # Отримання контурів зображення
    image_cont = image_contours(image_exit)
    # Розпізнавання об'єктів та малювання їх на зображенні
    image_recognition(image_entrance.copy(), image_cont, "image_recognition.jpg")

    # Виведення зображення результату сегментації
    plt.imshow(cv2.cvtColor(clustered_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title("Результат сегментації")
    plt.show()
