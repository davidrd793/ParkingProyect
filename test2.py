import threading
import time

def tarea(nombre, duracion):
    print(f"Inicio de la tarea {nombre}")
    time.sleep(duracion)
    print(f"Fin de la tarea {nombre}")

# Crear hilos
hilo1 = tarea('Hilo1', 2)
hilo2 = tarea('Hilo2', 3)

print("Todos los hilos han terminado.")