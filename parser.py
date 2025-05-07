import ply.yacc as yacc
from lexer import Lexer
from semantic_analyzer import SemanticAnalyzer

class Parser:
    def __init__(self):
        self.lexer_instance = Lexer()
        self.tokens = self.lexer_instance.tokens
        self.errors = []
        self.semantic_analyzer = SemanticAnalyzer()
        self.parser = yacc.yacc(module=self)

    def p_expresion_matriz(self, p):
        '''
        expresion : PALABRA_CLAVE LA SIGUIENTE MATRIZ ecuacion ecuacion ecuacion
        '''
        print("Expresión de matriz válida detectada")
        print("Palabra clave:", p[1])
        print("Matriz:", p[4], p[5], p[6])

    def p_ecuacion(self, p):
        '''
        ecuacion : PARENTESIS_IZQ terminos IGUAL NUMERO PARENTESIS_DER
        '''
        print("Ecuación válida detectada")
        for term in p[2]:
            print(term)
        print("Resultado:", p[4])

        self.semantic_analyzer.analyze_variable_order(
            p[2],
            getattr(p.slice[1], 'lineno', None),
            getattr(p.slice[1], 'lexpos', None)
        )

    def p_terminos(self, p):
        '''
        terminos : termino terminos
                 | termino
        '''
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

    def p_termino(self, p):
        '''
        termino : SIGNO NUMERO VARIABLE
        '''
        print("Término válido detectado")
        print("Signo:", p[1], "Número:", p[2], "Variable:", p[3])

        self.semantic_analyzer.analyze_term(
            p[1], p[2], p[3],
            getattr(p.slice[1], 'lineno', None),
            getattr(p.slice[1], 'lexpos', None)
        )
        p[0] = (p[1], p[2], p[3])

    def p_error(self, p):
        if p:
            error_msg = f"Error de sintaxis en el token '{p.value}' (tipo: {p.type})"
            position = (p.lineno, p.lexpos)
        else:
            error_msg = "Error de sintaxis al final de la entrada"
            position = None
        self.errors.append({"message": error_msg, "position": position})

    def parse(self, input_text):
        self.errors = []
        self.semantic_analyzer.clear()

        result = self.parser.parse(input_text)

        # Si hay errores sintácticos, NO ejecutar análisis semántico
        if self.errors:
            return result, self.errors

        # Si no hubo errores sintácticos, retornar todos (incluye semántico)
        return result, self.errors + self.semantic_analyzer.get_errors()
