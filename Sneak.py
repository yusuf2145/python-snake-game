import turtle
import time
import random

# Config
WIDTH, HEIGHT = 800, 600
STEP = 20
DELAY = 0.1

# Score
score = 0
high_score = 0

# Screen
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("black")
wn.setup(width=WIDTH, height=HEIGHT)
wn.tracer(0)

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("white")
head.penup()
head.goto(0, 0)
head.direction = "stop"   # start stopped so it doesn't move before input
head.showturtle()

# Food
food = turtle.Turtle()
food.speed(0)
food.shape("square")
food.color("white")
food.penup()
food.goto(0, 100)
food.showturtle()

# Segments
segments = []

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, HEIGHT//2 - 50)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# Movement helpers
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    x, y = head.xcor(), head.ycor()
    if head.direction == "up":
        head.sety(y + STEP)
    elif head.direction == "down":
        head.sety(y - STEP)
    elif head.direction == "left":
        head.setx(x - STEP)
    elif head.direction == "right":
        head.setx(x + STEP)

def reset_game():
    global score, DELAY, segments
    time.sleep(0.5)
    head.goto(0, 0)
    head.direction = "stop"

    # hide and clear segments
    for seg in segments:
        seg.goto(1000, 1000)
    segments.clear()

    score = 0
    DELAY = 0.1
    update_score()

def update_score():
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}", align="center",
              font=("Courier", 24, "normal"))

# Key bindings
wn.listen()
wn.onkey(go_up, "Up")
wn.onkey(go_down, "Down")
wn.onkey(go_left, "Left")
wn.onkey(go_right, "Right")
wn.onkey(go_up, "w")
wn.onkey(go_down, "s")
wn.onkey(go_left, "a")
wn.onkey(go_right, "d")

# Borders (half-dimensions minus margin)
XMAX = WIDTH // 2 - 10
YMAX = HEIGHT // 2 - 10

# Main loop
while True:
    wn.update()

    # Move tail (from end to front)
    for i in range(len(segments)-1, 0, -1):
        segments[i].goto(segments[i-1].xcor(), segments[i-1].ycor())
    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    # Move head
    move()

    # Border collision
    if (head.xcor() > XMAX or head.xcor() < -XMAX or
        head.ycor() > YMAX or head.ycor() < -YMAX):
        reset_game()

    # Food collision
    if head.distance(food) < 20:
        # move food
        food.goto(random.randint(-XMAX//STEP, XMAX//STEP)*STEP,
                  random.randint(-YMAX//STEP, YMAX//STEP)*STEP)

        # add new segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("gray")
        new_segment.penup()
        segments.append(new_segment)

        # update speed & score
        if DELAY > 0.03:
            DELAY -= 0.002
        score += 10

        # high score check
        if score > high_score:
            high_score = score

        update_score()

    # Self collision
    for seg in segments:
        if seg.distance(head) < 20:
            reset_game()
            break

    time.sleep(DELAY)
