import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Nave")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Nave:
    def __init__(self, x, y, velocidad):
        self.image = pygame.image.load('nave.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = velocidad

    def mover(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidad

        # Limitar el movimiento dentro de la pantalla
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def dibujar(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Proyectil:
    def __init__(self, x, y, velocidad):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.velocidad = velocidad

    def mover(self):
        self.rect.y -= self.velocidad

    def dibujar(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)

class Enemigo:
    def __init__(self, x, y, velocidad):
        self.image = pygame.Surface((50, 50))  # Rectángulo como enemigo
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidad = velocidad

    def mover(self):
        self.rect.y += self.velocidad  # Mover hacia abajo

    def dibujar(self, surface):
        surface.blit(self.image, self.rect.topleft)

# Crear la nave
nave = Nave(WIDTH // 2, HEIGHT // 2, 5)
proyectiles = []
enemigos = []
proyectil_velocidad = 10
enemigo_velocidad = 3

# Temporizador para crear enemigos
crear_enemigos_intervalo = 1000  # Cada 1 segundo
pygame.time.set_timer(pygame.USEREVENT, crear_enemigos_intervalo)  # Generar evento

# Bucle principal
running = True
while running:
    screen.fill(BLACK)  # Limpiar la pantalla

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                nuevo_proyectil = Proyectil(nave.rect.centerx, nave.rect.top, proyectil_velocidad)
                proyectiles.append(nuevo_proyectil)
        if event.type == pygame.USEREVENT:  # Evento para crear enemigos
            # Generar varios enemigos en cada evento
            for _ in range(random.randint(1, 3)):  # Generar entre 1 y 3 enemigos
                x = random.randint(0, WIDTH - 50)
                enemigo = Enemigo(x, random.randint(-50, -10), enemigo_velocidad)
                enemigos.append(enemigo)

    keys = pygame.key.get_pressed()
    
    # Mover la nave
    nave.mover(keys)

    # Mover los proyectiles
    for proyectil in proyectiles[:]:
        proyectil.mover()
        if proyectil.rect.bottom < 0:
            proyectiles.remove(proyectil)

    # Mover enemigos
    for enemigo in enemigos[:]:
        enemigo.mover()
        if enemigo.rect.top > HEIGHT:
            enemigos.remove(enemigo)

    # Detección de colisiones entre proyectiles y enemigos
    for proyectil in proyectiles[:]:
        for enemigo in enemigos[:]:
            if proyectil.rect.colliderect(enemigo.rect):
                proyectiles.remove(proyectil)  # Eliminar proyectil
                enemigos.remove(enemigo)  # Eliminar enemigo
                break

    # Detección de colisiones entre la nave y enemigos
    for enemigo in enemigos:
        if enemigo.rect.colliderect(nave.rect):
            print("¡Juego Terminado!")  # Mensaje de finalización
            running = False  # Terminar el juego

    # Dibujar la nave
    nave.dibujar(screen)

    # Dibujar los proyectiles
    for proyectil in proyectiles:
        proyectil.dibujar(screen)

    # Dibujar los enemigos
    for enemigo in enemigos:
        enemigo.dibujar(screen)

    # Actualizar la pantalla
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Salir de Pygame
pygame.quit()
