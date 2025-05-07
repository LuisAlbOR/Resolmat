#parser_analyser.py
class ParserAnalyzer:
    def __init__(self):
        """
        Inicializa el analizador sintáctico.
        """
        from parser import Parser  # Importar el parser real
        self.parser = Parser()
        self.errors = []  # Lista para almacenar errores

    def parse(self, input_text):
        """
        Analiza el texto de entrada y devuelve el resultado del análisis y los errores.
        """
        # Reiniciar la lista de errores
        self.errors = []

        # Ejecutar el análisis sintáctico
        result = self.parser.parse(input_text)

        return result, self.errors
    
    def analyze_tokens(self, input_text):
        """
        Analiza la cadena de entrada y devuelve los errores en el formato requerido.
        """
        # Reiniciar la lista de errores
        self.errors = []

        # Ejecutar el análisis sintáctico utilizando la cadena de texto
        result, errors = self.parser.parse(input_text)
        # Devolver los errores en el formato requerido
        return self._format_errors(errors)
    
    def _format_errors(self, errors):
        """
        Formatea los errores en el formato requerido.
        """
        formatted_errors = []
        for error in errors:
            # Verificar si el error es un diccionario y tiene las claves necesarias
            if isinstance(error, dict) and "message" in error and "position" in error:
                message = error["message"]
                position = error["position"]

                # Si no hay posición, devolver un error sin posición
                if position is None:
                    formatted_errors.append({
                        "message": message,
                        "start_position": None,
                        "end_position": None
                    })
                else:
                    # Convertir la posición al formato (línea, columna)
                    line, column = position
                    formatted_errors.append({
                        "message": message,
                        "start_position": (line, column),
                        "end_position": (line, column + 1)
                    })
            else:
                # Si el error no tiene el formato esperado, manejarlo como un error genérico
                formatted_errors.append({
                    "message": str(error),
                    "start_position": None,
                    "end_position": None
                })
        return formatted_errors
    
    def  analyze(self, input_data):
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