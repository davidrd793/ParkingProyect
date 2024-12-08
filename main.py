from src import login
import tkinter as tk


#Initialization of the program, execute this file to run the program

if __name__=="__main__":
    root = tk.Tk()
    app = login.LoginInterface(root)
    login.LoginInterface(root)
    root.mainloop()
