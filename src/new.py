import tkinter as tk
from tkinter import messagebox
import random

matriculas = ['1234ABC', '1234BCD']
places = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12', 'P13', 'P14', 'P15']

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
    def __init__(self, plate, assigned_place, size=(50, 30), is_disabled=False):
        self.plate = plate
        self.size = size
        self.is_disabled = is_disabled
        self.assigned_place = assigned_place


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
        self.add_car_button = tk.Button(self.contenedor, text='Add Car', command=self.generate_car).grid(column=0, row=0, padx=(200, 100), pady=(20, 20)) 
        self.boton2 = tk.Button(self.contenedor, text='+1 Floor').grid(column=1, row=0, padx=10)
        self.boton3 = tk.Button(self.contenedor, text='-1 Floor').grid(column=2, row=0, padx=10)


        # Dibujar aparcamiento
        self.num_columnas = 5
        self.draw_parking()

    def draw_parking(self):
        x, y = 150, 100
        width_plaza = 80
        height_plaza = 100

        horizontal_gap = 60
        vertical_gap = 60
        global places

        self.plaza_coords = {}
        for i, plaza in enumerate(aparcamiento.plazas):
            color = "blue" if plaza.is_disabled else "green"
            self.plaza_coords[places[i]] = (x, y, x + width_plaza, y + height_plaza)
            self.canvas.create_rectangle(x, y, x + width_plaza, y + height_plaza, fill=color, outline="white", width=4, tags=plaza.plaza_id)
            self.canvas.create_text(x + width_plaza / 2, y + height_plaza / 2, text=plaza.plaza_id, font=("Arial", 10), fill="white")

            x += width_plaza + horizontal_gap
            if (i + 1) % self.num_columnas == 0:
                x = 150  # Volver al margen izquierdo
                y += height_plaza + vertical_gap  # Salto de fila con espacio vertical

        # Dibujar la entrada (rectángulo gris claro) en la parte superior izquierda
        self.canvas.create_rectangle(0, 0, 100, 100, fill="gray", outline="white", width=2)
        self.canvas.create_text(50, 50, text="Entrada", font=("Arial", 12), fill="white")


        self.canvas.create_rectangle(900, 500, 1000, 600, fill="gray", outline="white", width=2)
        self.canvas.create_text(900 + (1000 - 900) / 2, 500 + (600 - 500) / 2, 
                                text="Salida", font=("Arial", 12), fill="white")
    
    def generate_car(self):
        plate = matriculas[0]
        assigned_place = self.assign_place()
        car = Vehicle(plate, assigned_place)
        car_vis = self.canvas.create_rectangle(50, 50, 50+car.size[0], 50+car.size[1], fill='blue', outline="black")
        self.car_movement(car_vis, assigned_place)
    
    def assign_place(self):
        selected_place = random.choice(places)
        places.remove(selected_place)
        return selected_place

    def car_movement(self, car, place):
        x1, y1, x2, y2 = self.plaza_coords[place]
        target_x = (x1 + x2) / 2
        target_y = (y1 + y2) / 2
        current_coords = self.canvas.coords(car)
        print(current_coords)
        car_center_x = (current_coords[0] + current_coords[2]) / 2
        car_center_y = (current_coords[1] + current_coords[3]) / 2

        # Move horizontally until 20px before the target x position
        while abs(car_center_x - target_x) > 20:
            if car_center_x < target_x - 20:
                car_center_x += 1
            elif car_center_x > target_x + 20:
                car_center_x -= 1

            new_coords = [
                car_center_x - (current_coords[2] - current_coords[0]) / 2,
                car_center_y - (current_coords[3] - current_coords[1]) / 2,
                car_center_x + (current_coords[2] - current_coords[0]) / 2,
                car_center_y + (current_coords[3] - current_coords[1]) / 2,
            ]

            self.canvas.coords(car, new_coords)
            self.canvas.update()
            self.canvas.after(5)

        # Move vertically until aligned with the target y position
        while car_center_y != target_y:
            if car_center_y < target_y:
                car_center_y += 10
            elif car_center_y > target_y:
                car_center_y -= 10

            new_coords = [
                car_center_x - (current_coords[2] - current_coords[0]) / 2,
                car_center_y - (current_coords[3] - current_coords[1]) / 2,
                car_center_x + (current_coords[2] - current_coords[0]) / 2,
                car_center_y + (current_coords[3] - current_coords[1]) / 2,
            ]

            self.canvas.coords(car, new_coords)
            self.canvas.update()
            self.canvas.after(5)

        # Move the remaining 20px horizontally to enter the plaza
        while car_center_x != target_x:
            if car_center_x < target_x:
                car_center_x += 10
            elif car_center_x > target_x:
                car_center_x -= 10

            new_coords = [
                car_center_x - (current_coords[2] - current_coords[0]) / 2,
                car_center_y - (current_coords[3] - current_coords[1]) / 2,
                car_center_x + (current_coords[2] - current_coords[0]) / 2,
                car_center_y + (current_coords[3] - current_coords[1]) / 2,
            ]

            self.canvas.coords(car, new_coords)
            self.canvas.update()
            self.canvas.after(5)



if __name__=="__main__":
    # Iniciar la aplicación
    root = tk.Tk()
    app = ParkingGUI(root)
    root.mainloop()




    def car_movement(self, car, place):
        x1, y1, x2, y2 = self.plaza_coords[place]
        target_x = (x1 + x2) / 2
        target_y = (y1 + y2) / 2
        current_coords = self.canvas.coords(car)
        car_center_x = (current_coords[0] + current_coords[2]) / 2
        car_center_y = (current_coords[1] + current_coords[3]) / 2

        # Move horizontally until 20px before the target x position
        while abs(x2 - target_x) > 20:
            if car_center_x < target_x - 20:
                car_center_x += 1
            elif car_center_x > target_x + 20:
                car_center_x -= 1

            new_coords = [
                car_center_x - (current_coords[2] - current_coords[0]) / 2,
                car_center_y - (current_coords[3] - current_coords[1]) / 2,
                car_center_x + (current_coords[2] - current_coords[0]) / 2,
                car_center_y + (current_coords[3] - current_coords[1]) / 2,
            ]

            self.canvas.coords(car, new_coords)
            self.canvas.update()
            self.canvas.after(5)

        # Move vertically until aligned with the target y position
        while car_center_y != target_y:
            if car_center_y < target_y:
                car_center_y += 10
            elif car_center_y > target_y:
                car_center_y -= 10

            new_coords = [
                car_center_x - (current_coords[2] - current_coords[0]) / 2,
                car_center_y - (current_coords[3] - current_coords[1]) / 2,
                car_center_x + (current_coords[2] - current_coords[0]) / 2,
                car_center_y + (current_coords[3] - current_coords[1]) / 2,
            ]

            self.canvas.coords(car, new_coords)
            self.canvas.update()
            self.canvas.after(5)

        # Move the remaining 20px horizontally to enter the plaza
        while car_center_x != target_x:
            if car_center_x < target_x:
                car_center_x += 10
            elif car_center_x > target_x:
                car_center_x -= 10

            new_coords = [
                car_center_x - (current_coords[2] - current_coords[0]) / 2,
                car_center_y - (current_coords[3] - current_coords[1]) / 2,
                car_center_x + (current_coords[2] - current_coords[0]) / 2,
                car_center_y + (current_coords[3] - current_coords[1]) / 2,
            ]

            self.canvas.coords(car, new_coords)
            self.canvas.update()
            self.canvas.after(5)