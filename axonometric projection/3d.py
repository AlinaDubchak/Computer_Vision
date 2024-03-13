from graphics import *
import numpy as np
import math as mt

# Coordinates of the vertices of a triangular pyramid
Pyramid = np.array([[50, 50, 0, 1],
                    [150, 350, 0, 1],
                    [350, 150, 0, 1],
                    [250, 250, 300, 1],
                    [250, 200, 150, 1]])  # Rows

# Function for axonometric projection
def AxonometricProjection(Figure, angle):
    theta = np.radians(angle)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    # Matrix for axonometric projection
    axonometric_matrix = np.array([[cos_theta, -sin_theta],
                                    [sin_theta, cos_theta]])
    return Figure.dot(axonometric_matrix)

# Updated function for projecting onto xy for the pyramid
def ProjectXY(Figure):
    f = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]])
    ft = f.T
    Prxy = Figure.dot(ft)
    # Keep only the first two coordinates representing the xy plane
    return Prxy[:, :2]

def PyramidWiz(win, vertices):
    obj = Polygon(Point(vertices[0, 0], vertices[0, 1]),
                  Point(vertices[1, 0], vertices[1, 1]),
                  Point(vertices[2, 0], vertices[2, 1]))
    obj.setFill('cyan')
    obj.draw(win)

win1 = GraphWin("Axonometric projection on xy", 400, 400)
win1.setBackground('white')

Prxy = ProjectXY(Pyramid)
PyramidWiz(win1, Prxy)

Prxy_axonometric = AxonometricProjection(Prxy, 45)

win1.getMouse()
win1.close()

# Coordinates of the pyramid vertices with a triangular base
Pyramid = np.array([[50, 50, 0, 1],
                    [150, 350, 0, 1],
                    [350, 150, 0, 1],
                    [250, 250, 300, 1],
                    [250, 200, 150, 1]])

# Function for projection onto xy, z=0
def ProjectXY(Figure):
    f = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]])
    ft = f.T
    Prxy = Figure.dot(ft)
    return Prxy

# Function for building a pyramid
def PyramidWiz(win, Prxy, color, outline_color):
    Ax = Prxy[0, 0]
    Ay = Prxy[0, 1]
    Bx = Prxy[1, 0]
    By = Prxy[1, 1]
    Cx = Prxy[2, 0]
    Cy = Prxy[2, 1]
    Dx = Prxy[3, 0]
    Dy = Prxy[3, 1]
    Ex = Prxy[4, 0]
    Ey = Prxy[4, 1]

    obj = Polygon(Point(Ax, Ay), Point(Bx, By), Point(Dx, Dy))
    obj.setFill(color)
    obj.setOutline(outline_color)
    obj.draw(win)
    obj = Polygon(Point(Bx, By), Point(Cx, Cy), Point(Dx, Dy))
    obj.setFill(color)
    obj.setOutline(outline_color)
    obj.draw(win)
    obj = Polygon(Point(Cx, Cy), Point(Ax, Ay), Point(Dx, Dy))
    obj.setFill(color)
    obj.setOutline(outline_color)
    obj.draw(win)
    obj = Polygon(Point(Ax, Ay), Point(Cx, Cy), Point(Ex, Ey))
    obj.setFill(color)
    obj.setOutline(outline_color)
    obj.draw(win)
    obj = Polygon(Point(Bx, By), Point(Cx, Cy), Point(Ex, Ey))
    obj.setFill(color)
    obj.setOutline(outline_color)
    obj.draw(win)
    obj = Polygon(Point(Bx, By), Point(Ax, Ay), Point(Ex, Ey))
    obj.setFill(color)
    obj.setOutline(outline_color)
    obj.draw(win)
    return obj

win2 = GraphWin("Pyramid with a triangular base", 400, 400)
win2.setBackground('white')

angle = 0
colors = ['#FFB6C1', '#87CEFA', '#F08080', '#90EE90', '#D3D3D3', '#FFD700', '#C0C0C0', '#FFFFE0', '#F0E68C', '#AFEEEE']
dark_colors = [
    "#A9A9A9",
    "#654321",
    "#00008B",
    "#006400",
    "#8B0000",
    "#9400D3",
    "#7B68EE",
    "#FFBF00",
    "#556B2F",
    "#2F4F4F"
]
def updateColor(index):
    return colors[index % len(colors)]

def updateOutlineColor(index):
    return dark_colors[index % len(dark_colors)]

while not win2.checkMouse():
    Prxy = ProjectXY(Pyramid.dot(np.array([[mt.cos(mt.radians(angle)), -mt.sin(mt.radians(angle)), 0, 0],
                                           [mt.sin(mt.radians(angle)), mt.cos(mt.radians(angle)), 0, 0],
                                           [0, 0, 1, 0],
                                           [0, 0, 0, 1]])))


    for item in win2.items[:]:
        item.undraw()

    PyramidWiz(win2, Prxy, updateColor(angle), updateOutlineColor(angle))

    angle += 1

    angle = angle % 360

    time.sleep(0.05)

win2.close()
