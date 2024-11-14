import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir el tamaño de la ventana
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pelota que rebota")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

# Clase para la pelota
class Pelota(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Tamaño de la pelota
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO // 2, ALTO // 2)  # Inicia en el centro de la pantalla

        # Propiedades de la pelota
        self.velocidad_x = 5  # Velocidad horizontal
        self.velocidad_y = -10  # Velocidad vertical (negativa para que suba al inicio)
        self.gravedad = 0.5  # Aceleración de la gravedad
        self.factor_rebote = 0.8  # Factor de rebote (reduce la velocidad tras el rebote)

    def update(self):
        # Aplicar gravedad
        self.velocidad_y += self.gravedad

        # Movimiento
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # Rebote con los bordes de la pantalla (colisiones con las paredes)
        if self.rect.left <= 0 or self.rect.right >= ANCHO:
            self.velocidad_x = -self.velocidad_x  # Invertir dirección horizontal
        if self.rect.top <= 0:  # Toque con el techo
            self.velocidad_y = -self.velocidad_y  # Invertir dirección vertical

        # Rebote en el suelo
        if self.rect.bottom >= ALTO:
            self.rect.bottom = ALTO  # Evitar que la pelota pase del suelo
            self.velocidad_y = -self.velocidad_y * self.factor_rebote  # Rebote con reducción de velocidad

# Crear la pelota
pelota = Pelota()

# Grupo de sprites para manejo eficiente
sprites = pygame.sprite.Group()
sprites.add(pelota)

# Bucle principal del juego
while True:
    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Actualizar la pelota
    sprites.update()

    # Rellenar la pantalla con blanco
    pantalla.fill(BLANCO)

    # Dibujar los objetos (pelota)
    sprites.draw(pantalla)

    # Actualizar la pantalla
    pygame.display.flip()

    # Control de FPS
    pygame.time.Clock().tick(60)
