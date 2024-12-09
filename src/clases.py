
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
    def __init__(self, num_plazas, num_columnas= 6):
        self.num_columnas = num_columnas
        self.plazas = [
            Plaza("1") for i in range(num_plazas)
        ]
        self.vehicles = []


# Configuración inicial
aparcamiento = Aparcamiento(15)  # 15 plazas

