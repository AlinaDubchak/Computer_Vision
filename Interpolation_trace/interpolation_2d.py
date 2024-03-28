from math import factorial
from graphics import *
from time import sleep
def initialize_parallelogram_coordinates(st, xw, yw):
    # Calculate center of the window
    center_x = xw / 2
    center_y = yw / 2

    # Adjust coordinates to place parallelogram at the center
    x1 = center_x - st * 1.5
    y1 = center_y + st
    x2 = center_x + st * 1.5
    y2 = center_y + st
    x3 = center_x + st * 0.5
    y3 = center_y - st
    x4 = center_x - st * 0.5
    y4 = center_y - st
    return x1, y1, x2, y2, x3, y3, x4, y4

# Graphic window dimensions and parallelogram size
xw = 600
yw = 600
st = 100  # Increase size of parallelogram

x1, y1, x2, y2, x3, y3, x4, y4 = initialize_parallelogram_coordinates(st, xw, yw)

win = GraphWin("Parallelogram", xw, yw)
win.setBackground('white')

parallelogram = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3), Point(x4, y4))
parallelogram.draw(win)

# Define control points (adjust these for different curve shapes)
control_points = [Point(x1, y1), Point(x2, y2), Point(x3, y3), Point(x4, y4)]

# Choose the desired control points
chosen_control_points = control_points  # Pick either control_points1 or control_points2

# Draw control points (optional)
for point in chosen_control_points:
    point.setFill('red')
    point.draw(win)

# Define number of segments for the Bézier curve (higher = smoother)
num_segments = 20

# Function to calculate a point on the Bézier curve for a given parameter t
def bezier_point(t, control_points):
    n = len(control_points) - 1
    x = 0
    y = 0
    for i in range(n + 1):
        binom = factorial(n) / (factorial(i) * factorial(n - i))
        term_x = (1 - t) ** (n - i) * t**i * control_points[i].getX()
        term_y = (1 - t) ** (n - i) * t**i * control_points[i].getY()
        x += binom * term_x
        y += binom * term_y
    return Point(x, y)

# Draw the Bézier curve
for i in range(num_segments):
    t = i / (num_segments - 1)
    point = bezier_point(t, chosen_control_points)
    if i == 0:
        start_point = point
    else:
        line = Line(start_point, point)
        line.setWidth(2)  # Set the width of the line to make it thicker
        line.draw(win)
        start_point = point
    update(50)  # Update the window every 50 milliseconds for slower animation

# Interpolation lines for parallelogram
for i in range(len(control_points)):
    line = Line(control_points[i], chosen_control_points[i-1])
    line.setFill('blue')
    line.setWidth(2)  # Set the width of the line to make it thicker
    line.draw(win)
    sleep(0.5)
    update(50)  # Update the window every 50 milliseconds for slower animation

win.getMouse()
win.close()
