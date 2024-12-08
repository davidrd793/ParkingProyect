import tkinter as tk
from tkinter import messagebox
import json
from src import visualization
import os

# Ruta dinámica hacia dataBase/users.json
DATABASE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataBase", "users.json")


# Clase Usuario
class Usuario:
    def __init__(self, nombre, email, contraseña, matricula, minusvalia):
        self.nombre = nombre
        self.email = email
        self.contraseña = contraseña
        self.matricula = matricula
        self.minusvalia = minusvalia


    def to_dict(self):
        """Convierte el objeto Usuario en un diccionario."""
        return {
            "nombre": self.nombre,
            "email": self.email,
            "contraseña": self.contraseña,
            "matricula": self.matricula,
            "minusvalia": self.minusvalia
        }

    @staticmethod
    def from_dict(data):
        """Crea un objeto Usuario a partir de un diccionario."""
        return Usuario(
            nombre=data["nombre"],
            email=data["email"],
            contraseña=data["contraseña"],  # Ya cifrada
            matricula=data["matricula"],
            minusvalia=data["minusvalia"],
        )


# Clase BaseDeDatos
class BaseDeDatos:
    def __init__(self, archivo):
        self.archivo = archivo
        self.usuarios = self.cargar_usuarios()

    def cargar_usuarios(self):
        """Carga los usuarios desde el archivo JSON."""
        try:
            with open(self.archivo, "r") as f:
                datos = json.load(f)
                return [Usuario.from_dict(u) for u in datos]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def guardar_usuarios(self):
        """Guarda los usuarios en el archivo JSON."""
        with open(self.archivo, "w") as f:
            json.dump([u.to_dict() for u in self.usuarios], f, indent=4)

    def agregar_usuario(self, usuario):
        """Agrega un usuario a la base de datos."""
        self.usuarios.append(usuario)
        self.guardar_usuarios()

    def buscar_usuario(self, email):
        """Busca un usuario por email."""
        for usuario in self.usuarios:
            if usuario.email == email:
                return usuario
        return None


# Clase Autenticación
class Autenticacion:
    def __init__(self, db):
        self.db = db

    def registrar_usuario(self, nombre, email, contraseña, matricula, minusvalia):
        """Registra un nuevo usuario en el sistema."""
        if self.db.buscar_usuario(email):
            return False, "El email ya está registrado."

        nuevo_usuario = Usuario(nombre, email, contraseña, matricula, minusvalia)
        self.db.agregar_usuario(nuevo_usuario)
        return True, "Usuario registrado exitosamente."

    def iniciar_sesion(self, email, contraseña):
        """Inicia sesión verificando las credenciales."""
        usuario = self.db.buscar_usuario(email)
        if not usuario:
            return False, "Usuario no encontrado."

        if usuario.contraseña == contraseña:
            return True, f"Bienvenido, {usuario.nombre}."
        else:
            return False, "Contraseña incorrecta."


# Interfaz gráfica con Tkinter
class LoginInterface:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x1000")
        self.root.title("Sistema de Login")
        self.db = BaseDeDatos(DATABASE_FILE)
        self.auth = Autenticacion(self.db)
        self.mostrar_login()

    def mostrar_login(self):
        """Pantalla de inicio de sesión."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Inicio de Sesión", font=("Arial", 24)).pack(pady=10)
        tk.Label(self.root, text="Email:").pack()
        email_entry = tk.Entry(self.root)
        email_entry.pack()
        tk.Label(self.root, text="Contraseña:").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def iniciar_sesion():
            email = email_entry.get()
            contraseña = password_entry.get()
            exito, mensaje = self.auth.iniciar_sesion(email, contraseña)
            messagebox.showinfo("Inicio de Sesión", mensaje)
            if exito:
                self.show_visualization()

        tk.Button(self.root, text="Iniciar Sesión", command=iniciar_sesion).pack(pady=10)
        tk.Button(self.root, text="Registrarse", command=self.mostrar_registro).pack()

    def mostrar_registro(self):
        """Pantalla de registro con validaciones."""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Títulos y campos de entrada
        tk.Label(self.root, text="Registro de Usuario", font=("Arial", 24)).pack(pady=10)
        tk.Label(self.root, text="Nombre:").pack()
        nombre_entry = tk.Entry(self.root)
        nombre_entry.pack()
        tk.Label(self.root, text="Email:").pack()
        email_entry = tk.Entry(self.root)
        email_entry.pack()
        tk.Label(self.root, text="Contraseña:").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()
        tk.Label(self.root, text="Matrícula:").pack()
        matricula_entry = tk.Entry(self.root)
        matricula_entry.pack()

        # Checkbutton para minusvalía
        minusvalia_var = tk.BooleanVar()
        tk.Label(self.root, text="¿Tienes minusvalía?").pack()
        tk.Checkbutton(self.root, variable=minusvalia_var).pack()
        
        #Autenticación de minusvalía
        if minusvalia_var is True:
            messagebox.showinfo("Pues agarrame el pepino") 
        # Función para validar los datos
        def validar_datos():
            nombre = nombre_entry.get()
            email = email_entry.get()
            contraseña = password_entry.get()
            matricula = matricula_entry.get()
            minusvalia = minusvalia_var.get()
            # Validaciones
            if not nombre.isalpha():
                messagebox.showerror("Error", "El nombre solo debe contener letras.")
                return False
            if not ("@" in email and "." in email.split("@")[-1]):
                messagebox.showerror("Error", "El email no tiene un formato válido.")
                return False
            if len(contraseña) < 9:
                messagebox.showerror("Error", "La contraseña debe tener al menos 9 caracteres.")
                return False
            if not (len(matricula) == 7 and matricula[:4].isdigit() and matricula[4:].isalpha()):
                messagebox.showerror("Error", "La matrícula debe ser de 4 números seguidos de 3 letras.")
                return False

            return True

        # Función de registro con validación
        def registrar():
            if validar_datos():
                nombre = nombre_entry.get()
                email = email_entry.get()
                contraseña = password_entry.get()
                matricula = matricula_entry.get()
                minusvalia = minusvalia_var.get()
                exito, mensaje = self.auth.registrar_usuario(
                    nombre, email, contraseña, matricula, minusvalia
                )
                messagebox.showinfo("Registro", mensaje)
                if exito:
                    self.mostrar_login()

        # Botones
        tk.Button(self.root, text="Registrar", command=registrar).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.mostrar_login).pack()


    def show_visualization(self):
        """Pantalla de bienvenida tras iniciar sesión."""
        for widget in self.root.winfo_children():
            widget.destroy()
        root = tk.Tk()
        visualization.ParkingGUI(root)