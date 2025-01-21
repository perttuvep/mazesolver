from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.wm_title("MazeSolver")
        self.canvas = Canvas()
        self.canvas.pack()
        self.running = False

    def redraw(self):
        self.root.update_idletasks()

    def wait_for_close(self):
        self.running = True

        while self.running:
            self.redraw()

    def close(self):
