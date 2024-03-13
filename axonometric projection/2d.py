from graphics import *
import time
import numpy as np
import math as mt

def initialize_parallelogram_coordinates(st, yw):
    x1 = st
    y1 = yw - 2 * st
    x2 = 2 * st
    y2 = yw - st
    x3 = x2 + 1.5 * st
    y3 = y2
    x4 = x1 + 1.5 * st
    y4 = y1
    return x1, y1, x2, y2, x3, y3, x4, y4

def check_boundary(xw, yw, *points):
    for x, y in zip(*[iter(points)]*2):
        if x < 0 or x > xw or y < 0 or y > yw:
            return False
    return True

# Graphic window dimensions and transformation parameters
xw = 600
yw = 600
st = 50
dx = 50
dy = 50

# Initial coordinates of the parallelogram vertices
x1, y1, x2, y2, x3, y3, x4, y4 = initialize_parallelogram_coordinates(st, yw)

win1 = GraphWin("Moving parallelogram", xw, yw)
win1.setBackground('white')


parallelogram = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3), Point(x4, y4))
parallelogram.draw(win1)

# Transformation matrix for translation
T = np.array([[1, 0, dx],
              [0, 1, -dy],
              [0, 0, 1]])

# Number of iterations for moving the parallelogram
iterations = 10

# Loop for moving and displaying the trajectory of position change
for i in range(iterations):
    time.sleep(0.3)

    points_matrix = np.array([[x1, x2, x3, x4],
                              [y1, y2, y3, y4],
                              [1, 1, 1, 1]])

    new_points_matrix = T.dot(points_matrix)

    x1, x2, x3, x4 = new_points_matrix[0]
    y1, y2, y3, y4 = new_points_matrix[1]

    if not check_boundary(xw, yw, x1, y1, x2, y2, x3, y3, x4, y4):
        break

    parallelogram.undraw()
    parallelogram = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3), Point(x4, y4))
    parallelogram.draw(win1)

win1.getMouse()
win1.close()

x1, y1, x2, y2, x3, y3, x4, y4 = initialize_parallelogram_coordinates(st, yw)

win2 = GraphWin("Moving and rotating parallelogram", xw, yw)
win2.setBackground('white')

parallelogram2 = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3), Point(x4, y4))
parallelogram2.draw(win2)

T = np.array([[1, 0, dx],
              [0, 1, -dy],
              [0, 0, 1]])

iterations = 10

TetaG = 180
TetaR = (3 / 14 * TetaG) / 180

for i in range(iterations):
    time.sleep(0.3)

    points_matrix2 = np.array([[x1, x2, x3, x4],
                               [y1, y2, y3, y4],
                               [1, 1, 1, 1]])

    new_points_matrix2 = T.dot(points_matrix2)

    x1, x2, x3, x4 = new_points_matrix2[0]
    y1, y2, y3, y4 = new_points_matrix2[1]

    if not check_boundary(xw, yw, x1, y1, x2, y2, x3, y3, x4, y4):
        break

    xc = (x1 + x2 + x3 + x4) / 4
    yc = (y1 + y2 + y3 + y4) / 4
    x1 = (x1 - xc) * mt.cos(TetaR) - (y1 - yc) * mt.sin(TetaR) + xc
    y1 = (x1 - xc) * mt.sin(TetaR) + (y1 - yc) * mt.cos(TetaR) + yc
    x2 = (x2 - xc) * mt.cos(TetaR) - (y2 - yc) * mt.sin(TetaR) + xc
    y2 = (x2 - xc) * mt.sin(TetaR) + (y2 - yc) * mt.cos(TetaR) + yc
    x3 = (x3 - xc) * mt.cos(TetaR) - (y3 - yc) * mt.sin(TetaR) + xc
    y3 = (x3 - xc) * mt.sin(TetaR) + (y3 - yc) * mt.cos(TetaR) + yc
    x4 = (x4 - xc) * mt.cos(TetaR) - (y4 - yc) * mt.sin(TetaR) + xc
    y4 = (x4 - xc) * mt.sin(TetaR) + (y4 - yc) * mt.cos(TetaR) + yc

    parallelogram2.undraw()
    parallelogram2 = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3), Point(x4, y4))
    parallelogram2.draw(win2)

win2.getMouse()
win2.close()

x1, y1, x2, y2, x3, y3, x4, y4 = initialize_parallelogram_coordinates(st, yw)

win3 = GraphWin("Scaling parallelogram", xw, yw)
win3.setBackground('white')

parallelogram3 = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3), Point(x4, y4))
parallelogram3.draw(win3)

center_x = xw / 2 - (x1 + x2 + x3 + x4) / 4
center_y = yw / 2 - (y1 + y2 + y3 + y4) / 4
parallelogram3.move(center_x, center_y)

scale_factor = 1.1
iterations = 10

for i in range(iterations):
    time.sleep(0.3)

    vertices = parallelogram3.getPoints()
    x1, y1 = vertices[0].getX(), vertices[0].getY()
    x2, y2 = vertices[1].getX(), vertices[1].getY()
    x3, y3 = vertices[2].getX(), vertices[2].getY()
    x4, y4 = vertices[3].getX(), vertices[3].getY()

    center_x = (x1 + x2 + x3 + x4) / 4
    center_y = (y1 + y2 + y3 + y4) / 4

    # Scaling each vertex with respect to the center
    x1 = center_x + (x1 - center_x) * scale_factor
    y1 = center_y + (y1 - center_y) * scale_factor
    x2 = center_x + (x2 - center_x) * scale_factor
    y2 = center_y + (y2 - center_y) * scale_factor
    x3 = center_x + (x3 - center_x) * scale_factor
    y3 = center_y + (y3 - center_y) * scale_factor
    x4 = center_x + (x4 - center_x) * scale_factor
    y4 = center_y + (y4 - center_y) * scale_factor

    parallelogram3.undraw()
    parallelogram3 = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3), Point(x4, y4))
    parallelogram3.draw(win3)

win3.getMouse()
win3.close()
