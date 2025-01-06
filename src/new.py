import tkinter as tk
import random
import threading
import time
from datetime import datetime
import json
import os

DATABASE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataBase", "cars.json")

matriculas = ['7601YUD', '9337JIH', '3560ANE', '8201QAL', '1487PRM', '3716KGV', '3208CJV', '8057HMF', '7121DGQ', '4523ZDP', 
 '9397SYK', '1512QFP', '0178TKQ', '9804AYJ', '3624EUH', '4477LKW', '0028JVC', '9881JWY', '4197SNA', '9291SET', 
 '8060ZHO', '4716QKX', '6802CPT', '2841NDY', '4608QRL', '7524LRK', '3955FTF', '7870FNH', '5067FSD', '4800OBO', 
 '7366YGC', '3041QQY', '3077LGS', '5398YJB', '8817EQY', '7860DWA', '6549RUS', '8912ZBL', '7689TBW', '6508USD']

places = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12', 'P13', 'P14', 'P15']	
disabled_places = ['P1', 'P2', 'P3']
non_disabled_places = ['P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12', 'P13', 'P14', 'P15']
disabled_cars = ['8817EQY', '2841NDY']


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

        # Contenedor para la visualización
        self.canvas = tk.Canvas(self.root, width=1000, height=600, bg="gray")
        self.canvas.grid(column=0, row=0, padx=100)

        #Contenedor para el botón
        self.button_container = tk.Frame(self.root, width=1000, height=100)
        self.button_container.grid(column=0, row=1, pady=25)
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
        plate, assigned_place, comprobador = self.assign_place()
        print(f"Coche con matrícula {plate} ha entrado al parking, su plaza asignada es {assigned_place}")
        car = Vehicle(plate, assigned_place)

        # Save the car data to the database
        data_to_save = {
            "matrícula": plate,
            "plaza": assigned_place,
            "hora_aparcamiento": None,
        }
        
        global DATABASE_FILE

        try:
            with open(DATABASE_FILE, 'r') as file:
                cars = json.load(file)
        
        except (FileNotFoundError, json.JSONDecodeError):
            cars = []
        
        cars.append(data_to_save)

        with open(DATABASE_FILE, 'w') as file:
            json.dump(cars, file, indent=4)

        car_vis = self.canvas.create_rectangle(50, 50, 50+car.size[0], 50+car.size[1], fill='blue', outline="black",width = 2)
        threading.Thread(target=self.car_movement, args=(car_vis, assigned_place, plate)).start()
    
    def random_plate(self):
        matricula = random.choice(matriculas)
        matriculas.remove(matricula)
        return matricula
    
    def assign_place(self):
        plate = self.random_plate()
        
        if not places:
            print("Parking lleno")
            return None, None
        
        if plate in disabled_cars:
            comprobador = True
            selected_place = random.choice(disabled_places)
            disabled_places.remove(selected_place)
            places.remove(selected_place)
            return plate, selected_place, comprobador
        
        else:
            comprobador = False
            selected_place = random.choice(non_disabled_places)
            places.remove(selected_place)
            non_disabled_places.remove(selected_place)
            return plate, selected_place, comprobador

    def car_movement(self, car, place, plate, comprobador=False):
        x1, y1, x2, y2 = self.plaza_coords[place]
        place_center_x = (x1 + x2) / 2
        place_center_y = (y1 + y2) / 2

        current_coords = self.canvas.coords(car)
        car_x1, car_y1, car_x2, car_y2 = current_coords

        # Move horizontally until 20px before the target x position
        print(f"Coche de matrícula {plate}, vaya recto")
        while abs(car_x2 - x1) > 10:
            if car_x2 < x1 - 10:
                movement_x = 2

            self.canvas.move(car, movement_x, 0)
            self.canvas.update()
            self.canvas.after(int(10))

            current_coords = self.canvas.coords(car)
            car_x1, car_y1, car_x2, car_y2 = current_coords

        # Move vertically until aligned with the target y position
        print(f"Coche de matrícula {plate}, gire hacia la derecha y siga recto")
        while abs((car_y1 + car_y2) / 2 - place_center_y) > 1:
            if (car_y1 + car_y2) / 2 < place_center_y:
                movement_y = 2

            self.canvas.move(car, 0, movement_y)
            self.canvas.update()
            self.canvas.after(int(10))

            current_coords = self.canvas.coords(car)
            car_x1, car_y1, car_x2, car_y2 = current_coords

        # Move the remaining 20px horizontally to enter the plaza
        print(f"Coche de matrícula {plate}, la plaza a su izquierda es la que se le fue asignada")
        while abs((car_x1 + car_x2) / 2 - place_center_x) > 1:
            if (car_x1 + car_x2) / 2 < place_center_x:
                movement_x = 2

            self.canvas.move(car, movement_x, 0)
            self.canvas.update()
            self.canvas.after(int(10))

            current_coords = self.canvas.coords(car)
            car_x1, car_y1, car_x2, car_y2 = current_coords
    
        # Update the database with the parking time
        global DATABASE_FILE
        with open(DATABASE_FILE, 'r') as file:
            cars = json.load(file)
            for i in cars:
                if i["matrícula"] == plate and i["hora_aparcamiento"] is None:
                    i["hora_aparcamiento"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(DATABASE_FILE, 'w') as file:
            json.dump(cars, file, indent=4)
        
        
        # Wait 2 seconds parked
        wait_time= 2
        time.sleep(wait_time)


        # Exit coordenates
        exit_x1, exit_y1, exit_x2, exit_y2 = 900, 500, 1000, 600
        exit_center_x = (exit_x1 + exit_x2) / 2
        exit_center_y = (exit_y1 + exit_y2) / 2

        # Move horizontally towards the exit
        print(f"Coche de matrícula {plate}, salga del aparcamiento por delante")
        for i in range(37):
            if (car_x1 + car_x2) / 2 < exit_center_x:
                movement_x = 2

            self.canvas.move(car, movement_x, 0)
            self.canvas.update()
            self.canvas.after(int(10))

            current_coords = self.canvas.coords(car)
            car_x1, car_y1, car_x2, car_y2 = current_coords

        # Move vertically towards the exit
        print(f'Coche de matrícula {plate} gire a la derecha y siga recto hasta el final del pasillo')
        while abs((car_y1 + car_y2) / 2 - exit_center_y) > 1:
            if (car_y1 + car_y2) / 2 < exit_center_y:
                movement_y = 2

            self.canvas.move(car, 0, movement_y)
            self.canvas.update()
            self.canvas.after(int(10))

            current_coords = self.canvas.coords(car)
            car_x1, car_y1, car_x2, car_y2 = current_coords
        
        print(f'Coche de matrícula {plate}, gire a la izquierda y avance hasta la salida')
        while abs((car_x1 + car_x2) / 2 - exit_center_x) > 1:
            if (car_x1 + car_x2) / 2 < exit_center_x:
                movement_x = 2

            self.canvas.move(car, movement_x, 0)
            self.canvas.update()
            self.canvas.after(int(10))

            current_coords = self.canvas.coords(car)
            car_x1, car_y1, car_x2, car_y2 = current_coords
        
        print(f'Coche de matrícula {plate} ha salido del parking')
 
        # Remove the car once it reaches the exit both in the database and the GUI
        with open(DATABASE_FILE, 'r') as file:
            cars = json.load(file)
            for i in cars:
                if i["matrícula"] == plate:
                    cars.remove(i)
        
        with open(DATABASE_FILE, 'w') as file:
            json.dump(cars, file, indent=4)

        self.canvas.delete(car)
        places.append(place)
        if comprobador:
            disabled_places.append(place)
        else:
            non_disabled_places.append(place)
        matriculas.append(plate)



if __name__=="__main__":
    # Iniciar la aplicación
    root = tk.Tk()
    app = ParkingGUI(root)
    root.mainloop()

