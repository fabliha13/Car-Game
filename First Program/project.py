from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import sin, cos, pi
import random



# window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# collision variables
collision = False
get = False
collision2 = False
collision3 = False

# points
point_x = random.randint(10, 80) # random x-coordinate of the point
point_y = 150 #y-coordinate of the point

position_of_y = 105 ##CAR POSITION 

# tree
circle1_y = 105 #y-coordinate of the tree
circle2_y = 105 #y-coordinate of the tree
circle_x = random.randint(10, 80) #random x-coordinate of the tree
circles_speed = 0.5 #speed of the tree
trunk = 96 #y-coordinate of the tree trunk

seq = random.randint(1, 5)

dis = False  # obstacle dissappear
dis2 = False  # diamond dissappear
dis3 = False
dis4 = False

cars_speed = 0.38
speed_of_diamond = 0.55
speed_of_obstacle = 0.1

position_of_car = 51 ##X AXIS E KOTHAY ASE CAR 
dir_of_car_movement = 0

game_is_paused = False

stop = True

p_speed = 0

p_cir_speed = 0

total_lives = 3


point_speed = 0.35

num_points = 5
points = []
score = 0

# Storing points coordinates
for i in range(num_points):
    point_x = random.uniform(23, 80)
    point_y = random.uniform(150, 110)
    points.append({'x': point_x, 'y': point_y, 'speed': point_speed})
    #print(points)


class AABB:
    x = 0
    y = 0
    w = 0
    h = 0

    def __init__(self, x, y, w, h):
        self.x=x
        self.y=y
        self.w=w
        self.h=h

    def collides_with(self, other):
        return (self.x < other.x + other.w and
                self.x + self.w > other.x and     #checks overlap between two boxes on both axes
                self.y < other.y + other.h and
                self.y + self.h > other.y)


# obstacle collision condition
##horizontal and vertical collision detect holei collision =True using AABB 
# def square_obstacle_collision(car_pos, car_width, car_height, obstacles):
#     return (car_pos -5 < obstacles.x + obstacles.w and #if the left edge ofthe car is to the left of the right of the obs
#             car_pos + car_width > obstacles.x and #if the right edge of the car is to the left of the obs
#             #top edge of the car=20
#             20 < obstacles.y + obstacles.h and
#             20 + car_height > obstacles.y)



def square_obstacle_collision(car_pos, car_width, car_height, obstacles):
    # Adjust the collision bounds to align with visual representations
    car_left = car_pos - car_width / 2
    car_right = car_pos + car_width / 2
    car_top = 20 + car_height  # Top edge of the car
    car_bottom = 20           # Bottom edge of the car

    obstacle_left = obstacles.x
    obstacle_right = obstacles.x + obstacles.w
    obstacle_top = obstacles.y + obstacles.h
    obstacle_bottom = obstacles.y

    # Check if any overlap occurs
    return (car_right > obstacle_left and  # Car's right edge past obstacle's left edge
            car_left < obstacle_right and  # Car's left edge before obstacle's right edge
            car_top > obstacle_bottom and  # Car's top edge past obstacle's bottom edge
            car_bottom < obstacle_top)     # Car's bottom edge before obstacle's top edge



##Check collision with points and car  

def collision_with_car(car_pos, car_width, car_height, point):
    padding = 1.5  # Tolerance for small points
    car_aabb = AABB(car_pos - car_width / 2 - padding, 20 - car_height / 2 - padding,
                    car_width + 2 * padding, car_height + 2 * padding)
    point_aabb = AABB(point['x'] - padding, point['y'] - padding, 2 * padding, 2 * padding)

    return car_aabb.collides_with(point_aabb)






# Midpoint Line drawing algo 
def draw_line(x1, y1, x2, y2):
    glBegin(GL_POINTS)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    if x1 < x2:
        step_x = 1
    else:
        step_x = -1

    if y1 < y2:
        step_y = 1
    else:
        step_y = -1
    x = x1
    y = y1
    cnt = 0
    if dx > dy:
        p = 2 * dy - dx
        while dx > cnt:
            glVertex2f(x, y)
            x += step_x
            if p >= 0:
                y += step_y
                p -= 2 * dx
            p += 2 * dy
            cnt += 1
    else:
        p = 2 * dx - dy
        while dy > cnt:
            glVertex2f(x, y)
            y += step_y
            if p >= 0:
                x += step_x
                p -= 2 * dy
            p += 2 * dx
            cnt += 1
    glEnd()



def mid_circle(cx, cy, radius):
    d = 1 - radius
    x = 0
    y = radius
    circle_points(x, y, cx, cy)

    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * x - 2 * y + 5
            y -= 1
        x += 1
        circle_points(x, y, cx, cy)


def circle_points(x, y, cx, cy):
    glPointSize(50)
    glBegin(GL_POINTS)
    ###8way symmetric 
    glVertex2f(x + cx, y + cy)
    glVertex2f(y + cx, x + cy)
    glVertex2f(y + cx, -x + cy)
    glVertex2f(x + cx, -y + cy)
    glVertex2f(-x + cx, -y + cy)
    glVertex2f(-y + cx, -x + cy)
    glVertex2f(-y + cx, x + cy)
    glVertex2f(-x + cx, y + cy)
    glEnd()


def draw_point(x, y):  
     
    #glEnable(GL_POINT_SMOOTH)  ##points k smooth dekhay 
    glPointSize(18.0)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
    #glDisable(GL_POINT_SMOOTH)



def drawing_the_car(car_position, car_width, car_height):
    y_car = 20  # Fixed y-position for the car in the middle
    # Draw wheels 
    
    
    radius_of_wheel = car_height/5 # Adjust the wheel size as needed
    wheel_y = y_car - car_height/2 - radius_of_wheel  # Place wheels at the bottom of the car
    position_of_wheel = [-car_width/2, -car_width / 3, car_width / 3, car_width / 2]
    glColor3f(0.0, 0.0, 0.0)  # Black color for the wheels
    glBegin(GL_POINTS)
    for wheel_position in position_of_wheel:
        draw_wheel(car_position + wheel_position, wheel_y, radius_of_wheel)
    glEnd()
    glColor3f(1.0, 0.0, 0.0)  # Red color for the car
    glPointSize(9.0)
    glBegin(GL_POINTS)
    glEnd()
    # Draw car body RECTABGULAR USING MIDPOINT LINE DRAWING ALGO 
    for x in range(int(car_position - car_width / 2), int(car_position + car_width / 2)):
        for y in range(int(y_car - car_height / 2), int(y_car + car_height / 2)):
            glPointSize(9)
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()


def draw_wheel(cx, cy, radius): ###MIDPOINT CIRCLE 
    for i in range(360):
        angle = i * 3.14159 / 180
        x = cx + radius * 0.2 * cos(angle)
        y = cy + radius * 0.7 * sin(angle)
        glVertex2f(x - 0.95, y + 11)
        glVertex2f(x - 0.95, y + 3)


def obstacles_drawing(obstacles):
    glColor3f(1.0, 0.0, 0.0)
    glPointSize(10)
    glBegin(GL_POINTS)
    glEnd()
    draw_line(obstacles.x, obstacles.y, obstacles.x + obstacles.w, obstacles.y) #top edge
    draw_line(obstacles.x, obstacles.y, obstacles.x, obstacles.y + obstacles.h)#left edge
    draw_line(obstacles.x, obstacles.y + obstacles.h, obstacles.x + obstacles.w, obstacles.y + obstacles.h)#bottom edge
    draw_line(obstacles.x + obstacles.w, obstacles.y + obstacles.h, obstacles.x + obstacles.w, obstacles.y)#right edge
    con = obstacles.x
    for i in range(10):
        con += 1
        draw_line(con, obstacles.y, con, obstacles.y + obstacles.h)

def draw_solid_diamond(diamond):
    glColor3f(0.0, 1.0, 0.0)  # Set color to green
    glBegin(GL_POINTS)
    con = diamond.x
    half_width = diamond.w // 2
    half_height = diamond.h // 2
    for i in range(0,half_height):
        for j in range(half_width - i, half_width + i + 1):
            # Draw two symmetrical points at a time
            glVertex2f(con + j, diamond.y + half_height + i)
            glVertex2f(con + j, diamond.y + half_height - i)
    glEnd()
 
# text function
def text_rendering(x, y, text, r, g, b):
    glColor3f(r, g, b)  # Set text color
    glRasterPos2f(x, y)  # Position the text
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))



def display():
    
    global score, game_is_paused
    global position_of_y, score, cars_speed, circle1_y, circle2_y, point_speed, circles_speed, diamond, circle_x, seq, position_of_car, game_is_paused, speed_of_obstacle, collision, var, dis, total_lives, point_y, point_x, trunk, points
    glClear(GL_COLOR_BUFFER_BIT)
    # Draw road
    glColor3f(0.41, 0.41, 0.41)
    draw_line(80, 10, 80, 100)
    draw_line(80, 10, 80, 90)
    draw_line(80, -5, 80, 80)

    draw_line(20, 10, 20, 100)
    draw_line(20, 10, 20, 90)
    draw_line(20, -5, 20, 80)
    glColor3f(0.41, 0.41, 0.41)
    glPointSize(10)
    glBegin(GL_POINTS)
    for x in range(0, 110):
        for y in range(20, 81):
            glVertex2f(y, x)  #MIDPOINT LINE DRAWING ALGO 
    glEnd()
    # Draw circles with updated y-coordinates
    glColor3f(0.0, 1.0, 0.0)  # Green color for the circles FOR TREE 
    
    m = 0
    n = 0
    ##CREATING TREE WITH CIRCLES 
    for i in range(seq):
        glColor3f(0.0, 1.0, 0.0) 
        mid_circle(10, circle1_y + m, 4)

        glColor3f(0.545, 0.181, 0.025)
        glPointSize(20)
        draw_line(10, trunk + n, 10, trunk + 7 + n)

        glColor3f(0.0, 1.0, 0.0)
        mid_circle(90, circle1_y + m, 4)

        glColor3f(0.545, 0.181, 0.025)
        glPointSize(20)
        draw_line(90, trunk + n, 90, trunk + 7 + n)
        m= m+30
        n= n+30
   

    # Draw moving line divider
    glColor3f(1.0, 1.0, 1.0)
    glPointSize(8)
    # draw_line(y_position, 50, y_position + 11, 50)
    draw_line(50, position_of_y, 50, position_of_y + 30)

    # draw obstacles
    obstacles_drawing(obstacles)

    obstacles_drawing(obstacles2)
    obstacles_drawing(obstacles3)

    # Draw moving points
    glColor3f(1.0, 0.843, 0.0)  # golden color

    for point in points:
        draw_point(point['x'], point['y'])

        # Check for collision of point  with car
        if collision_with_car(position_of_car, 5, 10, point):
            print("Point collected!")
            cars_speed += 0.025  #car_speed
            circles_speed += 0.005
            #point_speed += 0.25
            score += 1
            point['y'] = 105
            point['x'] = random.uniform(23, 80)

    # draw diamond untill the game is not ended 
    if game_is_paused == False and total_lives != 0:
        draw_solid_diamond(diamond)

        # Draw car
    glPointSize(12)
    drawing_the_car(position_of_car, 5, 10)

    # Draw "Lives" information text
    glColor3f(1.0, 1.0, 1.0)
    text_rendering(5, 10, f"Lives: {total_lives}", 0.0, 0.0, 0.0)
    text_rendering(5, 90, f"Score: {score}", 0.0, 0.0, 0.0)

    # Check if the game is over and display "Game Over" continuously
    if total_lives == 0:
        glColor3f(1.0, 0.0, 0.0)  # Set text color to white
        text_rendering(43, 50, "Game Over. Press R to Restart.", 0.0, 1.0, 1.0)
        glColor3f(1.0, 1.0, 1.0)
        text_rendering(43, 45, f"Your Final Score: {score}!", 1.0, 1.0, 1.0)
       
    # Draw Buttons
    draw_restart_icon()  # Restart icon at top-left
    draw_pause_icon(game_is_paused)  # Pause/Resume icon at top-center
    draw_exit_icon()  # Exit icon at top-right

   
    glutSwapBuffers()
    
    
    
def draw_restart_icon():
    text_rendering(1,97, "Press R to Restart", 0.0, 0.0, 0.0)


def draw_pause_icon(paused):
    glColor3f(0.7, 0.7, 0.0)  # Yellow for Pause/Resume
    if paused:
        # Smaller triangle for Resume
        draw_line(47, 97, 50, 95)  # Left edge
        draw_line(47, 97, 50, 101)  # Right edge
        draw_line(50, 95, 50, 101)  # Bottom edge
    else:
        # Smaller pause bars
        draw_line(47, 99, 47, 95)  # Left bar
        draw_line(50, 99, 50, 95)  # Right bar

def draw_exit_icon():
    glColor3f(1.0, 0.2, 0.2)  # Red for Exit icon
    # Smaller "X" for Exit
    draw_line(98, 99, 96, 95)  # Diagonal line (\)
    draw_line(96, 99, 98, 95)  # Diagonal line (/)



    


def animation():
    global position_of_y, stop, cars_speed, point_speed, speed_of_diamond, circle1_y, circle2_y, circles_speed
    global circle_x, seq, position_of_car, dis3, dis4, game_is_paused, speed_of_obstacle, dis2, collision
    global collision2, collision3, var, dis, total_lives, point_y, point_x, trunk

    # Check if the game is running (not paused and not stopped)
    if stop and not game_is_paused:
        # Circles animation
        circle1_y -= circles_speed
        circle2_y -= circles_speed
        trunk -= circles_speed

        # Reset circles to the top if they reach the bottom
        if trunk < -100:
            trunk = 105
        if circle1_y < -100:
            circle1_y = 105
            seq = random.randint(1, 5)
        if circle2_y < -300:
            circle2_y = 105
            circle_x = random.randint(30, 70)

        # Update the y-coordinate for each moving point
        for point in points:
            point['y'] -= point['speed']
            if point['y'] < -13:
                point['y'] = 105
                point['x'] = random.uniform(23, 80)
 
        # Update the y-coordinate for the animation
        position_of_y -= cars_speed
        if position_of_y < -25:
            position_of_y = 105

        # Obstacles animation
        obstacles.y -= cars_speed
        obstacles2.y -= cars_speed
        obstacles3.y -= cars_speed

        if obstacles.y < 0 or dis:
            obstacles.x = random.randint(20, 70)
            obstacles.y = 105
            dis = False
        if obstacles2.y < 0 or dis3:
            obstacles2.x = random.randint(20, 70)
            obstacles2.y = 105
            dis3 = False
        if obstacles3.y < 0 or dis4:
            obstacles3.x = random.randint(20, 70)
            obstacles3.y = 105
            dis4 = False
        

        # Diamond animation
        diamond.y -= speed_of_diamond
        diamon_dis = -2000
        if diamond.y < diamon_dis or dis2:
            diamond.x = random.randint(20, 70)
            diamond.y = 1000
            dis2 = False

        # Diamond collision
        get = square_obstacle_collision(position_of_car, 4, 8, diamond)
        if get:
            
            total_lives += 1
            diamon_dis *= 2
            print("Got a live")
            get = False
            dis2 = True

        # Collision detection for obstacles
        collision = square_obstacle_collision(position_of_car, 4, 8, obstacles)
        collision2 = square_obstacle_collision(position_of_car, 4, 8, obstacles2)
        collision3 = square_obstacle_collision(position_of_car, 4, 8, obstacles3)
        
        # collision = square_obstacle_collision(position_of_car, 4, 8, obstacles)
        # collision2 = square_obstacle_collision(position_of_car, 4, 8, obstacles2)
        # collision3 = square_obstacle_collision(position_of_car, 4, 8, obstacles3)
        
        
        # if collision:
        #     collision = False
        #     dis = True
        #     total_lives -= 1
        #     print("You lost 1 live")
        #     if total_lives == 0:
        #         points.clear()
        #         print("Game Over, YOUR score is", score)
        #         stop = False  # Halt the game logic
        # if collision2:
        #     collision2 = False
        #     dis3 = True
        #     print("You are lucky this time  ('-')")
        # if collision3:
        #     collision3 = False
        #     dis4 = True
        #     print("You are lucky this time ('-')")

    # Request screen update if animations are proceeding
        # glutPostRedisplay()
        
        
        # Handle collision with the first obstacle
        if collision:
            collision = False
            dis = True
            total_lives -= 1
            print("You lost 1 life")
            if total_lives == 0:
                print("Game Over, YOUR score is", score)
                stop = False  # Halt the game logic

        # Handle collision with the second obstacle
        if collision2:
            collision2 = False
            dis3 = True
            total_lives -= 1  # Reduce lives for collision with the second obstacle
            print("You lost 1 life (second obstacle)")
            if total_lives == 0:
                print("Game Over, YOUR score is", score)
                stop = False  # Halt the game logic

        # Handle collision with the third obstacle
        if collision3:
            collision3 = False
            dis4 = True
            total_lives -= 1  # Reduce lives for collision with the third obstacle
            print("You lost 1 life (third obstacle)")
            if total_lives == 0:
                print("Game Over, YOUR score is", score)
                stop = False  # Halt the game logic

    # Request screen update if animations are proceeding
    glutPostRedisplay()




def key_action(key, x, y):
    global position_of_car, game_is_paused, total_lives, stop, cars_speed, circles_speed, point_speed, score
    global point_x, point_y, circle1_y, circle2_y, circle_x, diamond, trunk, obstacles, obstacles2, obstacles3

    if key == GLUT_KEY_LEFT:  # Move car left
        if position_of_car > 24:
            position_of_car -= 1.5
    elif key == GLUT_KEY_RIGHT:  # Move car right
        if position_of_car < 78:
            position_of_car += 1.5
    
    if key == b'R' and (total_lives == 0 or game_is_paused or total_lives != 0):
        stop = True
        cars_speed = 0.38
        circles_speed = 0.5
        point_speed = 0.5
        point_x = random.randint(10, 80)
        point_y = 105

        circle1_y = 105
        circle2_y = 105
        circle_x = random.randint(10, 80)

        diamond.y = 1000
        total_lives = 3
        trunk = 96
        score = 0

        # Reset obstacles
        obstacles = AABB(random.randint(20, 70), 100 - 10, 10, 10)
        obstacles2 = AABB(random.randint(20, 70), 100 - 10, 10, 10)
        obstacles3 = AABB(random.randint(20, 70), 100 - 10, 10, 10)

        # Reinitialize points with new random positions and speed
        points.clear()  # Clear the existing points list
        for i in range(num_points):
            point_x = random.uniform(23, 80)
            point_y = random.uniform(150, 110)
            points.append({'x': point_x, 'y': point_y, 'speed': point_speed})

        print("Game Restarted!")
            
   

    
    



    glutPostRedisplay()




def mouse_action(button, state, x, y):
    global game_is_paused, stop, cars_speed, circles_speed, point_speed, score
    global point_x, point_y, circle1_y, circle2_y, circle_x, diamond, trunk, obstacles, obstacles2, obstacles3

    # Transform mouse coordinates to match OpenGL's coordinate space
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = 100 - (y * 100) // WINDOW_HEIGHT  # Convert y-coordinate
        x = (x * 100) // WINDOW_WIDTH  # Convert x-coordinate

        # Exit button click (top-right corner)
        if 96 <= x <= 98 and 95 <= y <= 99:
            print("Exiting Game!Final Score:", score)
            glutLeaveMainLoop()

        # Play/Pause button click (top-center)
        elif 47 <= x <= 53 and 95 <= y <= 99:
            game_is_paused = not game_is_paused
            print("Game Paused!" if game_is_paused else "Game Resumed!")

        
        

    

            # Reset obstacles
            obstacles = AABB(random.randint(20, 70), 100 - 10, 10, 10)
            obstacles2 = AABB(random.randint(20, 70), 100 - 10, 10, 10)
            obstacles3 = AABB(random.randint(20, 70), 100 - 10, 10, 10)

            print("Game Restarted!")
    glutPostRedisplay()



obstacles = AABB(random.randint(20, 70), 100 - 10, 10, 10)
obstacles2 = AABB(random.randint(20, 70), 100 - 10, 10, 10)
obstacles3 = AABB(random.randint(20, 70), 100 - 10, 10, 10)

# obstacles_speed = 1

diamond = AABB(x=40, y=1000, w=8, h=8)


def init():
    glClearColor(1, 0.76, 0.5, 1.75)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 100, 0, 100)  # Adjust the coordinates as needed


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"cAR COLLISION GAME")

    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(key_action)  # Register for normal keys
    glutSpecialFunc(key_action)   # Register for special keys (arrow keys)

    glutMouseFunc(mouse_action)
    glutIdleFunc(animation)
    glutMainLoop()


if __name__ == "__main__":
    main()