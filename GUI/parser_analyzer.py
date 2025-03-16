from parser import Parser  # Importar el parser real

class ParserAnalyzer:
    def __init__(self):
        """
        Inicializa el analizador sintáctico.
        """
        self.parser = Parser()  # Usar el parser definido en parser.py

    def analyze(self, input_data):
        """
        Ejecuta el parser sobre el texto de entrada y devuelve el resultado del análisis.

        Parámetros:
        -----------
        input_data : str
            El texto de entrada que se desea analizar.

        Retorna:
        --------
        str
            El resultado del análisis sintáctico.
        """
        try:
            result = self.parser.parse(input_data)
            return f"Análisis sintáctico exitoso:\n{result}"
        except Exception as e:
            return f"Error en el análisis sintáctico: {e}"