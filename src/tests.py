import tkinter as tk

# Crear la ventana principal
root = tk.Tk()
root.geometry("800x600")  # Tamaño inicial de la ventana

# Crear widgets que se ajusten
frame = tk.Frame(root, bg="blue")
frame.pack(fill=tk.BOTH, expand=True)  # El Frame ocupa todo el espacio disponible

label = tk.Label(frame, text="Este texto se adapta al tamaño de la ventana", bg="lightblue")
label.pack(fill=tk.BOTH, expand=True)  # El Label también se ajusta

root.mainloop()
