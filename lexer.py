import ply.lex as lex

class Lexer:
    # Definir los tokens
    tokens = (
        'PALABRA_CLAVE',
        'LA',
        'SIGUIENTE',
        'MATRIZ',
        'PARENTESIS_IZQ',
        'SIGNO',
        'NUMERO',
        'VARIABLE',
        'IGUAL',
        'PARENTESIS_DER',
    )

    # Expresiones regulares para los tokens simples
    t_LA = r'la'
    t_SIGUIENTE = r'siguiente'
    t_MATRIZ = r'matriz'
    t_PARENTESIS_IZQ = r'\('
    t_PARENTESIS_DER = r'\)'
    t_SIGNO = r'[\+\-]'
    t_IGUAL = r'='

    def t_PALABRA_CLAVE(self, t):
        r'crea|genera|realiza|has'
        return t
    
    # Expresión regular para números
    def t_NUMERO(self, t):
        r'\d+'
        t.value = int(t.value)  # Convertir a entero
        return t

    # Expresión regular para variables (x, y, z)
    def t_VARIABLE(self, t):
        r'[xyz]'
        return t

    # Ignorar espacios y tabulaciones
    t_ignore = ' \t'

    # Manejo de errores léxicos
    def t_error(self, t):
        print(f"Carácter ilegal '{t.value[0]}'")
        t.lexer.skip(1)

    # Constructor de la clase
    def __init__(self):
        self.lexer = lex.lex(module=self)  # Construir el lexer

    # Método para probar el lexer
    def test(self, input_text : str):
        """
        Procesa un texto de entrada y devuelve una lista de tokens generados por el lexer.

        Parámetros:
        -----------
        input_text : str
            El texto de entrada que se desea analizar léxicamente.

        Retorna:
        --------
        list
            Una lista de objetos `LexToken` que representan los tokens generados.
        """
        self.lexer.input(input_text)
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break  # No más tokens
            tokens.append(tok)
        return tokens