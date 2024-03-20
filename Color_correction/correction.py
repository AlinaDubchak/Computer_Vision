from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

FILE_NAME_START = 'owl.jpg'
FILE_NAME_STOP = 'stop.jpg'


def read_image(file_name: str) -> Image:
    try:
        image = Image.open(file_name)
        return image
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return None


def save_image(image: Image, file_name: str) -> None:
    try:
        image.save(file_name, "JPEG")
        print(f"Image saved as '{file_name}'")
    except Exception as e:
        print(f"Error occurred while saving image: {e}")


def apply_shades_of_gray(image: Image) -> Image:
    width, height = image.size
    gray_image = Image.new('L', (width, height))

    # Loop through each pixel in the image
    for x in range(width):
        for y in range(height):
            # Get the RGB values of the current pixel
            r, g, b = image.getpixel((x, y))

            # Calculate the grayscale value using the formula: 0.299 * R + 0.587 * G + 0.114 * B
            gray_value = int(0.299 * r + 0.587 * g + 0.114 * b)

            # Set the grayscale value as the new color of the pixel in the gray-scale image
            gray_image.putpixel((x, y), gray_value)

    return gray_image


def negative(image: Image, file_name_stop: str) -> None:
    draw = ImageDraw.Draw(image)
    width, height = image.size
    pix = image.load()

    # Loop through each pixel in the image
    for i in range(width):
        for j in range(height):
            # Get the RGB values of the current pixel
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            # Calculate the inverted RGB values and set them as the new color of the pixel
            draw.point((i, j), (255 - a, 255 - b, 255 - c))

    plt.imshow(image)
    plt.show()
    print("STOP_im", "red=", pix[1, 1][0], "green=", pix[1, 1][1], "blue=", pix[1, 1][2])
    image.save(file_name_stop, "JPEG")
    del draw


def sepia_gradient(image: Image, file_name_stop: str, mode: int) -> None:
    width, height = image.size
    draw = ImageDraw.Draw(image)
    pix = image.load()

    if mode == 2:
        depth_center = int(input('Depth at center (0 to 100): '))
        depth_edge = int(input('Depth at edge (0 to 100): '))
    elif mode == 3:
        depth_edge = int(input('Depth at edge (0 to 100): '))
        depth_center = int(input('Depth at center (0 to 100): '))
    elif mode == 4:
        depth_top_left = int(input('Depth at top-left (0 to 100): '))
        depth_bottom_right = int(input('Depth at bottom-right (0 to 100): '))
    elif mode == 5:
        depth_top_right = int(input('Depth at top-right (0 to 100): '))
        depth_bottom_left = int(input('Depth at bottom-left (0 to 100): '))
    else:
        print("Invalid mode. Please choose mode 2, 3, 4 or 5.")
        return

    for i in range(width):
        for j in range(height):
            if mode == 2:  # Mode 2: Gradient from center to edge
                distance_to_center_x = abs(i - width // 2)
                distance_to_center_y = abs(j - height // 2)
                distance_to_center = (distance_to_center_x ** 2 + distance_to_center_y ** 2) ** 0.5
                depth = depth_center + (depth_edge - depth_center) * (distance_to_center / (width // 2))

            elif mode == 3:  # Mode 3: Gradient from edge to center
                distance_to_center_x = abs(i - width // 2)
                distance_to_center_y = abs(j - height // 2)
                distance_to_center = (distance_to_center_x ** 2 + distance_to_center_y ** 2) ** 0.5
                depth = depth_center + (depth_edge - depth_center) * (1 - distance_to_center / (width // 2))

            elif mode == 4:  # Mode 4: Gradient from top-left to bottom-right
                diagonal_distance = (i ** 2 + j ** 2) ** 0.5
                depth = depth_top_left + (depth_bottom_right - depth_top_left) * (
                        diagonal_distance / ((width ** 2 + height ** 2) ** 0.5))

            elif mode == 5:  # Mode 5: Gradient from top-right to bottom-left
                diagonal_distance = ((width - i) ** 2 + j ** 2) ** 0.5
                depth = depth_top_right + (depth_bottom_left - depth_top_right) * (
                        diagonal_distance / ((width ** 2 + height ** 2) ** 0.5))

            else:
                print("Invalid mode. Please choose mode 2, 3, 4 or 5.")
                return

            depth = min(100, max(0, depth))

            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]

            S = (a + b + c) // 3
            a = S + depth * 2
            b = S + depth
            c = S

            if a > 255:
                a = 255
            if b > 255:
                b = 255
            if c > 255:
                c = 255

            draw.point((i, j), (int(a), int(b), int(c)))

    plt.imshow(image)
    plt.show()
    print("STOP_im", "red=", pix[1, 1][0], "green=", pix[1, 1][1], "blue=", pix[1, 1][2])
    image.save(file_name_stop, "JPEG")
    del draw


def main():
    print('Choose type of transformation:')
    print('0 - Shades of Gray')
    print('1 - Negative')
    print('2 - Sepia gradient from center to edges')
    print('3 - Sepia gradient from edges to center')
    print('4 - Sepia gradient from top-left to bottom-right')
    print('5 - Sepia gradient from top-right to bottom-left')

    mode = int(input('Mode: '))
    if mode == 0:
        original_image = read_image(FILE_NAME_START)
        if original_image:
            gray_image = apply_shades_of_gray(original_image)
            plt.imshow(gray_image, cmap='gray')
            plt.show()
            save_image(gray_image, FILE_NAME_STOP)
    elif mode == 1:
        original_image = read_image(FILE_NAME_START)
        if original_image:
            negative(original_image, FILE_NAME_STOP)
    elif mode in [2, 3, 4, 5]:
        original_image = read_image(FILE_NAME_START)
        if original_image:
            sepia_gradient(original_image, FILE_NAME_STOP, mode)
    else:
        print("Invalid mode. Please choose a mode between 0 and 5.")


if __name__ == "__main__":
    main()
