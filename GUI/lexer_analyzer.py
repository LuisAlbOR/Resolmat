from lexer import Lexer  # Importar el lexer real

class LexerAnalyzer:
    def __init__(self):
        """
        Inicializa el analizador léxico.
        """
        self.lexer = Lexer()  # Crear una instancia del lexer

    def analyze(self, input_data):
        """
        Ejecuta el lexer sobre el texto de entrada y devuelve los tokens generados.

        Parámetros:
        -----------
        input_data : str
            El texto de entrada que se desea analizar.

        Retorna:
        --------
        list
            Una lista de tokens generados por el lexer.
        """
        # Procesar el texto de entrada
        self.lexer.lexer.input(input_data)

        # Obtener los tokens
        tokens = []
        while True:
            tok = self.lexer.lexer.token()
            if not tok:
                break  # No más tokens
            tokens.append(tok)

        return tokens