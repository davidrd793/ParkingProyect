import tkinter as tk
from tkinter import messagebox
import random
import threading
import time

matriculas = ['1234ABC', '1234BCD']
places = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12', 'P13', 'P14', 'P15']


# System classes
class Place:
    def __init__(self, place_id, size="medium", is_disabled=False):
        self.place_id = place_id
        self.size = size
        self.is_disabled = is_disabled
        self.is_occupied = False
        self.vehicle = None

    def occupy(self, vehicle):
        if self.is_occupied:
            raise ValueError(f"Plaza {self.place_id} ya está ocupada")
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


class Parking:
    def __init__(self, num_places, column_number=6):
        self.column_number = column_number
        self.places = [
            Place(f"P{i+1}", size="medium" if i % 3 != 0 else "large", is_disabled=(i < 3)) for i in range(num_places)
        ]
        self.vehicles = []


# Configuración inicial
parking = Parking(15)


class ParkingGUI:
    def __init__(self, root):
        #Initial window configuration
        self.root = root
        self.root.title("parking Inteligente")
        self.root.geometry("800x900+20+20")
        self.root.maxsize(width=1200, height=750)
        self.root.minsize(width=1200, height=750) 

        # Crear un canvas para el parking
        self.canvas = tk.Canvas(self.root, width=1000, height=600, bg="gray")
        self.canvas.grid(column=0, row=0, padx=100)

        self.button_container = tk.Frame(self.root, width=1000, height=100, bg='lightblue')
        self.button_container.grid(column=0, row=1, pady=25)

        #Command del boton 1 llama a la función que añade un coche al parking
        self.add_car_button = tk.Button(self.button_container, text='Add Car', command=self.generate_car).grid(column=0, row=0, padx=(200, 100), pady=(20, 20)) 


        # Dibujar parking
        self.column_number = 5
        self.draw_parking()

    def draw_parking(self):
        x, y = 150, 100
        width_plaza = 80
        height_plaza = 100

        horizontal_gap = 60
        vertical_gap = 60
        global places

        self.plaza_coords = {}
        for i, plaza in enumerate(parking.places):
            color = "blue" if plaza.is_disabled else "green"
            self.plaza_coords[places[i]] = (x, y, x + width_plaza, y + height_plaza)
            self.canvas.create_rectangle(x, y, x + width_plaza, y + height_plaza, fill=color, outline="white", width=4, tags=plaza.place_id)
            self.canvas.create_text(x + width_plaza / 2, y + height_plaza / 2, text=plaza.place_id, font=("Arial", 10), fill="white")

            x += width_plaza + horizontal_gap
            if (i + 1) % self.column_number == 0:
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
        threading.Thread(target=self.car_movement, args=(car_vis, assigned_place)).start()
    
    def assign_place(self):
        selected_place = random.choice(places)
        places.remove(selected_place)
        return selected_place
    
    def car_movement(self, car, place):
        x1, y1, x2, y2 = self.plaza_coords[place]
        place_center_x = (x1 + x2) / 2
        place_center_y = (y1 + y2) / 2

        current_coords = self.canvas.coords(car)
        car_x1, car_y1, car_x2, car_y2 = current_coords

        # Move horizontally until 20px before the target x position
        while abs(car_x2 - x1) > 10:
            if car_x2 < x1 - 10:
                movement_x = 2

            self.canvas.move(car, movement_x, 0)
            self.canvas.update()
            self.canvas.after(10)

            current_coords = self.canvas.coords(car)
            car_x1, car_y1, car_x2, car_y2 = current_coords

        # Move vertically until aligned with the target y position
        while abs((car_y1 + car_y2) / 2 - place_center_y) > 1:
            if (car_y1 + car_y2) / 2 < place_center_y:
                movement_y = 2

            self.canvas.move(car, 0, movement_y)
            self.canvas.update()
            self.canvas.after(10)

            current_coords = self.canvas.coords(car)
            car_x1, car_y1, car_x2, car_y2 = current_coords

        # Move the remaining 20px horizontally to enter the plaza
        while abs((car_x1 + car_x2) / 2 - place_center_x) > 1:
            if (car_x1 + car_x2) / 2 < place_center_x:
                movement_x = 2

            self.canvas.move(car, movement_x, 0)
            self.canvas.update()
            self.canvas.after(10)

            current_coords = self.canvas.coords(car)
            car_x1, car_y1, car_x2, car_y2 = current_coords
    
        # Wait for a random time between 2 and 10 seconds
        wait_time= random.randint(2, 10)
        time.sleep(wait_time)

        # Move towards the exit
        exit_x1, exit_y1, exit_x2, exit_y2 = 900, 500, 1000, 600
        exit_center_x = (exit_x1 + exit_x2) / 2
        exit_center_y = (exit_y1 + exit_y2) / 2

        # Move horizontally towards the exit
        for i in range(37):
            if (car_x1 + car_x2) / 2 < exit_center_x:
                movement_x = 2

            self.canvas.move(car, movement_x, 0)
            self.canvas.update()
            self.canvas.after(10)

            current_coords = self.canvas.coords(car)
            car_x1, car_y1, car_x2, car_y2 = current_coords

        # Move vertically towards the exit
        while abs((car_y1 + car_y2) / 2 - exit_center_y) > 1:
            if (car_y1 + car_y2) / 2 < exit_center_y:
                movement_y = 2

            self.canvas.move(car, 0, movement_y)
            self.canvas.update()
            self.canvas.after(10)

            current_coords = self.canvas.coords(car)
            car_x1, car_y1, car_x2, car_y2 = current_coords
        
        while abs((car_x1 + car_x2) / 2 - exit_center_x) > 1:
            if (car_x1 + car_x2) / 2 < exit_center_x:
                movement_x = 2

            self.canvas.move(car, movement_x, 0)
            self.canvas.update()
            self.canvas.after(10)

            current_coords = self.canvas.coords(car)
            car_x1, car_y1, car_x2, car_y2 = current_coords

        


        # Remove the car once it reaches the exit
        self.canvas.delete(car)




if __name__=="__main__":
    # Iniciar la aplicación
    root = tk.Tk()
    app = ParkingGUI(root)
    root.mainloop()

