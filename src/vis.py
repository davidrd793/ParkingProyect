import tkinter as tk

class ParkingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title = "Parking Visualization"
        self.root.geometry = "1000x1000"


if __name__=="__main__":
    # Iniciar la aplicación
    root = tk.Tk()
    app = ParkingGUI(root)
    root.mainloop()