# vizualizador_gaussjordan.py
import pygame
import numpy as np
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

class GaussJordanVisualizer:
    def __init__(self, A, b):
        self.A = A
        self.b = b
        self.n = len(b)
        self.M = np.hstack((A, b.reshape(-1, 1)))  # Matriz aumentada [A|b]

        # Configuración de la ventana
        self.WIDTH, self.HEIGHT = 1000, 700
        self.ROSA_PASTEL = (255, 182, 193)
        self.AMARILLO_PASTEL = (255, 255, 200)
        self.VERDE_PASTEL = (200, 255, 200)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 139)  # Azul oscuro para explicaciones

        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 40)
        self.screen = None
        self.clock = pygame.time.Clock()
        
        # Variables de estado
        self.paso_actual = 1
        self.fila_actual = 0
        self.estado = "inicio"
        self.fila_eliminar = 0
        self.finalizado = False
        self.mostrar_resultado = False
        
        # Explicaciones contextuales
        self.explicacion = "Presiona ESPACIO para comenzar el método Gauss-Jordan"
        self.operacion_actual = ""

    def iniciar(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Método Gauss-Jordan")
        running = True

        while running:
            self.screen.fill(self.ROSA_PASTEL)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.finalizado:
                        self.realizar_paso()
                    elif event.key == pygame.K_RETURN and self.finalizado:
                        self.mostrar_resultado = True

            self.dibujar_matriz()
            self.mostrar_explicaciones()
            pygame.display.flip()
            self.clock.tick(30)

    def realizar_paso(self):
        if self.fila_actual >= self.n:
            self.explicacion = "¡Proceso completado! La matriz está en su forma escalonada reducida."
            self.operacion_actual = "Presiona ENTER para ver la solución del sistema"
            self.finalizado = True
            return

        if self.estado == "inicio":
            self.estado = "normalizar"
            self.explicacion = "PASO 1: Normalización - Hacer que el elemento diagonal (pivote) sea 1"
            
        elif self.estado == "normalizar":
            pivot = self.M[self.fila_actual, self.fila_actual]
            if pivot != 0:
                self.M[self.fila_actual] /= pivot
                self.operacion_actual = f"F{self.fila_actual+1} = F{self.fila_actual+1} / {pivot:.2f}"
                self.explicacion = f"Dividimos toda la fila {self.fila_actual+1} por {pivot:.2f} para hacer el pivote igual a 1"
            else:
                self.operacion_actual = f"Error: Pivote en F{self.fila_actual+1} es cero"
                self.explicacion = "No se puede continuar, el pivote es cero"
            
            self.estado = "eliminar"
            self.fila_eliminar = 0
            self.paso_actual += 1

        elif self.estado == "eliminar":
            if self.fila_eliminar < self.n:
                if self.fila_eliminar != self.fila_actual:
                    factor = self.M[self.fila_eliminar, self.fila_actual]
                    if factor != 0:
                        self.M[self.fila_eliminar] -= factor * self.M[self.fila_actual]
                        self.operacion_actual = f"F{self.fila_eliminar+1} = F{self.fila_eliminar+1} - ({factor:.2f}×F{self.fila_actual+1})"
                        self.explicacion = f"Eliminamos el elemento en F{self.fila_eliminar+1} usando la fila pivote {self.fila_actual+1}"
                        self.paso_actual += 1
                self.fila_eliminar += 1
            else:
                self.fila_actual += 1
                self.estado = "normalizar"
                if self.fila_actual < self.n:
                    self.explicacion = f"Avanzamos al siguiente pivote en la fila {self.fila_actual+1}"

    def dibujar_matriz(self):
        start_x = 100
        start_y = 280  # Más espacio para explicaciones
        cell_width = 100
        cell_height = 50

        # Limpiar área superior completamente
        pygame.draw.rect(self.screen, self.ROSA_PASTEL, (0, 0, self.WIDTH, start_y))

        # Dibujar matriz
        for i, fila in enumerate(self.M):
            for j, valor in enumerate(fila):
                x = start_x + j * cell_width
                y = start_y + i * cell_height

                color = self.ROSA_PASTEL
                if i == self.fila_actual and self.estado == "normalizar":
                    color = self.AMARILLO_PASTEL
                elif j == self.fila_actual and self.estado == "eliminar":
                    color = self.VERDE_PASTEL

                pygame.draw.rect(self.screen, color, (x, y, cell_width, cell_height))
                pygame.draw.rect(self.screen, self.GRAY, (x, y, cell_width, cell_height), 2)
                
                # Mostrar valores con diferente color para la columna de resultados
                color_texto = self.BLUE if j == self.n else self.BLACK
                texto = self.font.render(f"{valor:.2f}", True, color_texto)
                texto_rect = texto.get_rect(center=(x + cell_width/2, y + cell_height/2))
                self.screen.blit(texto, texto_rect)

        # Línea vertical para separar coeficientes de resultados
        sep_x = start_x + self.n * cell_width
        pygame.draw.line(self.screen, self.RED, (sep_x, start_y), 
                         (sep_x, start_y + self.n * cell_height), 3)

    def mostrar_explicaciones(self):
        # Título del método
        titulo = self.title_font.render("Método de Eliminación Gauss-Jordan", True, self.BLUE)
        self.screen.blit(titulo, (100, 30))

        # Explicación del paso actual
        explic_lines = [self.explicacion]
        if self.operacion_actual:
            explic_lines.append(f"Operación: {self.operacion_actual}")
        
        y_pos = 80
        for line in explic_lines:
            text = self.font.render(line, True, self.BLACK)
            self.screen.blit(text, (100, y_pos))
            y_pos += 40

        # Mostrar número de paso
        paso_text = self.font.render(f"Paso: {self.paso_actual}", True, self.RED)
        self.screen.blit(paso_text, (self.WIDTH - 150, 30))

        # Mostrar resultado final si está listo
        if self.mostrar_resultado:
            soluciones = self.M[:, -1]
            res_text = f"Solución: x = {soluciones[0]:.2f}, y = {soluciones[1]:.2f}, z = {soluciones[2]:.2f}"
            resultado = self.title_font.render(res_text, True, self.RED)
            self.screen.blit(resultado, (100, 200))

        # Instrucción mínima
        instruccion = "ESPACIO: Siguiente paso" if not self.finalizado else "ENTER: Ver solución"
        instruc_text = self.font.render(instruccion, True, self.BLUE)
        self.screen.blit(instruc_text, (self.WIDTH - 250, self.HEIGHT - 40))