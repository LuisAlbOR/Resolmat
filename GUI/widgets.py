import tkinter as tk
from tkinter import ttk
from .lexer_analyzer import LexerAnalyzer  # Importar la clase LexerAnalyzer
from .parser_analyzer import ParserAnalyzer  # Importar la clase ParserAnalyzer

class Widgets:
    def __init__(self, root):
        """
        Crea los widgets de la interfaz y maneja la interacción con los botones.
        """
        self.root = root
        self.lexer_analyzer = LexerAnalyzer()  # Crear una instancia del analizador léxico
        self.parser_analyzer = ParserAnalyzer()  # Crear una instancia del analizador sintáctico
        self.create_widgets()  # Crear los widgets de la interfaz

    def create_widgets(self):
        """
        Crea los widgets de la interfaz.
        """
        # Crear un contenedor principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Área de entrada de texto
        self.input_label = ttk.Label(self.main_frame, text="Entrada:")
        self.input_label.pack(anchor=tk.W)

        self.input_text = tk.Text(self.main_frame, height=10, width=70, bg="#3B4252", fg="#D8DEE9", insertbackground="#D8DEE9")
        self.input_text.pack(fill=tk.BOTH, expand=True)

        # Frame para los botones (horizontal)
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)

        # Botón para analizar léxicamente
        self.lexer_button = ttk.Button(self.button_frame, text="Análisis léxico", command=self.analyze_lexer)
        self.lexer_button.pack(side=tk.LEFT, padx=5)

        # Botón para analizar sintácticamente
        self.parser_button = ttk.Button(self.button_frame, text="Análisis sintáctico", command=self.analyze_parser)
        self.parser_button.pack(side=tk.LEFT, padx=5)

        # Área de salida de texto con barra de desplazamiento
        self.output_label = ttk.Label(self.main_frame, text="Salida:")
        self.output_label.pack(anchor=tk.W)

        # Crear un frame para el área de salida y la barra de desplazamiento
        self.output_frame = ttk.Frame(self.main_frame)
        self.output_frame.pack(fill=tk.BOTH, expand=True)

        # Área de salida de texto
        self.output_text = tk.Text(self.output_frame, height=10, width=70, bg="#3B4252", fg="#D8DEE9", state=tk.DISABLED)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Barra de desplazamiento
        self.scrollbar = ttk.Scrollbar(self.output_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Conectar la barra de desplazamiento con el área de texto
        self.output_text.configure(yscrollcommand=self.scrollbar.set)

    def analyze_lexer(self):
        """
        Método que se ejecuta cuando se presiona el botón "Análisis léxico".
        Procesa el texto de entrada con el lexer y muestra los resultados en el área de salida.
        """
        input_data = self.input_text.get("1.0", tk.END).strip()  # Obtener el texto de entrada
        self.output_text.config(state=tk.NORMAL)  # Habilitar la edición del área de salida
        self.output_text.delete("1.0", tk.END)  # Limpiar el área de salida

        if input_data:
            # Ejecutar el análisis léxico
            tokens, errors = self.lexer_analyzer.analyze(input_data)
            
            # Mostrar los tokens generados
            self.output_text.insert(tk.END, "Tokens generados:\n")
            for token in tokens:
                self.output_text.insert(tk.END, f"{token}\n")
            
            # Mostrar los errores (si los hay)
            if errors:
                self.output_text.insert(tk.END, "\nErrores encontrados:\n")
                for error in errors:
                    self.output_text.insert(tk.END, f"{error}\n")
        else:
            self.output_text.insert(tk.END, "Error: No se ha ingresado ningún texto.")

        self.output_text.config(state=tk.DISABLED)  # Deshabilitar la edición del área de salida

    def analyze_parser(self):
        """
        Método que se ejecuta cuando se presiona el botón "Análisis sintáctico".
        Procesa el texto de entrada con el parser y muestra los resultados en el área de salida.
        """
        input_data = self.input_text.get("1.0", tk.END).strip()  # Obtener el texto de entrada
        self.output_text.config(state=tk.NORMAL)  # Habilitar la edición del área de salida
        self.output_text.delete("1.0", tk.END)  # Limpiar el área de salida

        if input_data:
            # Ejecutar el análisis sintáctico
            result, errors = self.parser_analyzer.analyze(input_data)
            
            # Mostrar el resultado del análisis sintáctico
            if result is not None:
                self.output_text.insert(tk.END, "Análisis sintáctico exitoso:\n")
                self.output_text.insert(tk.END, f"{result}\n")
            
            # Mostrar los errores (si los hay)
            if errors:
                self.output_text.insert(tk.END, "\nErrores encontrados:\n")
                for error in errors:
                    self.output_text.insert(tk.END, f"{error}\n")
        else:
            self.output_text.insert(tk.END, "Error: No se ha ingresado ningún texto.")

        self.output_text.config(state=tk.DISABLED)  # Deshabilitar la edición del área de salida