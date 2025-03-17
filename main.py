import tkinter as tk
import random

# Window size
WIDTH = 500
HEIGHT = 500
GRID_SIZE = 20

# Global variables
dx, dy = GRID_SIZE, 0
score = 0
high_score = 0
game_running = False
restart_button = None  # Track the restart button

# Create the main window
window = tk.Tk()
window.title("Basic Snake Game")

# Create the canvas
canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# Create score labels
score_label = tk.Label(window, text="Score: 0", font=("Arial", 14))
score_label.pack()
high_score_label = tk.Label(window, text="High Score: 0", font=("Arial", 14))
high_score_label.pack()

# Snake and food setup
snake = []
food = None

# Function to start a new game
def new_game():
    global snake, dx, dy, score, game_running, food, restart_button

    # Remove restart button if it exists
    if restart_button:
        restart_button.destroy()
        restart_button = None

    # Reset game state
    canvas.delete("all")
    score = 0
    score_label.config(text=f"Score: {score}")
    game_running = True

    # Reset snake
    snake = [(240, 240), (220, 240), (200, 240)]
    for x, y in snake:
        canvas.create_oval(x, y, x + GRID_SIZE, y + GRID_SIZE, fill="green", outline="black", width=2)

    # Place food
    place_food()

    # Start moving
    move_snake()

# Function to place food at a random position
def place_food():
    global food
    x = random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE
    y = random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
    food = (x, y)
    canvas.create_rectangle(x, y, x + GRID_SIZE, y + GRID_SIZE, fill="red")

# Function to move the snake
def move_snake():
    global dx, dy, score, high_score, game_running

    if not game_running:
        return

    # Get head position for checking where head next move
    head_x, head_y = snake[0]
    new_head = (head_x + dx, head_y + dy)

    # Check collisions
    if (new_head[0] < 0 or new_head[0] >= WIDTH or 
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake):
        game_over()
        return

    # Move snake next step forward with placing new head
    snake.insert(0, new_head)

    # Check if food eaten
    if new_head == food:
        score += 1
        score_label.config(text=f"Score: {score}")
        if score > high_score:
            high_score = score
            high_score_label.config(text=f"High Score: {high_score}")
        place_food()
    else:
        snake.pop()

    # Redraw everything
    canvas.delete("all")
    for x, y in snake:
        canvas.create_oval(x, y, x + GRID_SIZE, y + GRID_SIZE, fill="green", outline="black", width=2)
        canvas.create_rectangle(food[0], food[1], food[0] + GRID_SIZE, food[1] + GRID_SIZE, fill="red")

    window.after(100, move_snake)

# Function to change direction
def change_direction(event):
    global dx, dy
    if event.keysym == "Up" and dy == 0:
        dx, dy = 0, -GRID_SIZE
    elif event.keysym == "Down" and dy == 0:
        dx, dy = 0, GRID_SIZE
    elif event.keysym == "Left" and dx == 0:
        dx, dy = -GRID_SIZE, 0
    elif event.keysym == "Right" and dx == 0:
        dx, dy = GRID_SIZE, 0

# Function to handle game over
def game_over():
    global game_running, restart_button
    game_running = False

    # Show "Game Over" message
    canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Game Over!", fill="white", font=("Arial", 20))

    # Remove old restart button if it exists
    if restart_button:
        restart_button.destroy()

    # Create a new Restart button
    restart_button = tk.Button(window, text="Restart Game", bg="green", fg="white", font=("Arial", 14), command=new_game)
    restart_button.pack()

# Bind keys
window.bind("<KeyPress>", change_direction)

# Create "New Game" button
new_game_button = tk.Button(window, text="New Game", bg="green", fg="white", font=("Arial", 14), command=new_game)
new_game_button.pack()

# Start the game loop
window.mainloop()