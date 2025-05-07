class ErrorManager:
    def __init__(self):
        """
        Inicializa el administrador de errores.
        """
        self.errors = []  # Lista para almacenar errores

    def add_error(self, error_type, message, position=None):
        """
        Agrega un error a la lista de errores.

        Parámetros:
        -----------
        error_type : str
            Tipo de error (léxico, sintáctico, semántico, etc.).
        message : str
            Mensaje descriptivo del error.
        position : tuple, opcional
            Tupla con la línea y columna donde ocurrió el error (por defecto es None).
        """
        error = {
            "type": error_type.upper(),  # Convertir a mayúsculas
            "message": message.capitalize(),
            "position": position
        }
        self.errors.append(error)

    def format_errors(self):
        """
        Formatea los errores en un mensaje legible y coloreado para terminal (bash).
        """
        formatted_errors = []
        for error in self.errors:
            error_type = error["type"]
            message = error["message"]
            position = error["position"]

            # Colores ANSI para terminal
            if error_type == "LÉXICO":
                color = "\033[91m"  # Rojo
            elif error_type == "SINTÁCTICO":
                color = "\033[93m"  # Naranja (amarillo claro)
            elif error_type == "SEMÁNTICO":
                color = "\033[92m"  # Verde
            else:
                color = "\033[0m"   # Reset

            # Formato con posición
            if position:
                line, column = position
                formatted_error = f"{color}{error_type} ERROR (Línea {line}, Columna {column}): {message}\033[0m"
            else:
                formatted_error = f"{color}{error_type} ERROR: {message}\033[0m"

            formatted_errors.append(formatted_error)

        return "\n".join(formatted_errors)

    def clear_errors(self):
        """
        Limpia la lista de errores.
        """
        self.errors = []
