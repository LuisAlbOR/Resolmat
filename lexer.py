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
        error_msg = f"Carácter ilegal '{t.value[0]}'"
        position = (t.lineno, t.lexpos)  # Línea y posición del error
        self.errors.append({"message": error_msg, "position": position})  # Registrar el error con posición
        t.lexer.skip(1)  # Saltar el carácter ilegal y continuar

    # Constructor de la clase
    def __init__(self):
        self.lexer = lex.lex(module=self)  # Construir el lexer
        self.errors = []  # Lista para almacenar errores