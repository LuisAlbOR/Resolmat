import ply.yacc as yacc
from lexer import Lexer  # Importar la clase Lexer

class Parser:
    def __init__(self):
        # Crear una instancia de Lexer para acceder a los tokens
        self.lexer_instance = Lexer()
        self.tokens = self.lexer_instance.tokens  # Obtener los tokens desde la instancia de Lexer

        # Construir el parser
        self.parser = yacc.yacc(module=self)

    # Reglas del parser
    def p_expresion_matriz(self, p):
        '''
        expresion : PALABRA_CLAVE LA SIGUIENTE MATRIZ ecuacion ecuacion ecuacion
        '''
        print("Expresión de matriz válida detectada")
        print("Palabra clave:", p[1])
        print("Matriz:", p[4], p[5], p[6])  # Aquí p[4], p[5], p[6] son las ecuaciones

    def p_ecuacion(self, p):
        '''
        ecuacion : PARENTESIS_IZQ termino termino termino IGUAL NUMERO PARENTESIS_DER
        '''
        print("Ecuación válida detectada")
        print("Términos:", p[2], p[3], p[4])  # p[2], p[3], p[4] son los términos
        print("Resultado:", p[6])  # p[6] es el número después del signo igual

    def p_termino(self, p):
        '''
        termino : SIGNO NUMERO VARIABLE
        '''
        print("Término válido detectado")
        print("Signo:", p[1])  # p[1] es el signo
        print("Número:", p[2])  # p[2] es el número
        print("Variable:", p[3])  # p[3] es la variable

    # Manejo de errores sintácticos
    def p_error(self, p):
        print("Error de sintaxis en la entrada")

    # Método para analizar la entrada
    def parse(self, input_text):
        self.parser.parse(input_text)