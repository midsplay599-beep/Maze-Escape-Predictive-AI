import tkinter as tk
from tkinter import messagebox
from queue import PriorityQueue

CELL = 50
ROWS = 10
COLS = 10

root = tk.Tk()
root.title("Maze Escape Game with AI Hint")

canvas = tk.Canvas(root,
                   width=COLS * CELL,
                   height=ROWS * CELL)
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
goal = (9, 9)

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

            color = "white"

            if maze[r][c] == 1:
                color = "black"

            if (r, c) == goal:
                color = "red"

            x1 = c * CELL
            y1 = r * CELL
            x2 = x1 + CELL
            y2 = y1 + CELL

            canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline="gray"
            )

    pr, pc = player

    canvas.create_oval(
        pc*CELL+10,
        pr*CELL+10,
        pc*CELL+40,
        pr*CELL+40,
        fill="blue"
    )

def move(event):

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

    if 0 <= nr < ROWS and 0 <= nc < COLS:
        if maze[nr][nc] == 0:
            player[0] = nr
            player[1] = nc

    draw()

    if tuple(player) == goal:
        messagebox.showinfo("Congratulations", "You Escaped the Maze!")

def show_hint(event=None):

    draw()

    path = astar(tuple(player), goal)

    if len(path) > 0:

        nr, nc = path[0]

        canvas.create_rectangle(
            nc*CELL+15,
            nr*CELL+15,
            nc*CELL+35,
            nr*CELL+35,
            fill="green"
        )

draw()

root.bind("<Up>", move)
root.bind("<Down>", move)
root.bind("<Left>", move)
root.bind("<Right>", move)

root.bind("h", show_hint)
root.bind("H", show_hint)

info = tk.Label(
    root,
    text="Arrow Keys = Move | Press H for AI Hint",
    font=("Arial", 12)
)
info.pack()

root.mainloop()
