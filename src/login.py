import tkinter as tk
from tkinter import messagebox
import json
from src import visualization
import os

# Ruta dinámica hacia dataBase/users.json
DATABASE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataBase", "users.json")


#Clase para definir usuario así como su traducción a formato json
class User:
    def __init__(self, name: str, email: str, password: str, plate: str, disability: bool) -> None:
        self.name = name
        self.email = email
        self.password = password
        self.plate = plate
        self.disability = disability


    def to_dict(self) -> dict: 
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "plate": self.plate,
            "disability": self.disability
        }

    @staticmethod
    def from_dict(data: dict):
        return User(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            plate=data["plate"],
            disability=data["disability"],
        )


class DataBase:
    def __init__(self, file) -> None:
        self.file = file
        self.users = self.load_users()

    def load_users(self) -> list:
        try:
            with open(self.file, "r") as f:
                all_data = json.load(f)
                return [User.from_dict(single_data) for single_data in all_data]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def save_users(self) -> None:
        with open(self.file, "w") as f:
            json.dump([single_data.to_dict() for single_data in self.users], f, indent=4)

    def add_user(self, user) -> None:
        self.users.append(user)
        self.save_users()

    def search_user(self, email):
        for user in self.users:
            if user.email == email:
                return user
        return None


class Autenticacion:
    def __init__(self, db) -> None:
        self.db = db

    def user_registry(self, name: str, email: str, password: str, plate: str, disability: bool) -> tuple:
        if self.db.search_user(email):
            return False, "El email ya está registrado."

        new_user = User(name, email, password, plate, disability)
        self.db.add_user(new_user)
        return True, "Usuario registrado exitosamente."

    def log_in(self, email: str, password: str) -> tuple:
        """Inicia sesión verificando las credenciales."""
        user = self.db.search_user(email)
        if not user:
            return False, "Usuario no encontrado."

        if user.password == password:
            return True, f"Bienvenido, {user.name}."
        else:
            return False, "Contraseña incorrecta."


# Interfaz gráfica con Tkinter
class LoginInterface:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.geometry("1000x1000")
        self.root.title("Sistema de Login")
        self.db = DataBase(DATABASE_FILE)
        self.auth = Autenticacion(self.db)
        self.show_login_screen()

    def show_login_screen(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Inicio de Sesión", font=("Arial", 24)).pack(pady=10)
        tk.Label(self.root, text="Email:").pack()
        email_entry = tk.Entry(self.root)
        email_entry.pack()
        tk.Label(self.root, text="Contraseña:").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        email_entry.bind("<Return>", lambda event: log_in())
        password_entry.bind("<Return>", lambda event: log_in())
        
        def log_in() -> None:
            email = email_entry.get()
            password = password_entry.get()
            success, message = self.auth.log_in(email, password)
            messagebox.showinfo("Inicio de Sesión", message)
            if success:
                self.show_visualization()

        tk.Button(self.root, text="Iniciar Sesión", command=log_in).pack(pady=10)
        tk.Button(self.root, text="Registrarse", command=self.sign_in_screen).pack()

    def sign_in_screen(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

        # Títulos y campos de entrada
        tk.Label(self.root, text="Registro de usuario", font=("Arial", 24)).pack(pady=10)
        tk.Label(self.root, text="Nombre:").pack()
        name_entry = tk.Entry(self.root)
        name_entry.pack()
        tk.Label(self.root, text="Email:").pack()
        email_entry = tk.Entry(self.root)
        email_entry.pack()
        tk.Label(self.root, text="Contraseña:").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()
        tk.Label(self.root, text="Matrícula:").pack()
        plate_entry = tk.Entry(self.root)
        plate_entry.pack()

        # Checkbutton para minusvalía
        disability_var = tk.BooleanVar()
        tk.Label(self.root, text="¿Tiene usted alguna minusvalía?").pack()

        def show_disability_message() -> None:
            if disability_var.get():
                messagebox.showinfo("IMPORTANTE", "Como medida temporal, para autenticar tu minusvalía debes mandarle un correo a administrador@gmail.com con un documento que acredite tu minusvalía. En un futuro próximo se añadirán formas más directas de autenticar la minusvalía. Lamentamos las molestias")

        tk.Checkbutton(self.root, text="Si", 
               variable=disability_var, 
               command=show_disability_message).pack()
        
        # Vincular tecla ENTER
        name_entry.bind("<Return>", lambda event: sign_in())
        email_entry.bind("<Return>", lambda event: sign_in())
        password_entry.bind("<Return>", lambda event: sign_in())
        plate_entry.bind("<Return>", lambda event: sign_in())     
          
        # Función para validar los all_data
        def verify_data() -> bool:
            name = name_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            plate = plate_entry.get()
            disability = disability_var.get()
            # Validaciones
            if not name.isalpha():
                messagebox.showerror("Error", "El nombre solo debe contener letras.")
                return False
            if not ("@" in email and "." in email.split("@")[-1]):
                messagebox.showerror("Error", "El email no tiene un formato válido.")
                return False
            if len(password) < 9:
                messagebox.showerror("Error", "La contraseña debe tener al menos 9 caracteres.")
                return False
            if not (len(plate) == 7 and plate[:4].isdigit() and plate[4:].isalpha()):
                messagebox.showerror("Error", "La matrícula debe ser de 4 números seguidos de 3 letras.")
                return False

            return True

        # Función de registro con validación
        def sign_in() -> None:
            if verify_data():
                name = name_entry.get()
                email = email_entry.get()
                password = password_entry.get()
                plate = plate_entry.get()
                disability = disability_var.get()
                success, message = self.auth.user_registry(
                    name, email, password, plate, disability
                )
                messagebox.showinfo("Registro", message)
                if success:
                    self.show_login_screen()

        # Botones
        tk.Button(self.root, text="Registrar", command=sign_in).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.show_login_screen).pack()


    def show_visualization(self) -> None: #Redirige a la visualización de la app en sí
        for widget in self.root.winfo_children():
            widget.destroy()
        app = visualization.ParkingGUI(self.root)
