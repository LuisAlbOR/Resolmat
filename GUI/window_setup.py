#windows_setup.py
import tkinter as tk
from tkinter import ttk

class WindowSetup:
    def __init__(self, root):
        """
        Configura la ventana principal con un fondo oscuro y estilos personalizados.
        """
        self.root = root
        self.setup_window()

    def setup_window(self):
        """
        Aplica la configuración de la ventana y los estilos personalizados.
        """
        self.root.title("Compilador")
        self.root.geometry("600x400")
        self.root.configure(bg="#2E3440")  # Fondo oscuro

        # Configurar estilos personalizados
        self.setup_styles()

    def setup_styles(self):
        """
        Configura los estilos personalizados para los widgets.
        """
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Usar un tema que permita personalización

        # Estilos personalizados
        self.style.configure("TFrame", background="#2E3440")  # Fondo del frame
        self.style.configure("TLabel", background="#2E3440", foreground="#D8DEE9")  # Etiquetas
        self.style.configure("TButton", background="#4C566A", foreground="#D8DEE9")  # Botones
        self.style.configure("TText", background="#3B4252", foreground="#D8DEE9")  # Áreas de texto