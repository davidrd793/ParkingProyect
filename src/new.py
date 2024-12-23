import tkinter as tk
from tkinter import messagebox

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


class Vehiculo:
    def __init__(self, plate, size="medium", is_disabled=False):
        self.plate = plate
        self.size = size
        self.is_disabled = is_disabled
        self.car_id = f"Car_{plate}"


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
        self.root = root
        self.root.title("Aparcamiento Inteligente")
        self.root.geometry("1200x900")

        # Crear un canvas para el aparcamiento
        self.canvas = tk.Canvas(self.root, width=1200, height=900, bg="gray")
        self.canvas.pack(pady=20)

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

        # Dibujar la salida (rectángulo gris oscuro) en el centro de la parte derecha
        salida_x1 = 1100
        salida_y1 = 400
        salida_x2 = 1200
        salida_y2 = 500  
        self.canvas.create_rectangle(salida_x1, salida_y1, salida_x2, salida_y2, fill="gray", outline="white", width=2)
        self.canvas.create_text(salida_x1 + (salida_x2 - salida_x1) / 2, salida_y1 + (salida_y2 - salida_y1) / 2, 
                                text="Salida", font=("Arial", 12), fill="white")


if __name__=="__main__":
    # Iniciar la aplicación
    root = tk.Tk()
    app = ParkingGUI(root)
    root.mainloop()