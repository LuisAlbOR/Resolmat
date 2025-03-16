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
            "type": error_type.upper(),  # Convertir el tipo de error a mayúsculas
            "message": message.upper(),  # Convertir el mensaje de error a mayúsculas
            "position": position
        }
        self.errors.append(error)

    def format_errors(self):
        """
        Formatea los errores en un mensaje legible.

        Retorna:
        --------
        str
            Cadena formateada con todos los errores.
        """
        formatted_errors = []
        for error in self.errors:
            error_type = error["type"]
            message = error["message"]
            position = error["position"]

            if position:
                line, column = position
                formatted_error = f"{error_type} ERROR (LÍNEA {line}, COLUMNA {column}): {message}"
            else:
                formatted_error = f"{error_type} ERROR: {message}"

            formatted_errors.append(formatted_error)

        return "\n".join(formatted_errors)

    def clear_errors(self):
        """
        Limpia la lista de errores.
        """
        self.errors = []