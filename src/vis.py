from tkinter import *

class ParkingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title = "Parking Visualization"
        self.root.geometry("1000x700")


if __name__=="__main__":
    root = Tk()
    app = ParkingGUI(root)
    root.mainloop()