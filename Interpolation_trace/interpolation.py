from graphics import *
import numpy as np
import math as mt
from time import sleep

# Coordinates of the vertices of a triangular pyramid #Pyramid 1
Pyramid = np.array([[50, 50, 0, 1],
                    [150, 350, 0, 1],
                    [350, 150, 0, 1],
                    [250, 250, 300, 1],
                    [250, 200, 150, 1]])  # Rows

xw = 600  #Pyramid 2
yw = 600
st = 300

# Coordinates for the triangular base of the pyramid (ABC)
base_points = np.array([[0, 0, 0, 1],
                        [st, 0, 0, 1],
                        [st / 2, st * mt.sqrt(3) / 2, 0, 1]])

# Apex of the pyramid
apex_point = np.array([[st / 2, st / (2 * mt.sqrt(3)), st, 1]])

# Function for projection onto xy, z=0
def ProjectXY(Figure):
    f = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])  # Updated matrix for projection
    ft = f.T
    Prxy = Figure.dot(ft)
    return Prxy

# Function for building a pyramid
def PyramidWiz(win, Prxy, color):
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
    obj.draw(win)
    obj = Polygon(Point(Bx, By), Point(Cx, Cy), Point(Dx, Dy))
    obj.setFill(color)
    obj.draw(win)
    obj = Polygon(Point(Cx, Cy), Point(Ax, Ay), Point(Dx, Dy))
    obj.setFill(color)
    obj.draw(win)
    obj = Polygon(Point(Ax, Ay), Point(Cx, Cy), Point(Ex, Ey))
    obj.setFill(color)
    obj.draw(win)
    obj = Polygon(Point(Bx, By), Point(Cx, Cy), Point(Ex, Ey))
    obj.setFill(color)
    obj.draw(win)
    obj = Polygon(Point(Bx, By), Point(Ax, Ay), Point(Ex, Ey))
    obj.setFill(color)
    obj.draw(win)
    return obj

def DrawControlPoints(win, Prxy):
    for i in range(len(Prxy)):
        point = Circle(Point(Prxy[i, 0], Prxy[i, 1]), 3)
        point.setFill('red')
        point.draw(win)

# Function to calculate a point on the Bézier curve for a given parameter t
def bezier_point(t, control_points):
    n = len(control_points) - 1
    x = 0
    y = 0
    for i in range(n + 1):
        binom = mt.factorial(n) / (mt.factorial(i) * mt.factorial(n - i))
        term_x = (1 - t) ** (n - i) * t ** i * control_points[i, 0]
        term_y = (1 - t) ** (n - i) * t ** i * control_points[i, 1]
        x += binom * term_x
        y += binom * term_y
    return Point(x, y)

# Function to draw Bézier curve
def bezier_curve(win, control_points, num_segments, color):
    bezier_points = []
    for i in range(num_segments):
        t = i / (num_segments - 1)
        point = bezier_point(t, control_points)
        bezier_points.append(point)
        if i != 0:
            line = Line(bezier_points[-2], point)
            line.setWidth(2)
            line.setFill(color)
            line.draw(win)
        sleep(0.1)
    return bezier_points

# Function to draw a line between two points with a given color
def draw_line(win, point1, point2, color):
    line = Line(point1, point2)
    line.setWidth(2)
    line.setFill(color)
    line.draw(win)

# Function to calculate the normal vector of a face
def calculate_normal(face):
    v1 = face[1] - face[0]
    v2 = face[2] - face[0]
    # Calculate the components of the normal vector
    normal_x = v1[1] * v2[2] - v1[2] * v2[1]
    normal_y = v1[2] * v2[0] - v1[0] * v2[2]
    normal_z = v1[0] * v2[1] - v1[1] * v2[0]
    normal = np.array([normal_x, normal_y, normal_z])
    return normal

def is_face_visible(face, viewpoint):
    normal = calculate_normal(face)
    view_vector = viewpoint - face[0]
    return np.dot(normal, view_vector) > 0

def ShiftXYZ(Figure, l, m, n):
    f = np.array([[1, 0, 0, l], [0, 1, 0, m], [0, 0, 1, n], [1, 0, 0, 1]])  # Transformation matrix
    ft = f.T
    Prxy = Figure.dot(ft)
    return Prxy

def dimetri(Figure, TetaG1, TetaG2):
    TetaR1 = (3 / 14 * TetaG1) / 180
    TetaR2 = (3 / 14 * TetaG2) / 180
    f1 = np.array([[mt.cos(TetaR1), 0, -mt.sin(TetaR1), 0], [0, 1, 0, 0], [mt.sin(TetaR1), 0, mt.cos(TetaR1), 1],
                   [0, 0, 0, 0], ])
    ft1 = f1.T
    Prxy1 = Figure.dot(ft1)
    f2 = np.array([[1, 0, 0, 0], [0, mt.cos(TetaR2), mt.sin(TetaR2), 0],
                   [0, -mt.sin(TetaR2), mt.cos(TetaR2), 0], [0, 0, 0, 1]])
    ft2 = f2.T
    Prxy2 = Prxy1.dot(ft2)
    return Prxy2

def is_visible(vertex1, vertex2, vertex3):
    # Convert vertices to three-dimensional vectors
    v1 = vertex1[:3]
    v2 = vertex2[:3]
    v3 = vertex3[:3]

    # Calculate normal vector of the face
    vector1 = v2 - v1
    vector2 = v3 - v1
    normal = np.cross(vector1, vector2)

    # Calculate view vector (from viewer to the face)
    view_vector = np.array([0, 0, 1])  # Assuming viewer is looking along the positive z-axis

    # Check if the angle between the normal and view vector is acute
    return np.dot(normal, view_vector) >= 0


# Calculate coordinates of the base after transformation
base_points_shifted = ShiftXYZ(base_points, (xw / 2) - st / 2, (yw / 2) - st / (2 * mt.sqrt(3)), 0)

win2 = GraphWin("Pyramid Bezier", 400, 400)
win2.setBackground('white')

color = 'cyan'

Prxy = ProjectXY(Pyramid)

PyramidWiz(win2, Prxy, color)
DrawControlPoints(win2, Prxy)

# Selecting faces and determining critical points
ABE = Pyramid[[0, 1, 4]]
BCD = Pyramid[[1, 2, 4]]
CDE = Pyramid[[2, 0, 4]]

# Projecting face ABE and BCD onto the xy plane
Prxy_ABE = ProjectXY(ABE)
Prxy_BCD = ProjectXY(BCD)
Prxy_CDE = ProjectXY(CDE)

# Drawing control points on faces ABE and BCD
DrawControlPoints(win2, Prxy_ABE)
DrawControlPoints(win2, Prxy_BCD)
DrawControlPoints(win2, Prxy_CDE)

#Drawing Bezier curves on face ABE (red) and BCD (blue) and CDE (green)
bezier_curve(win2, Prxy_ABE, 20, 'red')
bezier_curve(win2, Prxy_BCD, 20, 'blue')
bezier_curve(win2, Prxy_CDE, 20, 'green')

# Drawing lines
for i in range(len(Prxy_ABE)):
    if i != len(Prxy_ABE) - 1:
        draw_line(win2, Point(Prxy_ABE[i, 0], Prxy_ABE[i, 1]), Point(Prxy_ABE[i + 1, 0], Prxy_ABE[i + 1, 1]), 'yellow')
        sleep(1.5)
    else:
        draw_line(win2, Point(Prxy_ABE[i, 0], Prxy_ABE[i, 1]), Point(Prxy_ABE[0, 0], Prxy_ABE[0, 1]), 'yellow')
        sleep(1.5)

for i in range(len(Prxy_BCD)):
    if i != len(Prxy_BCD) - 1:
        draw_line(win2, Point(Prxy_BCD[i, 0], Prxy_BCD[i, 1]), Point(Prxy_BCD[i + 1, 0], Prxy_BCD[i + 1, 1]), 'yellow')
        sleep(1.5)
    else:
        draw_line(win2, Point(Prxy_BCD[i, 0], Prxy_BCD[i, 1]), Point(Prxy_BCD[0, 0], Prxy_BCD[0, 1]), 'yellow')
        sleep(1.5)

for i in range(len(Prxy_CDE)):
    if i != len(Prxy_CDE) - 1:
        draw_line(win2, Point(Prxy_CDE[i, 0], Prxy_CDE[i, 1]), Point(Prxy_CDE[i + 1, 0], Prxy_CDE[i + 1, 1]), 'yellow')
        sleep(1.5)
    else:
        draw_line(win2, Point(Prxy_CDE[i, 0], Prxy_CDE[i, 1]), Point(Prxy_CDE[0, 0], Prxy_CDE[0, 1]), 'yellow')
        sleep(1.5)

win2.getMouse()
win2.close()

win3 = GraphWin("3-D Pyramid (Hidden Lines Removal)", xw, yw)
win3.setBackground('white')

# Draw the base
base = Polygon(Point(base_points_shifted[0, 0], base_points_shifted[0, 1]),
               Point(base_points_shifted[1, 0], base_points_shifted[1, 1]),
               Point(base_points_shifted[2, 0], base_points_shifted[2, 1]))
base.setFill('lightblue')
base.draw(win3)

# Draw the sides of the pyramid
for i in range(len(base_points_shifted)):
    side = Polygon(Point(base_points_shifted[i, 0], base_points_shifted[i, 1]),
                   Point(apex_point[0, 0], apex_point[0, 1]),
                   Point(base_points_shifted[(i + 1) % len(base_points_shifted), 0],
                         base_points_shifted[(i + 1) % len(base_points_shifted), 1]))
    side.setFill('lightblue')
    side.draw(win3)

win3.getMouse()
win3.close()

win4 = GraphWin("3-D Pyramid (Hidden Surface Removal)", xw, yw)
win4.setBackground('white')

base = Polygon(Point(base_points_shifted[0, 0], base_points_shifted[0, 1]),
               Point(base_points_shifted[1, 0], base_points_shifted[1, 1]),
               Point(base_points_shifted[2, 0], base_points_shifted[2, 1]))
base.setFill('lightblue')
base.draw(win4)

# Draw the sides of the pyramid (removing invisible ones)
for i in range(len(base_points_shifted)):
    if is_visible(base_points_shifted[i], apex_point[0], base_points_shifted[(i + 1) % len(base_points_shifted)]):
        side = Polygon(Point(base_points_shifted[i, 0], base_points_shifted[i, 1]),
                       Point(apex_point[0, 0], apex_point[0, 1]),
                       Point(base_points_shifted[(i + 1) % len(base_points_shifted), 0],
                             base_points_shifted[(i + 1) % len(base_points_shifted), 1]))
        side.setFill('lightblue')
        side.draw(win4)

win4.getMouse()
win4.close()