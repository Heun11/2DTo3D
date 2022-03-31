import pygame as p
import numpy as np
from math import sin,cos


p.init()
WIDTH = 600
HEIGHT = 600
screen = p.display.set_mode([WIDTH, HEIGHT])
p.display.set_caption("3D test")
clock = p.time.Clock()

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (250, 12, 234)
GREEN = (0,255,0)

cube_position = [WIDTH//2,HEIGHT//2]
scale = 100
speed = 0.01
angle = 0
points = [
    np.matrix([-1, -1, 1]),
    np.matrix([1, -1, 1]),
    np.matrix([1, 1, 1]),
    np.matrix([-1, 1, 1]),

    np.matrix([-1, -1, -1]),
    np.matrix([1, -1, -1]),
    np.matrix([1, 1, -1]),
    np.matrix([-1, 1, -1])
]

projection_matrix = [
    [1,0,0],
    [0,1,0]
]

projected_points = [
    [n,n] for n in range(len(points))
]


def connect_points(i, j, points):
    p.draw.line(screen, WHITE, (points[i][0], points[i][1]), (points[j][0], points[j][1]))

# main loop
run = True
while run:
    for event in p.event.get():
        if event.type == p.QUIT:
            run = False
        if event.type == p.KEYDOWN:
            if event.key == p.K_ESCAPE:
                run = False
            
    screen.fill(BLACK)

    # doing
    rotationZ_matrix = np.matrix([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1],
    ])

    rotationY_matrix = np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)],
    ])

    rotationX_matrix = np.matrix([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)],
    ])

    angle += speed

    i = 0
    for point in points:
        rotated2d = np.dot(rotationZ_matrix, point.reshape(3,1))
        rotated2d = np.dot(rotationY_matrix, rotated2d)
        rotated2d = np.dot(rotationX_matrix, rotated2d)

        projected2d = np.dot(projection_matrix, rotated2d)

        x = int(projected2d[0][0]*scale) + cube_position[0]
        y = int(projected2d[1][0]*scale) + cube_position[1]

        projected_points[i] = [x,y]

        p.draw.circle(screen, GREEN, (x,y), 5)

        i += 1

    connect_points(0, 1, projected_points)
    connect_points(1, 2, projected_points)
    connect_points(2, 3, projected_points)
    connect_points(3, 0, projected_points)

    connect_points(4, 5, projected_points)
    connect_points(5, 6, projected_points)
    connect_points(6, 7, projected_points)
    connect_points(7, 4, projected_points)

    connect_points(0, 4, projected_points)
    connect_points(1, 5, projected_points)
    connect_points(2, 6, projected_points)
    connect_points(3, 7, projected_points)

    # update display
    p.display.update()
    # fps
    clock.tick(60)

# quit
p.quit()

