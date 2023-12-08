import tkinter as tk
from math import sin, cos, radians


class draggableCube(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<B1-Motion>", self.on_drag)

        self.size = 50
        self.vertices = [
            [-self.size, -self.size, -self.size],
            [self.size, -self.size, -self.size],
            [self.size, self.size, -self.size],
            [-self.size, self.size, -self.size],
            [-self.size, -self.size, self.size],
            [self.size, -self.size, self.size],
            [self.size, self.size, self.size],
            [-self.size, self.size, self.size]
        ]

        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

        self.angle_x = 0
        self.angle_y = 0
        self.draw_cube()

    def draw_cube(self):
        self.delete("cube")
        cube = []

        for edge in self.edges:
            start = self.project(self.vertices[edge[0]])
            end = self.project(self.vertices[edge[1]])
            line = self.create_line(start, end, tags="cube")
            cube.append(line)

    def project(self, point):
        x, y, z = point
        x_rot = x * cos(self.angle_y) - z * sin(self.angle_y)
        y_rot = y * cos(self.angle_x) - z * sin(self.angle_x)
        z_rot = x * sin(self.angle_y) + z * cos(self.angle_y)
        scale = 3
        x_proj = 200 + x_rot * scale
        y_proj = 200 - y_rot * scale
        return x_proj, y_proj

    def on_drag(self, event):
        self.angle_x += radians((event.y - 200) / 2)
        self.angle_y += radians((event.x - 200) / 2)
        self.draw_cube()


root = tk.Tk()
root.title("Cube")

canvas = draggableCube(root, width=400, height=400, bg="white")
canvas.pack()

root.mainloop()
