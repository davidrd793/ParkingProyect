import tkinter as tk
from tkinter import messagebox

matriculas = ['1234ABC', '1234BCD']

# def check_disability(): ??


# Clases del Sistema
class Plaza:
    def __init__(self, plaza_id, size="medium", is_disabled=False):
        self.plaza_id = plaza_id
        self.size = size
        self.is_disabled = is_disabled
        self.is_occupied = False
        self.vehicle = None

    def occupy(self, vehicle):
        if self.is_occupied:
            raise ValueError(f"Plaza {self.plaza_id} ya está ocupada")
        self.is_occupied = True
        self.vehicle = vehicle

    def vacate(self):
        self.is_occupied = False
        self.vehicle = None


class Vehicle:
    def __init__(self, plate, size=(50, 30), is_disabled=False):
        self.plate = plate
        self.size = size
        self.is_disabled = is_disabled


class Aparcamiento:
    def __init__(self, num_plazas, num_columnas=6):
        self.num_columnas = num_columnas
        self.plazas = [
            Plaza(f"P{i+1}", size="medium" if i % 3 != 0 else "large", is_disabled=(i < 3)) for i in range(num_plazas)
        ]
        self.vehicles = []


# Configuración inicial
aparcamiento = Aparcamiento(15)


class ParkingGUI:
    def __init__(self, root):
        #Initial window configuration
        self.root = root
        self.root.title("Aparcamiento Inteligente")
        self.root.geometry("800x900+20+20")
        self.root.maxsize(width=1200, height=750)
        self.root.minsize(width=1200, height=750) 

        # Crear un canvas para el aparcamiento
        self.canvas = tk.Canvas(self.root, width=1000, height=600, bg="gray")
        self.canvas.grid(column=0, row=0, padx=100)

        self.contenedor = tk.Frame(self.root, width=1000, height=100, bg='lightblue')
        self.contenedor.grid(column=0, row=1, pady=25)

        #Command del boton 1 llama a la función que añade un coche al parking
        self.boton = tk.Button(self.contenedor, text='Add Car', command=self.generate_car).grid(column=0, row=0, padx=(200, 100), pady=(20, 20)) 
        self.boton2 = tk.Button(self.contenedor, text='+1 Floor').grid(column=1, row=0, padx=10)
        self.boton3 = tk.Button(self.contenedor, text='-1 Floor').grid(column=2, row=0, padx=10)


        # Dibujar aparcamiento
        self.num_columnas = 5
        self.draw_parking()

    def draw_parking(self):
        x, y = 150, 150
        width_plaza = 90
        height_plaza = 110

        horizontal_gap = 80
        vertical_gap = 80

        self.plaza_coords = []
        for i, plaza in enumerate(aparcamiento.plazas):
            color = "blue" if plaza.is_disabled else "green"
            self.plaza_coords.append((x, y, x + width_plaza, y + height_plaza))
            self.canvas.create_rectangle(x, y, x + width_plaza, y + height_plaza, fill=color, outline="white", width=4, tags=plaza.plaza_id)
            self.canvas.create_text(x + width_plaza / 2, y + height_plaza / 2, text=plaza.plaza_id, font=("Arial", 10), fill="white")
            if plaza.is_disabled:
                self.canvas.create_text(x + width_plaza / 2, y + height_plaza - 20, text="DIS", font=("Arial", 8), fill="white")
            x += width_plaza + horizontal_gap
            if (i + 1) % self.num_columnas == 0:
                x = 150  # Volver al margen izquierdo
                y += height_plaza + vertical_gap  # Salto de fila con espacio vertical

        # Dibujar la entrada (rectángulo gris claro) en la parte superior izquierda
        self.canvas.create_rectangle(0, 0, 100, 100, fill="gray", outline="white", width=2)
        self.canvas.create_text(50, 50, text="Entrada", font=("Arial", 12), fill="white")


        self.canvas.create_rectangle(1100, 400, 1200, 500, fill="gray", outline="white", width=2)
        self.canvas.create_text(1100 + (1200 - 1100) / 2, 400 + (500 - 400) / 2, 
                                text="Salida", font=("Arial", 12), fill="white")
    
    def generate_car(self):
        plate = matriculas[0]
        car = Vehicle(plate)
        car_vis = self.canvas.create_rectangle(50, 50, 50+car.size[0], 50+car.size[1], fill='red', outline="black")


if __name__=="__main__":
    # Iniciar la aplicación
    root = tk.Tk()
    app = ParkingGUI(root)
    root.mainloop()