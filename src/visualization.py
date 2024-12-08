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
aparcamiento = Aparcamiento(15)  # 15 plazas


# Interfaz Gráfica
class ParkingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aparcamiento Inteligente")
        self.root.geometry("1200x900")

        # Crear un canvas para el aparcamiento
        self.canvas = tk.Canvas(self.root, width=1200, height=900, bg="gray")
        self.canvas.pack(pady=20)

        # Botones
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack()

        # Añadir el botón para ver las plazas
        tk.Button(self.menu_frame, text="Ver Plazas", command=self.view_plazas).grid(row=0, column=1, padx=10)

        # Dibujar aparcamiento
        self.num_columnas = 5  # Número de columnas en el aparcamiento
        self.draw_parking()

        # Inicializar vehículo (un vehículo al principio)
        self.car = Vehiculo(plate="1234ABC", size="medium")
        
        # Aquí asignamos las coordenadas de la entrada para el coche morado
        self.car_x = 50  # Coordenada X de la entrada
        self.car_y = 50  # Coordenada Y de la entrada (ajustable)

        self.create_car()

        # Crear otro coche de color rosa con una ruta predeterminada
        self.rosa_car = Vehiculo(plate="5678DEF", size="medium")
        self.rosa_car_x = 50
        self.rosa_car_y = 480
        self.create_rosa_car()

        # Definir la ruta predeterminada del coche rosa
        self.rosa_car_route = [(840, 480),  # Posición inicial
                               (840, 480),  # Zona libre horizontal debajo de las plazas
                               (840, 560)   # Subida directa a P15
                              ]

        self.rosa_car_index = 0

        # Asociar las teclas para mover el coche principal
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)

        # Iniciar el movimiento del coche rosa
        self.move_rosa_car()

        # Variable para controlar el parpadeo de la plaza asignada
        self.blinking = False
        self.blinking_plaza = None

        # Asignar plaza al coche morado y comenzar a parpadear
        self.assign_parking_for_purple_car()

    def view_plazas(self):
        # Este es el método que se llama cuando se presiona el botón "Ver Plazas"
        print("Botón 'Ver Plazas' presionado")

        # Como ejemplo, vamos a cambiar el color de todas las plazas a amarillo cuando se presiona el botón
        for x1, y1, x2, y2 in self.plaza_coords:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", outline="white", width=4)

    def draw_parking(self):
        x, y = 150, 150
        width_plaza = 90
        height_plaza = 110

        # Aumentar la separación entre las plazas
        horizontal_gap = 80  # Mayor separación horizontal entre plazas
        vertical_gap = 80  # Mayor separación vertical entre filas de plazas

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
        salida_x1 = 1100  # Borde derecho
        salida_y1 = 400   # Centro vertical
        salida_x2 = 1200  # Borde derecho
        salida_y2 = 500   # Tamaño de la salida
        self.canvas.create_rectangle(salida_x1, salida_y1, salida_x2, salida_y2, fill="gray", outline="white", width=2)
        self.canvas.create_text(salida_x1 + (salida_x2 - salida_x1) / 2, salida_y1 + (salida_y2 - salida_y1) / 2, 
                                text="Salida", font=("Arial", 12), fill="white")

    def create_car(self):
        car_width = 60
        car_height = 40
        self.car_rect = self.canvas.create_rectangle(self.car_x, self.car_y, self.car_x + car_width, self.car_y + car_height, fill="purple", outline="black", tags=self.car.car_id)
        self.car_label = self.canvas.create_text(self.car_x + car_width / 2, self.car_y - 10, text=self.car.plate, font=("Arial", 10), fill="black")

    def create_rosa_car(self):
        car_width = 60
        car_height = 40
        self.rosa_car_rect = self.canvas.create_rectangle(self.rosa_car_x, self.rosa_car_y, self.rosa_car_x + car_width, self.rosa_car_y + car_height, fill="pink", outline="black", tags=self.rosa_car.car_id)
        # Crear la matrícula del coche rosa encima del coche
        self.rosa_car_label = self.canvas.create_text(self.rosa_car_x + car_width / 2, self.rosa_car_y - 10, text=self.rosa_car.plate, font=("Arial", 10), fill="black")

    def move_left(self, event):
        self.canvas.move(self.car_rect, -10, 0)
        self.canvas.move(self.car_label, -10, 0)
        self.car_x -= 10
        self.check_parking()

    def move_right(self, event):
        self.canvas.move(self.car_rect, 10, 0)
        self.canvas.move(self.car_label, 10, 0)
        self.car_x += 10
        self.check_parking()

    def move_up(self, event):
        self.canvas.move(self.car_rect, 0, -10)
        self.canvas.move(self.car_label, 0, -10)
        self.car_y -= 10
        self.check_parking()

    def move_down(self, event):
        self.canvas.move(self.car_rect, 0, 10)
        self.canvas.move(self.car_label, 0, 10)
        self.car_y += 10
        self.check_parking()

    def move_rosa_car(self):
        if self.rosa_car_index < len(self.rosa_car_route):
            target_x, target_y = self.rosa_car_route[self.rosa_car_index]

            if self.rosa_car_y < target_y:  # Mover hacia abajo
                self.canvas.move(self.rosa_car_rect, 0, 10)
                self.canvas.move(self.rosa_car_label, 0, 10)
                self.rosa_car_y += 10
            elif self.rosa_car_x < target_x:  # Mover hacia la derecha
                self.canvas.move(self.rosa_car_rect, 10, 0)
                self.canvas.move(self.rosa_car_label, 10, 0)
                self.rosa_car_x += 10
            elif self.rosa_car_x > target_x:  # Mover hacia la izquierda (si necesario)
                self.canvas.move(self.rosa_car_rect, -10, 0)
                self.canvas.move(self.rosa_car_label, -10, 0)
                self.rosa_car_x -= 10
            elif self.rosa_car_y > target_y:  # Mover hacia arriba
                self.canvas.move(self.rosa_car_rect, 0, -10)
                self.canvas.move(self.rosa_car_label, 0, -10)
                self.rosa_car_y -= 10

            # Actualizar el índice si se alcanza el objetivo
            if self.rosa_car_x == target_x and self.rosa_car_y == target_y:
                self.rosa_car_index += 1

            # Continuar moviendo cada 100 ms
            self.root.after(100, self.move_rosa_car)
        else:
            # Al llegar al destino, ocupar la plaza
            plaza = aparcamiento.plazas[14]  # Plaza 15 es el índice 14
            if not plaza.is_occupied:
                plaza.occupy(self.rosa_car)
                self.canvas.itemconfig(self.canvas.find_withtag(plaza.plaza_id), fill="red")
            
            # Asignar plaza al coche morado
            self.assign_parking_for_purple_car()

    def check_parking(self):
        if self.car_x >= 1100 and self.car_x <= 1200 and self.car_y >= 400 and self.car_y <= 500:
            # Mostrar el mensaje cuando el coche esté en la zona de salida
            messagebox.showinfo("¡Gracias por su visita!", "¡Vas a abandonar el aparcamiento! Gracias por su visita.")
            
            # Eliminar el coche completamente de la pantalla
            self.canvas.delete(self.car_rect)
            self.canvas.delete(self.car_label)
            self.car_rect = None
            self.car_label = None
            
        else:
            parked = False
            for i, (x1, y1, x2, y2) in enumerate(self.plaza_coords):
                if x1 < self.car_x < x2 and y1 < self.car_y < y2:
                    plaza = aparcamiento.plazas[i]
                    if plaza.is_occupied:
                        # Si la plaza está ocupada por otro vehículo, mostrar el aviso
                        if plaza.vehicle != self.car:  # Si el vehículo en la plaza no es el actual
                            messagebox.showwarning("AVISO!", f"Plaza {plaza.plaza_id} ocupada por otro vehículo. Elija otra plaza.")
                        else:
                            # Si el vehículo en la plaza es el mismo, no mostrar el aviso
                            parked = True
                    else:
                        # Si la plaza no está ocupada, aparcar el coche
                        plaza.occupy(self.car)
                        self.canvas.itemconfig(self.canvas.find_withtag(plaza.plaza_id), fill="red")
                        parked = True
                    break

            if not parked:
                for plaza in aparcamiento.plazas:
                    if plaza.is_occupied and plaza.vehicle == self.car:
                        plaza.vacate()
                        color = "blue" if plaza.is_disabled else "green"
                        self.canvas.itemconfig(self.canvas.find_withtag(plaza.plaza_id), fill=color)

    def assign_parking_for_purple_car(self):
    # Asignar la plaza 4 como objetivo para el coche morado
     self.blinking_plaza = aparcamiento.plazas[3]  # Plaza 4 (índice 3)
     self.blinking = True
     self.plaza_4_occupied_once = False  # Indicar que aún no se ha ocupado la plaza 4
     self.blink_plaza()  # Iniciar el parpadeo de la plaza

    def blink_plaza(self):
    # Asegurarse de que el parpadeo de la plaza 4 solo se detiene cuando se ocupa o cuando el coche se va
     if self.blinking and self.blinking_plaza:
        plaza_rect = self.canvas.find_withtag(self.blinking_plaza.plaza_id)
        current_color = self.canvas.itemcget(plaza_rect, "fill")

        # Si la plaza está ocupada por algún coche (incluido el coche morado), detener el parpadeo y ponerla en rojo
        if self.blinking_plaza.is_occupied and not self.plaza_4_occupied_once:
            self.canvas.itemconfig(plaza_rect, fill="red")
            self.blinking = False  # Detener el parpadeo
            self.plaza_4_occupied_once = True  # Marcar que la plaza fue ocupada al menos una vez
        elif not self.blinking_plaza.is_occupied:
            # Si la plaza no está ocupada, alternar entre naranja ámbar
            new_color = "orange" if current_color != "orange" else "green"
            self.canvas.itemconfig(plaza_rect, fill=new_color)
            self.root.after(500, self.blink_plaza)  # Continuar el parpadeo cada 500 ms

    def check_parking(self):
    # Comprobar si el coche morado está en la zona de salida
     if 1100 <= self.car_x <= 1200 and 400 <= self.car_y <= 500:
        messagebox.showinfo("¡Gracias por su visita!", "¡Vas a abandonar el aparcamiento! Gracias por su visita.")
        
        # Eliminar el coche morado completamente de la pantalla
        self.canvas.delete(self.car_rect)
        self.canvas.delete(self.car_label)
        self.car_rect = None
        self.car_label = None

        # Si la plaza 4 estaba ocupada por el coche morado, desocuparla
        for plaza in aparcamiento.plazas:
            if plaza.is_occupied and plaza.vehicle == self.car:
                plaza.vacate()
                color = "blue" if plaza.is_disabled else "green"
                self.canvas.itemconfig(self.canvas.find_withtag(plaza.plaza_id), fill=color)

        # Detener el parpadeo independientemente del estado
        self.blinking = False

        return  # Evitar que siga ejecutando el código de aparcar

     parked = False
     for i, (x1, y1, x2, y2) in enumerate(self.plaza_coords):
        if x1 < self.car_x < x2 and y1 < self.car_y < y2:
            plaza = aparcamiento.plazas[i]
            if plaza.is_occupied:
                # Si la plaza está ocupada por otro vehículo, mostrar el aviso
                if plaza.vehicle != self.car:  # Si el vehículo en la plaza no es el coche morado
                    messagebox.showwarning("AVISO!", f"Plaza {plaza.plaza_id} ocupada por otro vehículo. Elija otra plaza.")
                else:
                    # Si el vehículo en la plaza es el coche morado, no mostrar el aviso
                    parked = True
            else:
                # Si la plaza no está ocupada, aparcar el coche
                plaza.occupy(self.car)
                self.canvas.itemconfig(self.canvas.find_withtag(plaza.plaza_id), fill="red")
                parked = True

                # Si aparca en una plaza distinta de la 4, detener el parpadeo y mostrar el mensaje
                if plaza != self.blinking_plaza:
                    self.blinking = False  # Detener el parpadeo de la plaza 4
                    messagebox.showwarning("¡Aviso!", "Esta no es tu plaza, dirígete a la adjudicada (Plaza 4).")

                # Si aparca en la plaza 4, marcarla como ocupada definitivamente
                elif plaza == self.blinking_plaza:
                    self.blinking = False
                    self.plaza_4_occupied_once = True

            break

     # Si el coche morado no ha aparcado en ninguna plaza
     if not parked:
        for plaza in aparcamiento.plazas:
            if plaza.is_occupied and plaza.vehicle == self.car:
                plaza.vacate()
                color = "blue" if plaza.is_disabled else "green"
                self.canvas.itemconfig(self.canvas.find_withtag(plaza.plaza_id), fill=color)

     # Si la plaza 4 se ha desocupado, reiniciar el parpadeo si no ha sido ocupada
     if self.blinking_plaza and not self.blinking_plaza.is_occupied and not self.plaza_4_occupied_once:
        self.blinking = True
        self.blink_plaza()

if __name__=="__main__":
    # Iniciar la aplicación
    root = tk.Tk()
    app = ParkingGUI(root)
    root.mainloop()