from tkinter import *
from clases import *

class ParkingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title = "Parking Visualization"
        self.root.geometry("1000x700+100+100")

        self.canvas = Canvas(self.root, width=800, height=500, bg="gray")
        self.canvas.grid(row=0, column=0, padx=100, pady=(50,0))

        #Por defecto, los widgets de tkinter se ajustan al tamaño de lo que contienen e ignoran width y height
        self.container = Frame(self.root, width=100, height=300, bg="lightblue")
        self.container.grid(row=1, column=0)
        boton = Button(self.container, text="Boton 1").grid(row=0, column=0, padx=(300,10), pady=5)
        boton2 = Button(self.container, text="Boton 2").grid(row=0, column=1, padx=(10, 300), pady=5)

        self.num_columnas = 5  # Número de columnas en el aparcamiento
        self.draw_parking()

    def draw_parking(self):
        x, y = 0, 0
        width_plaza = 90
        height_plaza = 110 


        self.plaza_coords = []
        for i, plaza in enumerate(aparcamiento.plazas):
            color = "blue" if plaza.is_disabled else "green"
            self.plaza_coords.append((x, y, x + width_plaza, y + height_plaza))
            self.canvas.create_rectangle(x, y, x + width_plaza, y + height_plaza, fill=color, outline="white", width=4, tags=plaza.plaza_id)
            self.canvas.create_text(x + width_plaza / 2, y + height_plaza / 2, text=plaza.plaza_id, font=("Arial", 10), fill="white")
            if plaza.is_disabled:
                self.canvas.create_text(x + width_plaza / 2, y + height_plaza - 20, text="DIS", font=("Arial", 8), fill="white")
            x += width_plaza
            if (i + 1) % self.num_columnas == 0:
                x = 150  # Volver al margen izquierdo
                y += height_plaza  # Salto de fila con espacio vertical

        # Dibujar la entrada (rectángulo gris claro) en la parte superior izquierda
        self.canvas.create_rectangle(0, 0, 100, 100, fill="gray", outline="white", width=2)
        self.canvas.create_text(50, 50, text="Entrada", font=("Arial", 12), fill="white")

        # Dibujar la salida (rectángulo gris oscuro) en el centro de la parte derecha
        salida_x1 = 1100  # Borde derecho
        salida_y1 = 400   # Centro vertical
        salida_x2 = 1200  # Borde derecho
        salida_y2 = 500   # Tamaño de la salida
        self.canvas.create_rectangle(salida_x1, salida_y1, salida_x2, salida_y2, fill="gray", outline="white", width=2)
        self.canvas.create_text(salida_x1 + (salida_x2 - salida_x1) / 2, salida_y1 + (salida_y2 - salida_y1) / 2, 
                                text="Salida", font=("Arial", 12), fill="white")
    
    def draw_parking(self):
        




if __name__=="__main__":
    root = Tk()
    app = ParkingGUI(root)
    root.mainloop()