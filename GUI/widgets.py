import threading
import tkinter as tk
from tkinter import ttk
from .error_manager import ErrorManager
from .lexer_analyzer import LexerAnalyzer  # Importar la clase LexerAnalyzer
from .parser_analyzer import ParserAnalyzer  # Importar la clase ParserAnalyzer

class Widgets:
    def __init__(self, root):
        """
        Crea los widgets de la interfaz y maneja la interacción con los botones.
        """
        self.root = root
        self.lexer_analyzer = LexerAnalyzer()  # Crear una instancia del analizador léxico
        self.error_manager = ErrorManager()  # Crear una instancia del administrador de errores
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

        # Configurar el tag para subrayar errores en rojo
        self.input_text.tag_config("lexical_error", foreground="red")  # Errores léxicos
        self.input_text.tag_config("syntax_error", foreground="orange")  # Errores sintácticos
        # self.input_text.tag_config("semantic_error", foreground="yellow")  # Errores semánticos 

        # Vincular el evento KeyRelease al método de análisis en tiempo real
        self.input_text.bind("<KeyRelease>", self.analyze_input_real_time)

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

        # Configurar el color rojo para los errores
        self.output_text.tag_config("error", foreground="skyblue")

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
            # Limpiar errores anteriores
            self.error_manager.clear_errors()

            # Ejecutar el análisis léxico
            tokens, errors = self.lexer_analyzer.analyze(input_data)
            
            # Mostrar los tokens generados
            self.output_text.insert(tk.END, "Tokens generados:\n")
            for token in tokens:
                self.output_text.insert(tk.END, f"{token}\n")
            
            # Mostrar los errores (si los hay)
            if errors:
                # Agregar errores al administrador de errores
                for error in errors:
                    self.error_manager.add_error("léxico", error["message"], error["position"])
                
                # Formatear y mostrar los errores
                formatted_errors = self.error_manager.format_errors()
                self.output_text.insert(tk.END, "\nErrores encontrados:\n")
                self.output_text.insert(tk.END, formatted_errors, "error")  # Aplicar el tag "error"
        else:
            self.output_text.insert(tk.END, "Error: No se ha ingresado ningún texto.")

        self.output_text.config(state=tk.DISABLED)  # Deshabilitar la edición del área de salida

    def analyze_input_real_time(self, event):
        """
        Método que se ejecuta cada vez que el usuario suelta una tecla.
        Inicia un hilo para analizar el texto en tiempo real.
        """
        # Obtener el texto actual del área de entrada
        input_data = self.input_text.get("1.0", tk.END).strip()

        # Limpiar los tags anteriores
        self.input_text.tag_remove("lexical_error", "1.0", tk.END)
        self.input_text.tag_remove("syntax_error", "1.0", tk.END)
        # self.input_text.tag_remove("semantic_error", "1.0", tk.END)  # Opcional

        # Iniciar un hilo para realizar el análisis en segundo plano
        threading.Thread(target=self.analyze_input_background, args=(input_data,), daemon=True).start()

    def analyze_input_background(self, input_data):
        """
        Método que se ejecuta en un hilo separado para analizar el texto.
        """
        try:
            # Realizar el análisis léxico
            tokens, lexical_errors = self.lexer_analyzer.analyze(input_data)

            # Resaltar errores léxicos en el hilo principal
            self.root.after(0, self.highlight_errors, lexical_errors)

            # Iniciar un hilo para el análisis sintáctico solo si no hay errores léxicos
            if not lexical_errors:
                threading.Thread(target=self.analyze_syntax_background, args=(input_data,), daemon=True).start()
        except Exception as e:
            print(f"Error durante el análisis léxico: {e}")

    def analyze_syntax_background(self, input_text):
        """
        Método que se ejecuta en un hilo separado para analizar la sintaxis.
        """
        try:
            # Realizar el análisis sintáctico utilizando la cadena de texto
            syntax_errors = self.parser_analyzer.analyze_tokens(input_text)

            # Asegurarse de que syntax_errors sea una lista
            if syntax_errors is None:
                syntax_errors = []

            # Pasar los errores sintácticos al hilo principal para resaltarlos
            self.root.after(0, self.highlight_syntax_errors, syntax_errors)
        except Exception as e:
            print(f"Error durante el análisis sintáctico: {e}")

    def highlight_errors(self, lexical_errors):
        """
        Resalta los errores léxicos en el área de entrada.
        """
        for error in lexical_errors:
            if error["position"]:
                start_index = f"1.0 + {error['position'][1]} chars"
                end_index = f"1.0 + {error['position'][1] + 1} chars"
                self.input_text.tag_add("lexical_error", start_index, end_index)

    def highlight_syntax_errors(self, syntax_errors):
        """
        Resalta los errores sintácticos en el área de entrada.
        """
        for error in syntax_errors:
            if error["start_position"] and error["end_position"]:
                start_index = f"{error['start_position'][0]}.{error['start_position'][1]}"
                end_index = f"{error['end_position'][0]}.{error['end_position'][1]}"
                self.input_text.tag_add("syntax_error", start_index, end_index)


    def analyze_parser(self):
        """
        Método que se ejecuta cuando se presiona el botón "Análisis sintáctico".
        Procesa el texto de entrada con el parser y muestra los resultados en el área de salida.
        """
        input_data = self.input_text.get("1.0", tk.END).strip()  # Obtener el texto de entrada
        self.output_text.config(state=tk.NORMAL)  # Habilitar la edición del área de salida
        self.output_text.delete("1.0", tk.END)  # Limpiar el área de salida

        if input_data:
            # Limpiar errores anteriores
            self.error_manager.clear_errors()

            # Ejecutar el análisis sintáctico
            result, errors = self.parser_analyzer.analyze(input_data)
            
            # Mostrar el resultado del análisis sintáctico
            if result is not None:
                self.output_text.insert(tk.END, "Análisis sintáctico exitoso:\n")
                self.output_text.insert(tk.END, f"{result}\n")
            
            # Mostrar los errores (si los hay)
            if errors:
                # Agregar errores al administrador de errores
                for error in errors:
                    self.error_manager.add_error("sintáctico", error["message"], error["position"])
                
                # Formatear y mostrar los errores
                formatted_errors = self.error_manager.format_errors()
                self.output_text.insert(tk.END, "\nErrores encontrados:\n")
                self.output_text.insert(tk.END, formatted_errors, "error")  # Aplicar el tag "error"
        else:
            self.output_text.insert(tk.END, "Error: No se ha ingresado ningún texto.")

        self.output_text.config(state=tk.DISABLED)  # Deshabilitar la edición del área de salida