import pygame 
import sys
import math
import random

pygame.display.init()

Width = 1500
Height = 750
screen = pygame.display.set_mode((Width , Height))
pygame.display.set_caption("Obstacle Avoidance")
clock = pygame.time.Clock()

dt = 0.1

# Ball properties 
ball_x = 700
ball_y = 200
ball_radius = 7
ball_vx = 15
ball_vy = 15
ball_v = math.hypot(ball_vx,ball_vy)
ball_ax = 0.0
ball_ay = 0.0
ball_trail = []
ball_color = (255,255,255)

#Walls
class Walls:
    def __init__(self, x1, y1, x2, y2, color):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color 
        
walls = []
number_of_walls = 50
for i in range(number_of_walls):
    x1 = random.randint(50, Width - 50)
    y1 = random.randint(150, Height - 50) 
    length = random.randint(50, 70)
    angle = random.uniform(0, 2 * math.pi)
    
    x2 = x1 + length * math.cos(angle)
    y2 = y1 + length * math.sin(angle)
    
    x2 = max(50, min(x2, Width - 50))
    y2 = max(150, min(y2, Height - 50))
    
    random_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    wall = Walls(x1, y1, x2, y2, random_color)
    walls.append(wall)


Running = True
while Running:
      
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  
                Running = False
                
    ball_v = math.hypot(ball_vx , ball_vy)
    if ball_v>0:
        # Sensors Properties - 
        sensor_range = 100

        #Front Sensor
        front_sensor_x1 = ball_x
        front_sensor_x2 = ((ball_vx/ball_v)*sensor_range) + front_sensor_x1
        front_sensor_y1 = ball_y
        front_sensor_y2 = ((ball_vy/ball_v)*sensor_range) + front_sensor_y1
        front_sensor_color = (0,255,0)
        

        #Left Sensor 
        left_sensor_x1 = ball_x
        left_sensor_x2 = ((-ball_vy/ball_v)*sensor_range) + left_sensor_x1
        left_sensor_y1 = ball_y
        left_sensor_y2 = ((ball_vx/ball_v)*sensor_range) + left_sensor_y1
        left_sensor_color = (0,255,0)
        left_sensor_direction = math.hypot((left_sensor_x2-left_sensor_x1), (left_sensor_y2 - left_sensor_y1))


        #Right Sensor 
        right_sensor_x1 = ball_x
        right_sensor_x2 = ((ball_vy/ball_v)*sensor_range) + right_sensor_x1
        right_sensor_y1 = ball_y
        right_sensor_y2 = ((-ball_vx/ball_v)*sensor_range) + right_sensor_y1
        right_sensor_color = (0,255,0)
        right_sensor_direction = math.hypot((right_sensor_x2-right_sensor_x1), (right_sensor_y2 - right_sensor_y1))

    # Sensor Detection 
    front_sensor_detection = False
    left_sensor_detection = False
    right_sensor_detection = False

    for w in walls:
        # --- Front Sensor Detection ---
        del_front = (front_sensor_x2 - front_sensor_x1) * (w.y2 - w.y1) - (front_sensor_y2 - front_sensor_y1) * (w.x2 - w.x1) 
        if del_front != 0:
            t_front = ((w.x1 - front_sensor_x1) * (w.y2 - w.y1) - (w.y1 - front_sensor_y1) * (w.x2 - w.x1)) / del_front
            u_front = ((w.x1 - front_sensor_x1) * (front_sensor_y2 - front_sensor_y1) - (w.y1 - front_sensor_y1) * (front_sensor_x2 - front_sensor_x1)) / del_front
            if 0 <= t_front <= 1 and 0 <= u_front <= 1:
                front_sensor_detection = True
        
        # --- Left Sensor Detection ---
        del_left = (left_sensor_x2 - left_sensor_x1) * (w.y2 - w.y1) - (left_sensor_y2 - left_sensor_y1) * (w.x2 - w.x1) 
        if del_left != 0:
            t_left = ((w.x1 - left_sensor_x1) * (w.y2 - w.y1) - (w.y1 - left_sensor_y1) * (w.x2 - w.x1)) / del_left
            u_left = ((w.x1 - left_sensor_x1) * (left_sensor_y2 - left_sensor_y1) - (w.y1 - left_sensor_y1) * (left_sensor_x2 - left_sensor_x1)) / del_left
            if 0 <= t_left <= 1 and 0 <= u_left <= 1:
                left_sensor_detection = True

        # --- Right Sensor Detection ---
        del_right = (right_sensor_x2 - right_sensor_x1) * (w.y2 - w.y1) - (right_sensor_y2 - right_sensor_y1) * (w.x2 - w.x1) 
        if del_right != 0:
            t_right = ((w.x1 - right_sensor_x1) * (w.y2 - w.y1) - (w.y1 - right_sensor_y1) * (w.x2 - w.x1)) / del_right
            u_right = ((w.x1 - right_sensor_x1) * (right_sensor_y2 - right_sensor_y1) - (w.y1 - right_sensor_y1) * (right_sensor_x2 - right_sensor_x1)) / del_right
            if 0 <= t_right <= 1 and 0 <= u_right <= 1:
                right_sensor_detection = True

    #Robot Decision -
    ball_ax = 0.0
    ball_ay = 0.0

    if front_sensor_detection:
        front_sensor_color = (255, 0, 0)
        desired_speed = ball_v
        
        if not left_sensor_detection and right_sensor_detection:
            ball_vx = ((left_sensor_x2 - left_sensor_x1) / left_sensor_direction) * desired_speed
            ball_vy = ((left_sensor_y2 - left_sensor_y1) / left_sensor_direction) * desired_speed
            
        if left_sensor_detection and not right_sensor_detection:
            ball_vx = ((right_sensor_x2 - right_sensor_x1) / right_sensor_direction) * desired_speed
            ball_vy = ((right_sensor_y2 - right_sensor_y1) / right_sensor_direction) * desired_speed
            
        if left_sensor_detection and right_sensor_detection:
            ball_vx = -ball_vx
            ball_vy = -ball_vy
            
        if not left_sensor_detection and not right_sensor_detection:
            decision = random.randint(0, 1)
            if decision == 0:
                ball_vx = ((left_sensor_x2 - left_sensor_x1) / left_sensor_direction) * desired_speed
                ball_vy = ((left_sensor_y2 - left_sensor_y1) / left_sensor_direction) * desired_speed
            if decision == 1:
                ball_vx = ((right_sensor_x2 - right_sensor_x1) / right_sensor_direction) * desired_speed
                ball_vy = ((right_sensor_y2 - right_sensor_y1) / right_sensor_direction) * desired_speed

    if left_sensor_detection:
        left_sensor_color = (255, 0, 0)
        
    if right_sensor_detection:
        right_sensor_color = (255, 0, 0)
            

    if ball_x > Width - ball_radius:
        ball_x = Width - ball_radius  
        ball_vx = -ball_vx
    elif ball_x < ball_radius:
        ball_x = ball_radius
        ball_vx = -ball_vx

    if ball_y > Height - ball_radius:
        ball_y = Height - ball_radius  
        ball_vy = -ball_vy
    elif ball_y < ball_radius:
        ball_y = ball_radius
        ball_vy = -ball_vy

    ball_vx += ball_ax * dt
    ball_vy += ball_ay * dt 
    ball_x += ball_vx * dt
    ball_y += ball_vy * dt

    #Robot Trail
    ball_trail.append((int(ball_x) , int(ball_y)))

    if len(ball_trail) > 5000 :
        ball_trail.pop(0)
    
    screen.fill((20, 20, 20)) 

    if len(ball_trail) > 1 :
        pygame.draw.lines(screen , ball_color , False , ball_trail , 2)

    #DRAW
    for w in walls:
        pygame.draw.line(screen, w.color, (w.x1 , w.y1 ), (w.x2 , w.y2), 5)

    pygame.draw.circle(
            screen,
            ball_color,
            (int(ball_x), int(ball_y)),
            ball_radius
        )
    
    pygame.draw.line(
            screen,
            front_sensor_color,
            (int(front_sensor_x1), int(front_sensor_y1)),
            (int(front_sensor_x2), int(front_sensor_y2)),
            2
        )
    pygame.draw.line(
            screen,
            left_sensor_color,
            (int(left_sensor_x1), int(left_sensor_y1)),
            (int(left_sensor_x2), int(left_sensor_y2)),
            2
        )
    pygame.draw.line(
            screen,
            right_sensor_color,
            (int(right_sensor_x1), int(right_sensor_y1)),
            (int(right_sensor_x2), int(right_sensor_y2)),
            2
        )
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
