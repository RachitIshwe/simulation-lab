import pygame
import math
import sys
import random

pygame.display.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Gravity Simulation")
clock = pygame.time.Clock()

#TIME 
dt = 0.02

#Gravitational Constant 
G = 670

#Class
class Star :

    def __init__(self , m , x , y , radius , vx , vy , color):
        self.m = m
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = vx 
        self.vy = vy 
        self.ax = 0.0
        self.ay = 0.0
        self.trail = []
        self.color = color


stars = []
dis = []

number_stars = 100

for i in range(number_stars):

    #Random Values 
    random_radius = random.randint(3, 8)
    random_mass = random_radius * 20
    random_x = random.randint(50, 1150)
    random_y = random.randint(50, 750)  
    random_vx = random.uniform(-5.0, 5.0)
    random_vy = random.uniform(-5.0, 5.0)
    random_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

    #Making Stars
    star = Star(random_mass, random_x, random_y, random_radius, random_vx, random_vy, random_color)
    stars.append(star)

Running = True

while Running : 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  
                    Running = False  
    for star in stars:
        star.ax = 0.0
        star.ay = 0.0


    for i in range (number_stars) : 
        star1=stars[i]

        for j in range (i +1 , number_stars):
            star2 = stars[j]
            dx = star2.x - star1.x
            dy = star2.y - star1.y

            r= math.hypot(dx,dy)

            if r > 10 :
                a1 = (G*star2.m) / (r**2)
                a2 = (G*star1.m) / (r**2)

                star1.ax += a1*(dx/r)
                star1.ay += a1*(dy/r)

                star2.ax -= a2*(dx/r)
                star2.ay -= a2*(dy/r)
                
        #Velocity Update
    for star in stars:
        star.vx += star.ax *dt
        star.vy += star.ay *dt

    screen.fill((20, 20, 20)) 

    for star in stars:
        star.x += star.vx * dt
        star.y += star.vy * dt

        pygame.draw.circle(
            screen,
            star.color,
            (int(star.x), int(star.y)),
            star.radius
        )


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

