import pygame
import math
import sys

pygame.display.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Gravity Simulation")
clock = pygame.time.Clock()

#TIME 
dt = 0.05

#Gravitational Constant 
G = 670

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

# Create your objects with custom RGB tuples at the end
star1 = Star(200, 750, 450, 11, 0.0, 22.0, (255, 180, 0))     # Yellow-Orange
star2 = Star(200, 850, 450, 15, 0.0, -22.0, (255, 255, 255))  # White
star3 = Star(150, 300, 450, 12, 0.0, -16.5, (0, 255, 255))    # Cyan / Light Blue

stars = [star1, star2, star3]

Running = True

while Running : 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  
                    Running = False  
    
    dx1 = star2.x - star1.x
    dx2 = star3.x - star2.x
    dx3 = star3.x - star1.x
    dy1 = star2.y - star1.y
    dy2 = star3.y - star2.y
    dy3 = star3.y - star1.y

    A = math.hypot(dx1 , dy1)
    B = math.hypot(dx2 , dy2)
    C = math.hypot(dx3 , dy3)

    if A >15 and B >15 and C >15:

        a1 = (G*star1.m)/(A**2)
        a2 = (G*star1.m)/(C**2)
        a3 = (G*star2.m)/(A**2)
        a4 = (G*star2.m)/(B**2)
        a5 = (G*star3.m)/(B**2)
        a6 = (G*star3.m)/(C**2)

        #Acceleration For STAR 1 
        star1.ax = (a3 * (dx1 / A)) + (a6 * (dx3 / C)) 
        star1.ay = (a3 * (dy1 / A)) + (a6 * (dy3 / C))

        #Acceleration For STAR 2
        star2.ax = (-a1 * (dx1 / A)) + (a5 * (dx2 / B))
        star2.ay = (-a1 * (dy1 / A)) + (a5 * (dy2 /B))

        #Acceleration For STAR 3
        star3.ax = (-a2 * (dx3 / C) ) + (-a4 * (dx2 / B))
        star3.ay = (-a2 * (dy3 / C)) + (-a4 * (dy2 / B))

        #Velocity Update
        for star in stars:
            star.vx += star.ax *dt
            star.vy += star.ay *dt

    screen.fill((20, 20, 20)) 

    for star in stars:
        star.x += star.vx * dt
        star.y += star.vy * dt

        #TRAIL 
        star.trail.append((int(star.x), int(star.y)))
        if len(star.trail) > 500:
            star.trail.pop(0)
        

        if len(star.trail) > 1:
            pygame.draw.lines(screen, star.color, False, star.trail, 2)

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
