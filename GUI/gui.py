#gui.py
from .window_setup import WindowSetup  # Importar la clase WindowSetup
from .widgets import Widgets  # Importar la lógica de widgets y análisis léxico

class GUI:
    def __init__(self, root):
        self.window_setup = WindowSetup(root)  # Configurar la ventana
        self.widgets = Widgets(root)  # Crear los widgets y manejar la lógica