import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import time

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
gluOrtho2D(-1, 1, -1, 1)

left_bound, right_bound = -0.9, 0.9
bottom_bound, top_bound = -0.9, 0.9

points = []

speed_factor = 1.0
blinking = False
frozen = False

def add_point(mouse_x, mouse_y):
    x = (mouse_x / width) * 2 - 1
    y = -((mouse_y / height) * 2 - 1)
    dx = random.choice([-0.005, 0.005])
    dy = random.choice([-0.005, 0.005])
    color = [random.random(), random.random(), random.random()]
    points.append([x, y, dx, dy, *color, True])
    print(f"added point at ({x:.2f}, {y:.2f}) moving ({dx}, {dy}) color: {color}")

def draw_box():
    glColor3f(1, 1, 1)
    glBegin(GL_LINES)
    glVertex2f(left_bound, bottom_bound)
    glVertex2f(left_bound, top_bound)
    glVertex2f(left_bound, top_bound)
    glVertex2f(right_bound, top_bound)
    glVertex2f(right_bound, top_bound)
    glVertex2f(right_bound, bottom_bound)
    glVertex2f(right_bound, bottom_bound)
    glVertex2f(left_bound, bottom_bound)
    glEnd()

def draw_points():
    glPointSize(5)
    glBegin(GL_POINTS)
    for p in points:
        if p[7]:
            glColor3f(p[4], p[5], p[6])
            glVertex2f(p[0], p[1])
    glEnd()

def update_points():
    global points, speed_factor
    if frozen:
        return

    for p in points:
        p[0] += p[2] * speed_factor
        p[1] += p[3] * speed_factor

        # If the point moves past the boundary, move it back and reverse direction
        if p[0] < left_bound:
            p[0] = left_bound  # Snap back inside
            p[2] *= -1         # Reverse direction
        
        if p[0] > right_bound:
            p[0] = right_bound
            p[2] *= -1
        
        if p[1] < bottom_bound:
            p[1] = bottom_bound
            p[3] *= -1
        
        if p[1] > top_bound:
            p[1] = top_bound
            p[3] *= -1

def blink_points():
    if blinking:
        for p in points:
            p[7] = not p[7]

def main():
    global speed_factor, blinking, frozen

    last_blink_time = time.time()

    while True:
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        draw_box()
        draw_points()

        current_time = time.time()
        if current_time - last_blink_time >= 0.5:
            blink_points()
            last_blink_time = current_time

        update_points()
        pygame.display.flip()
        pygame.time.wait(10)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 3:
                    add_point(*pygame.mouse.get_pos())

                elif event.button == 1:
                    blinking = not blinking
                    print(f"blinking: {blinking}")

            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    speed_factor *= 1.05
                    print(f"speed: {speed_factor}")
                elif event.key == K_DOWN:
                    speed_factor *= 0.95
                    print(f"speed: {speed_factor}")
                elif event.key == K_SPACE:
                    frozen = not frozen
                    print(f"frozen: {frozen}")

if __name__ == "__main__":
    main()

