import pygame as p
import numpy as np
from math import sin,cos

# vars
p.init()
WIDTH = 601
HEIGHT = 601
screen = p.display.set_mode([WIDTH, HEIGHT])
p.display.set_caption("3D")
clock = p.time.Clock()

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (27, 234, 245)

Xangle = 0
Yangle = 0
Zangle = 0

cube_position = [WIDTH//2,HEIGHT//2]
scale = 100
speed = 0.02
Xspeed = 0
Yspeed = 0
Zspeed = 0
points = []


points.append(np.matrix([-1, -1, 1]))
points.append(np.matrix([1, -1, 1]))
points.append(np.matrix([1,  1, 1]))
points.append(np.matrix([-1, 1, 1]))
points.append(np.matrix([-1, -1, -1]))
points.append(np.matrix([1, -1, -1]))
points.append(np.matrix([1, 1, -1]))
points.append(np.matrix([-1, 1, -1]))


projection_matrix = np.matrix([
    [1,0,0],
    [0,1,0]
])

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

            if event.key == p.K_w:
                Xspeed = speed
            
            if event.key == p.K_s:
                Xspeed = -speed

            if event.key == p.K_a:
                Yspeed = -speed
            
            if event.key == p.K_d:
                Yspeed = speed

            if event.key == p.K_q:
                Zspeed = speed
            
            if event.key == p.K_e:
                Zspeed = -speed

        if event.type == p.KEYUP:
            if event.key == p.K_w:
                Xspeed = 0
            
            if event.key == p.K_s:
                Xspeed = 0

            if event.key == p.K_a:
                Yspeed = 0
            
            if event.key == p.K_d:
                Yspeed = 0

            if event.key == p.K_q:
                Zspeed = 0
            
            if event.key == p.K_e:
                Zspeed = 0
            

    screen.fill(BLACK)

    # doing everything
    rotationZ_matrix = np.matrix([
        [cos(Zangle), -sin(Zangle), 0],
        [sin(Zangle), cos(Zangle), 0],
        [0, 0, 1],
    ])

    rotationY_matrix = np.matrix([
        [cos(Yangle), 0, sin(Yangle)],
        [0, 1, 0],
        [-sin(Yangle), 0, cos(Yangle)],
    ])

    rotationX_matrix = np.matrix([
        [1, 0, 0],
        [0, cos(Xangle), -sin(Xangle)],
        [0, sin(Xangle), cos(Xangle)],
    ])

    Xangle += Xspeed
    Yangle += Yspeed
    Zangle += Zspeed

    i = 0
    for point in points:

        rotated2d = np.dot(rotationZ_matrix, point.reshape((3, 1)))
        rotated2d = np.dot(rotationY_matrix, rotated2d)
        rotated2d = np.dot(rotationX_matrix, rotated2d)

        projected2d = np.dot(projection_matrix, rotated2d)

        x = int(projected2d[0][0]*scale)+cube_position[0]
        y = int(projected2d[1][0]*scale)+cube_position[1]

        projected_points[i] = [x,y]

        p.draw.circle(screen, RED, (x,y), 5)
        
        i+=1

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

