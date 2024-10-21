import pygame

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mover Nave con OOP")

# Colores
BLACK = (0, 0, 0)

class Nave:
    def __init__(self, x, y, velocidad):
        self.image = pygame.image.load('nave.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = velocidad

    def mover(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidad  # Mover a la izquierda
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidad  # Mover a la derecha
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidad  # Mover hacia arriba
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidad  # Mover hacia abajo

        # Limitar el movimiento dentro de la pantalla
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def dibujar(self, surface):
        surface.blit(self.image, self.rect.topleft)

# Crear la nave
nave = Nave(WIDTH // 2, HEIGHT // 2, 5)

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # Mover la nave
    nave.mover(keys)

    # Limpiar la pantalla
    screen.fill(BLACK)

    # Dibujar la nave
    nave.dibujar(screen)

    # Actualizar la pantalla
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Salir de Pygame
pygame.quit()
