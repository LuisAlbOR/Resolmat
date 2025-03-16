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