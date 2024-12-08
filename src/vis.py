from tkinter import *

class ParkingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title = "Parking Visualization"
        self.root.geometry("1000x700+300+150")

        self.canvas = Canvas(self.root, width=200, height=200, bg="gray")
        self.canvas.pack(pady = 50)
        self.menu_frame = Frame(self.root, width=100, height=300, bg="lightblue")
        self.menu_frame.pack()
        boton = Button(self.menu_frame, text="Ver Plazas").grid(row=0, column=1, padx=10)


if __name__=="__main__":
    root = Tk()
    app = ParkingGUI(root)
    root.mainloop()