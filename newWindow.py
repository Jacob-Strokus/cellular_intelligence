import tkinter as tk
from coevolution import coevolution

# creates a new window. Can be used to create abitrary instances of new windows to add to simulation
class NewWindow:

    # initialization function
    def __init__(self):
        # self.root = root
        # self.window = tk.Toplevel(root)
        # self.window.title("New Window")
        new_root = tk.Tk()
        new_root.title("New Window")
        new_root.mainloop()


    @staticmethod
    def main():
        evolution_algorithm = coevolution(5)
        evolution_algorithm.main()
