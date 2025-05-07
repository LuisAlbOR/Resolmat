import threading
import tkinter as tk
from tkinter import ttk
from .error_manager import ErrorManager
from .lexer_analyzer import LexerAnalyzer
from .parser_analyzer import ParserAnalyzer
from vizualizador_gaussjordan import GaussJordanVisualizer
import numpy as np
import re
import pygame

class Widgets:
    def __init__(self, root):
        self.root = root
        self.lexer_analyzer = LexerAnalyzer()
        self.parser_analyzer = ParserAnalyzer()
        self.error_manager = ErrorManager()
        self.create_widgets()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.input_label = ttk.Label(self.main_frame, text="Entrada:")
        self.input_label.pack(anchor=tk.W)

        self.input_text = tk.Text(self.main_frame, height=10, width=70, bg="#3B4252", fg="#D8DEE9", insertbackground="#D8DEE9")
        self.input_text.pack(fill=tk.BOTH, expand=True)

        self.input_text.tag_config("lexical_error", foreground="red")
        self.input_text.tag_config("syntax_error", foreground="orange")
        self.input_text.tag_config("semantic_error", foreground="lime")

        self.input_text.bind("<KeyRelease>", self.analyze_input_real_time)

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)

        self.lexer_button = ttk.Button(self.button_frame, text="Análisis léxico", command=self.analyze_lexer)
        self.lexer_button.pack(side=tk.LEFT, padx=5)

        self.parser_button = ttk.Button(self.button_frame, text="Análisis sintáctico", command=self.analyze_parser)
        self.parser_button.pack(side=tk.LEFT, padx=5)

        self.compile_button = ttk.Button(self.button_frame, text="Compilar", command=self.compile_code)
        self.compile_button.pack(side=tk.LEFT, padx=5)

        self.execute_button = ttk.Button(self.button_frame, text="Ejecutar", command=self.run_visualizer)
        self.execute_button.pack(side=tk.LEFT, padx=5)

        self.output_label = ttk.Label(self.main_frame, text="Salida:")
        self.output_label.pack(anchor=tk.W)

        self.output_frame = ttk.Frame(self.main_frame)
        self.output_frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = tk.Text(self.output_frame, height=10, width=70, bg="#3B4252", fg="#D8DEE9", state=tk.NORMAL)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.output_text.tag_config("error", foreground="skyblue")

        self.scrollbar = ttk.Scrollbar(self.output_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.configure(yscrollcommand=self.scrollbar.set)

    def analyze_lexer(self):
        input_data = self.input_text.get("1.0", tk.END).strip()
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)

        if input_data:
            self.error_manager.clear_errors()
            tokens, errors = self.lexer_analyzer.analyze(input_data)
            self.output_text.insert(tk.END, "Tokens generados:\n")
            for token in tokens:
                self.output_text.insert(tk.END, f"{token}\n")
            if errors:
                for error in errors:
                    self.error_manager.add_error("léxico", error["message"], error["position"])
                self.output_text.insert(tk.END, "\nErrores encontrados:\n")
                self.output_text.insert(tk.END, self.error_manager.format_errors(), "error")
        else:
            self.output_text.insert(tk.END, "Error: No se ha ingresado ningún texto.")

        self.output_text.config(state=tk.DISABLED)

    def analyze_input_real_time(self, event):
        input_data = self.input_text.get("1.0", tk.END).strip()
        self.input_text.tag_remove("lexical_error", "1.0", tk.END)
        self.input_text.tag_remove("syntax_error", "1.0", tk.END)
        self.input_text.tag_remove("semantic_error", "1.0", tk.END)
        threading.Thread(target=self.analyze_input_background, args=(input_data,), daemon=True).start()

    def analyze_input_background(self, input_data):
        try:
            tokens, lexical_errors = self.lexer_analyzer.analyze(input_data)
            self.root.after(0, self.highlight_errors, lexical_errors)
            if not lexical_errors:
                threading.Thread(target=self.analyze_syntax_background, args=(input_data,), daemon=True).start()
        except Exception as e:
            print(f"Error durante el análisis léxico: {e}")

    def analyze_syntax_background(self, input_text):
        try:
            syntax_errors = self.parser_analyzer.analyze_tokens(input_text)
            if syntax_errors is None:
                syntax_errors = []
            self.root.after(0, self.highlight_syntax_errors, syntax_errors)
        except Exception as e:
            print(f"Error durante el análisis sintáctico: {e}")

    def highlight_errors(self, lexical_errors):
        for error in lexical_errors:
            if error["position"]:
                start_index = f"1.0 + {error['position'][1]} chars"
                end_index = f"1.0 + {error['position'][1] + 1} chars"
                self.input_text.tag_add("lexical_error", start_index, end_index)

    def highlight_syntax_errors(self, syntax_errors):
        for error in syntax_errors:
            if error["start_position"] and error["end_position"]:
                start_index = f"{error['start_position'][0]}.{error['start_position'][1]}"
                end_index = f"{error['end_position'][0]}.{error['end_position'][1]}"
                tipo = error.get("type", "").lower()
                if tipo == "semántico":
                    self.input_text.tag_add("semantic_error", start_index, end_index)
                elif tipo == "sintáctico":
                    self.input_text.tag_add("syntax_error", start_index, end_index)

    def analyze_parser(self):
        input_data = self.input_text.get("1.0", tk.END).strip()
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)

        if input_data:
            self.error_manager.clear_errors()
            result, errors = self.parser_analyzer.analyze(input_data)
            if result is not None:
                self.output_text.insert(tk.END, "Análisis sintáctico exitoso:\n")
            if errors:
                for error in errors:
                    tipo = error.get("type", "").lower()
                    self.error_manager.add_error(tipo, error["message"], error["position"])
                self.output_text.insert(tk.END, "\nErrores encontrados:\n")
                self.output_text.insert(tk.END, self.error_manager.format_errors(), "error")
        else:
            self.output_text.insert(tk.END, "Error: No se ha ingresado ningún texto.")

        self.output_text.config(state=tk.DISABLED)

    def compile_code(self):
        input_data = self.input_text.get("1.0", tk.END).strip()
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)

        if input_data:
            self.error_manager.clear_errors()
            result, errors = self.parser_analyzer.analyze(input_data)
            errors = [e for e in errors if e.get("type", "").lower() != "léxico"]

            if result is not None:
                self.output_text.insert(tk.END, "Compilación exitosa.\n")
            else:
                self.output_text.insert(tk.END, "Se encontraron errores en la compilación.\n")

            for error in errors:
                tipo = error.get("type", "").lower()
                self.error_manager.add_error(tipo, error["message"], error["position"])

            if errors:
                self.output_text.insert(tk.END, "\nErrores encontrados:\n")
                self.output_text.insert(tk.END, self.error_manager.format_errors(), "error")
        else:
            self.output_text.insert(tk.END, "Error: No se ha ingresado ningún texto.")

        self.output_text.config(state=tk.DISABLED)

    def run_visualizer(self):
        input_data = self.input_text.get("1.0", tk.END).strip()
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)

        self.error_manager.clear_errors()
        result, errors = self.parser_analyzer.analyze(input_data)

        if errors:
            for error in errors:
                self.error_manager.add_error(error.get("type", ""), error["message"], error["position"])
            self.output_text.insert(tk.END, "\nErrores encontrados:\n")
            self.output_text.insert(tk.END, self.error_manager.format_errors(), "error")
            return

        # Limpiar espacios antes de extraer la matriz
        input_data = self.limpiar_espacios_matriz(input_data)

        A, b = self.extraer_matriz(input_data)
        if isinstance(A, list):
            self.output_text.insert(tk.END, A[0], "error")
            return

        visualizador = GaussJordanVisualizer(A, b)
        visualizador.iniciar()

    def extraer_matriz(self, entrada):
        entrada = entrada.lower().strip()
        if not re.match(r'^(crea|genera|realiza|has)\s+la\s+siguiente\s+matriz', entrada):
            return ["Error: Instrucción inválida"], None
        entrada = re.sub(r'^(crea|genera|realiza|has)\s+la\s+siguiente\s+matriz', '', entrada).strip()
        ecuaciones = re.findall(r'\(([-\dxzy\s\+\-]+)=([-\d]+)\)', entrada)
        if len(ecuaciones) != 3:
            return ["Error: Se esperaban 3 ecuaciones"], None

        coef, const = [], []
        def convertir_coef(c):
            if c is None: return 0
            valor = c.group(1)
            return 1 if valor in ["", "+"] else -1 if valor == "-" else int(valor)

        for izq, der in ecuaciones:
            x = convertir_coef(re.search(r'([-+]?\d*)x', izq))
            y = convertir_coef(re.search(r'([-+]?\d*)y', izq))
            z = convertir_coef(re.search(r'([-+]?\d*)z', izq))
            coef.append([x, y, z])
            const.append(int(der))

        return np.array(coef, float), np.array(const, float)

    def limpiar_espacios_matriz(self, texto):
        ecuaciones = re.findall(r'\(([^=]+)=([^)]+)\)', texto)
        for izq, der in ecuaciones:
            izq_limpio = re.sub(r'\s+', '', izq)
            der_limpio = re.sub(r'\s+', '', der)
            original = f"({izq}={der})"
            limpio = f"({izq_limpio}={der_limpio})"
            texto = texto.replace(original, limpio)
        return texto
