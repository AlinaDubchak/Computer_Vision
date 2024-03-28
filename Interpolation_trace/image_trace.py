from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import sys

def vector_circuit(im, threshold=170):
    fig, ax = plt.subplots()
    contour = ax.contour(im, levels=[threshold], colors='black', origin='image')
    ax.axis('equal')
    plt.show()
    return contour

def mono(image, factor):
    draw = ImageDraw.Draw(image)
    width, height = image.size

    print('--- Beginning transformation ---')
    for i in range(width):
        for j in range(height):
            r, g, b = image.getpixel((i, j))
            if r + g + b > ((255 + factor) // 2) * 3:
                r, g, b = 255, 255, 255
            else:
                r, g, b = 0, 0, 0
            draw.point((i, j), (r, g, b))

    plt.imshow(image)
    plt.show()
    image.save("output_image.jpg", "JPEG")
    del draw
    print('--- Image successfully saved ---')

if __name__ == '__main__':
    print('Choose the data source:')
    print('1 - ideal image')
    print('2 - real image')
    mode_1 = int(input('Enter mode: '))

    if mode_1 == 1:
        image = Image.open("ideal.jpeg")
        im = np.array(image.convert('L'))
        contour = vector_circuit(im)

    elif mode_1 == 2:
        image = Image.open("fruits.jpg")
        im = np.array(image.convert('L'))
        contour = vector_circuit(im)

    print('Improve image quality?')
    print('1 - yes')
    print('2 - no')
    mode = int(input('Enter mode: '))

    if mode == 1:
        factor = int(input('Enter resolution factor in the range of 50-100: '))
        mono(image, factor)
        im = np.array(image.convert('L'))
        vector_circuit(im)

    elif mode == 2:
        sys.exit()
