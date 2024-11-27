import turtle as t
import random
 
w = 500 # Width of box
h = 500 # Height of box
food_size = 10 # Size of food
delay = 100 # in milliseconds

# Values by which snake will move in direction when given direction
offsets = {
    "up": (0, 20),
    "down": (0,-20),
    "left": (-20,0),
    "right": (20,0)
}

global SCORE
SCORE = 0
game_over = False  # To track whether the game is over or not

def reset():
    global snake, snake_dir, food_position, pen, SCORE, game_over
    SCORE = 0  # Reset the score when the game is reset
    game_over = False  # Reset game over state
    update_score()  # Show the reset score
    snake = [[0,0],[0,20],[0,40],[0,60],[0,80]]
    snake_dir = "up"  # default snake direction
    food_position = get_random_food_position()
    food.goto(food_position)  # render food on scene
    move_snake()

def move_snake():
    global snake_dir, SCORE, game_over
 
    if game_over:  # Stop moving if the game is over
        return

    new_head = snake[-1].copy()
    new_head[0] = snake[-1][0] + offsets[snake_dir][0]
    new_head[1] = snake[-1][1] + offsets[snake_dir][1]
    
    # If snake collides with itself or goes out of bounds
    if new_head in snake[:-1] or out_of_bounds(new_head):
        display_game_over()
        game_over = True  # Set game over flag
    else:
        snake.append(new_head)
 
        if not food_collision():
            snake.pop(0)
 
        pen.clearstamps()
      
        for segment in snake:
            pen.goto(segment[0], segment[1])
            pen.stamp()
       
        screen.update() 
        t.ontimer(move_snake, delay)

# Check if the snake goes out of bounds
def out_of_bounds(position):
    x, y = position
    return x > w / 2 or x < -w / 2 or y > h / 2 or y < -h / 2

# Display game over message
def display_game_over():
    score_pen.goto(0, 0)
    score_pen.write("Game Over", align="center", font=("Arial", 30, "bold"))

# If snake collides with food
def food_collision():
    global food_position, SCORE
    if get_distance(snake[-1], food_position) < 20:
        SCORE += 10  # Increase the score when food is eaten
        update_score()  # Update score display
        food_position = get_random_food_position()
        food.goto(food_position)
        return True
    return False

# Function to update the score display
def update_score():
    score_pen.clear()
    score_pen.goto(0, h // 2 - 40)  # Positioning the score at the top
    score_pen.write(f"Score: {SCORE}", align="center", font=("Arial", 24, "bold"))

# Random position for food
def get_random_food_position():
    x = random.randint(int(- w / 2 + food_size), int(w / 2 - food_size))
    y = random.randint(int(- h / 2 + food_size), int(h / 2 - food_size))
    return (x, y)

def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
    return distance
  
# Control
def go_up():
    global snake_dir
    if snake_dir != "down":
        snake_dir = "up"
def go_down():
    global snake_dir
    if snake_dir != "up":
        snake_dir = "down"
def go_left():
    global snake_dir
    if snake_dir != "right":
        snake_dir = "left"
def go_right():
    global snake_dir
    if snake_dir != "left":
        snake_dir = "right"

# Define screen setup
screen = t.Screen()
screen.setup(w, h)
screen.title("Snake Game")
screen.bgcolor("lightgrey")
screen.tracer(0)

# Define snake setup
pen = t.Turtle("square")
pen.penup()

# Define food setup
food = t.Turtle()
food.shape("circle")
food.color("red")
food.shapesize(food_size / 20)
food.penup()

# Create a turtle for the score display
score_pen = t.Turtle()
score_pen.hideturtle()
score_pen.penup()
score_pen.color("black")

# Define control setup
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_right, "Right")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")

reset()
t.done()
