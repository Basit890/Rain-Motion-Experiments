# Task 1:
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import cos, sin
import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
gluOrtho2D(-1, 1, -1, 1)

raindrops = [[random.uniform(-1, 1), random.uniform(-1, 1)] for _ in range(500)]
rain_direction = [0, -0.02]
rain_bend = 0  
bg_color = [0.0, 0.0, 0.0]
target_bg_color = [0.0, 0.0, 0.0]
is_frozen = False  

def draw_raindrops():
    global raindrops
    glColor3f(0.5, 0.5, 1.0)
    glBegin(GL_LINES)
    for drop in raindrops:
        x, y = drop
        glVertex2f(x, y)
        glVertex2f(x, y - 0.05)  
    glEnd()
    if not is_frozen:
        for drop in raindrops:
            drop[0] += rain_direction[0]
            drop[1] += rain_direction[1]  
            if drop[1] < -1:  
                drop[1] = random.uniform(0.5, 1)
                drop[0] = random.uniform(-1, 1)



def update_background():
    for i in range(3):
        if bg_color[i] < target_bg_color[i]:  
            bg_color[i] += 0.01  
        elif bg_color[i] > target_bg_color[i]:  
            bg_color[i] -= 0.01 

    glClearColor(*bg_color, 1)
    glClear(GL_COLOR_BUFFER_BIT)

def draw_house():
    # roof
    glColor3f(0.6, 0.3, 0.0)  
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.5, -0.2)
    glVertex2f(0.5, -0.2)
    glVertex2f(0.0, 0.3)
    glEnd()
    
    # walls
    glColor3f(1.0, 1.0, 0.0) 
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.4, -0.2)
    glVertex2f(0.4, -0.2)
    glVertex2f(0.4, -0.6)
    glEnd()
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.4, -0.2)
    glVertex2f(-0.4, -0.6)
    glVertex2f(0.4, -0.6)
    glEnd()
    
    # door
    glColor3f(0.3, 0.1, 0.0)  
    glBegin(GL_QUADS)
    glVertex2f(-0.1, -0.6)
    glVertex2f(0.1, -0.6)
    glVertex2f(0.1, -0.3)
    glVertex2f(-0.1, -0.3)
    glEnd()

def draw_soil():
    glColor3f(0.6, 0.3, 0.0)  
    glBegin(GL_QUADS)
    glVertex2f(-1, -1)
    glVertex2f(1, -1)
    glVertex2f(1, -0.6)
    glVertex2f(-1, -0.6)
    glEnd()

def draw_grass():
    glColor3f(0.0, 0.5, 0.0)
    for i in range(-10, 10):
        x = i * 0.1
        glBegin(GL_TRIANGLES)
        glVertex2f(x, -0.6)
        glVertex2f(x + 0.1, -0.6)
        glVertex2f(x + 0.05, -0.5)
        glEnd()

def draw_sun():
    if bg_color == [0.9, 0.9, 0.9]:
        glColor3f(1.0, 1.0, 0.0)
        glBegin(GL_TRIANGLE_FAN)
        for i in range(360):
            angle = i * 3.14159 / 180
            glVertex2f(-0.7 + 0.1 * cos(angle), 0.7 + 0.1 * sin(angle))
        glEnd()

def draw_moon():
    if bg_color == [0.0, 0.0, 0.0]:
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_TRIANGLE_FAN)
        for i in range(360):
            angle = i * 3.14159 / 180
            glVertex2f(0.7 + 0.1 * cos(angle), 0.7 + 0.1 * sin(angle))
        glEnd()

def main():
    global rain_bend, target_bg_color, is_frozen

    while True:
        update_background()
        draw_raindrops()
        draw_house()
        draw_soil()
        draw_grass()
        draw_sun()
        draw_moon()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
        
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    rain_bend -= 0.005
                elif event.key == K_RIGHT:
                    rain_bend += 0.005
                elif event.key == K_UP:
                    rain_direction[1] *= 1.1  
                elif event.key == K_DOWN:
                    rain_direction[1] *= 0.8                
                elif event.key == K_d:  
                    target_bg_color = [0.9, 0.9, 0.9]
                elif event.key == K_n:  
                    target_bg_color = [0.0, 0.0, 0.0]
                elif event.key == K_SPACE:
                    is_frozen = not is_frozen  
                    print("Rain Frozen:", is_frozen)  
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    rain_direction[0] -= 0.05  
                elif event.button == 3: 
                    rain_direction[0] += 0.05  
        
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()