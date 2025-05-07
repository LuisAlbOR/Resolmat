class SemanticAnalyzer:
    def __init__(self):
        self.errors = []

    def analyze_term(self, signo, numero, variable, lineno=None, lexpos=None):
        if signo not in ['+', '-']:
            self.add_error(f"Signo no válido '{signo}'", lineno, lexpos)
        if not isinstance(numero, int) or numero < 0:
            self.add_error(f"Número no válido '{numero}'", lineno, lexpos)
        if variable not in ['x', 'y', 'z']:
            self.add_error(f"Variable no válida '{variable}'", lineno, lexpos)

    def analyze_variable_order(self, term_list, lineno=None, lexpos=None):
        expected_order = ['x', 'y', 'z']
        received_order = [var for (_, _, var) in term_list]
        filtered_expected = [v for v in expected_order if v in received_order]

        if received_order != filtered_expected:
            self.add_error("Las variables no están en orden x → y → z", lineno, lexpos)

    def add_error(self, message, lineno=None, lexpos=None):
        self.errors.append({
            "type": "semántico",
            "message": message,
            "position": (lineno, lexpos) if lineno is not None and lexpos is not None else None
        })

    def clear(self):
        self.errors = []

    def get_errors(self):
        return self.errors
