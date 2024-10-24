import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Naves")

# Cargar imagen de fondo
fondo = pygame.image.load('fondo.png').convert()
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))  # Escalar al tamaño de la ventana

# Variables para el movimiento del fondo
fondo_y1 = 0
fondo_y2 = -HEIGHT  # Segunda copia del fondo, justo debajo
fondo_speed = 3  # Velocidad del movimiento del fondo

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
        pygame.draw.rect(surface, (255, 255, 255), self.rect)

class Enemigo:
    def __init__(self, x, y, velocidad):
        self.image = pygame.Surface((50, 50))  # Rectángulo como enemigo
        self.image.fill((255, 0, 0))
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

# Inicializar puntaje
puntaje = 0
fuente = pygame.font.Font(None, 36)  # Fuente para el puntaje

def generar_enemigo():
    while True:
        x = random.randint(0, WIDTH - 50)
        y = random.randint(-50, -10)
        nuevo_enemigo = Enemigo(x, y, enemigo_velocidad)
        
        # Verificar si el nuevo enemigo colisiona con algún enemigo existente
        colision = False
        for enemigo in enemigos:
            if nuevo_enemigo.rect.colliderect(enemigo.rect):
                colision = True
                break
        
        if not colision:
            return nuevo_enemigo  # Retornar el enemigo si no hay colisión

# Bucle principal
running = True
while running:
    # Limpiar la pantalla
    screen.fill((0, 0, 0))  # Opcional: llenar de negro, pero el fondo cubrirá esto

    # Mover el fondo hacia arriba
    fondo_y1 += fondo_speed
    fondo_y2 += fondo_speed

    # Reposicionar el fondo si sale de la pantalla
    if fondo_y1 >= HEIGHT:
        fondo_y1 = fondo_y2 - HEIGHT  # Colocar justo encima
    if fondo_y2 >= HEIGHT:
        fondo_y2 = fondo_y1 - HEIGHT  # Colocar justo encima

    # Dibujar el fondo
    screen.blit(fondo, (0, fondo_y1))
    screen.blit(fondo, (0, fondo_y2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                nuevo_proyectil = Proyectil(nave.rect.centerx, nave.rect.top, proyectil_velocidad)
                proyectiles.append(nuevo_proyectil)
        if event.type == pygame.USEREVENT:  # Evento para crear enemigos
            for _ in range(random.randint(1, 3)):  # Generar entre 1 y 3 enemigos
                enemigo = generar_enemigo()
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
                puntaje += 1  # Aumentar el puntaje
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

    # Mostrar puntaje
    texto_puntaje = fuente.render(f'Puntaje: {puntaje}', True, (255, 255, 255))
    screen.blit(texto_puntaje, (10, 10))

    # Actualizar la pantalla
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Salir de Pygame
pygame.quit()
