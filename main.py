#main.py
import tkinter as tk
from GUI.gui import GUI

def main():
    # Crear la ventana principal
    root = tk.Tk()

    # Crear la interfaz gráfica
    app = GUI(root)

    # Ejecutar el bucle principal de la interfaz
    root.mainloop()

if __name__ == "__main__":
    main()
    
# genera la siguiente matriz (+ 2 x + 3 y - 1 z = 10)(+ 2 y + 3 x - 1 z = 12)(+ 1 x + 1 y + 1 z = 5)
# genera la siguiente matriz (+ 2 x + y - 1 z = 10)