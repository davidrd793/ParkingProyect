import threading
import time

def tarea(nombre, duracion):
    print(f"Inicio de la tarea {nombre}")
    time.sleep(duracion)
    print(f"Fin de la tarea {nombre}")

# Crear hilos
hilo1 = threading.Thread(target=tarea, args=("Hilo 1", 2))
hilo2 = threading.Thread(target=tarea, args=("Hilo 2", 3))

# Iniciar hilos
hilo1.start()
hilo2.start()

# Esperar a que los hilos terminen
hilo1.join()
hilo2.join()

print("Todos los hilos han terminado.")