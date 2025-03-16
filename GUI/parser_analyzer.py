class ParserAnalyzer:
    def __init__(self):
        """
        Inicializa el analizador sintáctico.
        """
        from parser import Parser  # Importar el parser real
        self.parser = Parser()

    def analyze(self, input_data):
        """
        Ejecuta el parser sobre el texto de entrada y devuelve el resultado del análisis y los errores.

        Parámetros:
        -----------
        input_data : str
            El texto de entrada que se desea analizar.

        Retorna:
        --------
        tuple
            Una tupla con dos elementos:
            - El resultado del análisis sintáctico (si es exitoso).
            - Una lista de errores (cada error es un diccionario con "message" y "position").
        """
        try:
            result, errors = self.parser.parse(input_data)
            return result, errors  # Devolver el resultado y los errores
        except Exception as e:
            error_msg = f"Error sintáctico: {e}"
            return None, [{"message": error_msg, "position": None}]  # Devolver el error