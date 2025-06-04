# Snake Game

from tkinter import *
import random

GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 200
SPACE_SIZE = 50
BODY_PARTS = 3

THEMES = {
    "Classic": {"bg": "#000000", "snake": "#00FF00", "food": "#FF0000"},
    "Ocean":   {"bg": "#001f3f", "snake": "#7FDBFF", "food": "#39CCCC"},
    "Sunset":  {"bg": "#FB9062", "snake": "#CE4993", "food": "#EE5D6C"},
    "Retro":   {"bg": "#F6DCAC", "snake": "#028391", "food": "#F85525"}
}

# Predefine colors globally so they are accessible before theme is applied
BACKGROUND_COLOR = THEMES["Classic"]["bg"]
SNAKE_COLOR = THEMES["Classic"]["snake"]
FOOD_COLOR = THEMES["Classic"]["food"]

class Snake:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        self.color = color

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                                                  fill=self.color, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self, canvas, color):
        self.canvas = canvas
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        self.canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=color, tag="food")

def apply_theme(theme_name):
    global BACKGROUND_COLOR, SNAKE_COLOR, FOOD_COLOR, snake, food, score, direction, game_running
    theme = THEMES[theme_name]
    BACKGROUND_COLOR = theme["bg"]
    SNAKE_COLOR = theme["snake"]
    FOOD_COLOR = theme["food"]

    canvas.config(bg=BACKGROUND_COLOR)
    score_label.config(bg=BACKGROUND_COLOR)
    high_score_label.config(bg=BACKGROUND_COLOR)

    canvas.delete("all")
    score = 0
    direction = None
    game_running = False
    score_label.config(text="Score: 0")
    high_score_label.config(text=f"High Score: {high_score}")

    snake = Snake(canvas, SNAKE_COLOR)
    food = Food(canvas, FOOD_COLOR)
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, font=("consolas", 30),
                       text="Press SPACEBAR to start", fill="white", tag="start_message")
    animate_title("SNAKE", 0, SNAKE_COLOR)

def animate_title(text, index, color):
    if index < len(text):
        spacing = 30  # Slightly closer spacing
        start_x = GAME_WIDTH / 2 - (len(text) - 1) * spacing / 2
        canvas.create_text(start_x + index * spacing, 40,
                           text=text[index], fill=color,
                           font=("Courier New", 36, "bold"), tag=f"title{index}")
        window.after(150, lambda: animate_title(text, index + 1, color))

def next_turn():
    global snake, food, direction, score, high_score

    if not game_running:
        return

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                                     fill=SNAKE_COLOR, tag="snake")
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        if score > high_score:
            high_score = score
        score_label.config(text=f"Score: {score}")
        high_score_label.config(text=f"High Score: {high_score}")
        canvas.delete("food")
        food = Food(canvas, FOOD_COLOR)
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collision():
        game_over()
    else:
        window.after(SPEED, next_turn)

def change_direction(event):
    global direction
    new_direction = event.keysym.lower()
    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction

def check_collision():
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    global game_running
    game_running = False
    canvas.delete("all")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 50,
                       font=("consolas", 70), text="GAME OVER", fill="red", tag="gameover")
    canvas.create_window(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 30,
                         window=Button(window, text="Reset Game", font=("consolas", 20),
                                       command=lambda: apply_theme(theme_var.get())),
                         tag="reset_button")

def start_game(event=None):
    global direction, game_running
    if direction is None:
        direction = "down"
        game_running = True
        canvas.delete("start_message")
        canvas.delete("reset_button")
        next_turn()

window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
high_score = 0
direction = None
game_running = False

# Theme selector
theme_var = StringVar(value="Classic")
theme_menu = OptionMenu(window, theme_var, *THEMES.keys(), command=apply_theme)
theme_menu.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

score_label = Label(window, text="Score: 0", font=("consolas", 20), bg=BACKGROUND_COLOR, fg="white")
score_label.place(x=10, y=5)

high_score_label = Label(window, text="High Score: 0", font=("consolas", 20), bg=BACKGROUND_COLOR, fg="white")
high_score_label.place(x=GAME_WIDTH - 220, y=5)

animate_title("SNAKE", 0, SNAKE_COLOR)

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind("<Left>", change_direction)
window.bind("<Right>", change_direction)
window.bind("<Up>", change_direction)
window.bind("<Down>", change_direction)
window.bind("<space>", start_game)

snake = Snake(canvas, SNAKE_COLOR)
food = Food(canvas, FOOD_COLOR)
canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2,
                   font=("consolas", 30), text="Press SPACEBAR to start", fill="white", tag="start_message")

window.mainloop()

