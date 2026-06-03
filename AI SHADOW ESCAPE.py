import tkinter as tk
from tkinter import messagebox
from queue import PriorityQueue
from collections import deque
import random

CELL = 50
ROWS = 10
COLS = 10

root = tk.Tk()
root.title("AI Shadow Escape")
root.configure(bg="#121212")

canvas = tk.Canvas(
    root,
    width=COLS * CELL,
    height=ROWS * CELL,
    bg="#121212",
    highlightthickness=0
)
canvas.pack()

maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]

obstacles = [
    (1,1),(1,2),(1,3),
    (2,3),(3,3),(4,3),
    (5,3),(5,4),(5,5),
    (2,6),(3,6),(4,6),
    (7,2),(7,3),(7,4),
    (8,7)
]

for r, c in obstacles:
    maze[r][c] = 1

player = [0, 0]
enemy = [9, 0]
exit_portal = (9, 9)

keys = [(0, 9), (5, 8), (8, 2)]
collected_keys = 0

history = deque(maxlen=12)
history.append((0, 0))

game_over = False

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(start, goal):
    pq = PriorityQueue()
    pq.put((0, start))

    came_from = {}
    cost = {start: 0}

    while not pq.empty():
        current = pq.get()[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        r, c = current

        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr = r + dr
            nc = c + dc

            if not (0 <= nr < ROWS and 0 <= nc < COLS):
                continue

            if maze[nr][nc] == 1:
                continue

            new_cost = cost[current] + 1

            if (nr, nc) not in cost or new_cost < cost[(nr, nc)]:
                cost[(nr, nc)] = new_cost
                priority = new_cost + heuristic((nr, nc), goal)
                pq.put((priority, (nr, nc)))
                came_from[(nr, nc)] = current

    return []

def draw():
    canvas.delete("all")

    for r in range(ROWS):
        for c in range(COLS):

            color = "#1e1e1e"

            if maze[r][c] == 1:
                color = "#6a0dad"

            x1 = c * CELL
            y1 = r * CELL
            x2 = x1 + CELL
            y2 = y1 + CELL

            canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline="#333333"
            )

    gr, gc = exit_portal
    portal_color = "#00ff7f" if collected_keys == 3 else "#228b22"

    canvas.create_rectangle(
        gc*CELL+10,
        gr*CELL+10,
        gc*CELL+40,
        gr*CELL+40,
        fill=portal_color,
        outline=""
    )

    for kr, kc in keys:
        canvas.create_oval(
            kc*CELL+15,
            kr*CELL+15,
            kc*CELL+35,
            kr*CELL+35,
            fill="#ffd700"
        )

    pr, pc = player
    canvas.create_oval(
        pc*CELL+10,
        pr*CELL+10,
        pc*CELL+40,
        pr*CELL+40,
        fill="#00bfff"
    )

    er, ec = enemy
    canvas.create_oval(
        ec*CELL+10,
        er*CELL+10,
        ec*CELL+40,
        er*CELL+40,
        fill="#ff3b30"
    )

    canvas.create_text(
        110,
        15,
        text=f"Keys: {collected_keys}/3",
        fill="white",
        font=("Segoe UI", 12, "bold")
    )

def end_game(title, text):
    global game_over
    if not game_over:
        game_over = True
        messagebox.showinfo(title, text)
        root.destroy()

def move_enemy():
    if game_over:
        return

    if len(history) >= 6:
        target = history[0]
    else:
        target = tuple(player)

    if random.random() < 0.10:
        nr = target[0] + random.choice([-1,0,1])
        nc = target[1] + random.choice([-1,0,1])

        nr = max(0, min(ROWS-1, nr))
        nc = max(0, min(COLS-1, nc))

        if maze[nr][nc] == 0:
            target = (nr, nc)

    path = astar(tuple(enemy), target)

    if path:
        enemy[0], enemy[1] = path[0]

    if tuple(enemy) == tuple(player):
        end_game("Game Over", "Enemy Caught You!")

def check_game():
    global collected_keys

    for key in keys[:]:
        if tuple(player) == key:
            keys.remove(key)
            collected_keys += 1

    if tuple(player) == tuple(enemy):
        end_game("Game Over", "Enemy Caught You!")

    if collected_keys == 3 and tuple(player) == exit_portal:
        end_game("Victory", "Collected 3 Keys And Escaped!")

def move(event):
    if game_over:
        return

    r, c = player

    if event.keysym == "Up":
        nr, nc = r-1, c
    elif event.keysym == "Down":
        nr, nc = r+1, c
    elif event.keysym == "Left":
        nr, nc = r, c-1
    elif event.keysym == "Right":
        nr, nc = r, c+1
    else:
        return

    if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] == 0:
        player[0] = nr
        player[1] = nc

        history.append(tuple(player))

        check_game()
        move_enemy()
        draw()
        check_game()

def show_hint(event=None):
    draw()

    target = exit_portal
    path = astar(tuple(player), target)

    if path:
        nr, nc = path[0]

        canvas.create_rectangle(
            nc*CELL+15,
            nr*CELL+15,
            nc*CELL+35,
            nr*CELL+35,
            fill="lime"
        )

def enemy_loop():
    if not game_over:
        move_enemy()
        draw()
        check_game()
        root.after(800, enemy_loop)

draw()

root.bind("<Up>", move)
root.bind("<Down>", move)
root.bind("<Left>", move)
root.bind("<Right>", move)

root.bind("h", show_hint)
root.bind("H", show_hint)

info = tk.Label(
    root,
    text="Arrow Keys = Move | H = AI Hint | Collect 3 Keys Then Escape",
    font=("Segoe UI", 11, "bold"),
    fg="white",
    bg="#121212"
)
info.pack(pady=5)

enemy_loop()
root.mainloop() 