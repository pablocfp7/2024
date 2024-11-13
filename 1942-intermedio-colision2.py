import pygame
import random

pygame.init()

ANCHO = 800
ALTO = 600
FPS = 60

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)

screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("1942 - Juego Básico")

clock = pygame.time.Clock()

# Cargar imágenes de los aviones
avion_img = pygame.image.load("avion.png")  # Imagen del avión del jugador
avion_rect = avion_img.get_rect()

# Imagen del avión enemigo
enemigo_img = pygame.image.load("enemigo.png")  # Imagen del avión enemigo
enemigo_rect = enemigo_img.get_rect()

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))  # Bala representada por un rectángulo
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()   # Eliminar la bala si se sale de la pantalla


class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemigo_img  # Usar la imagen del enemigo en lugar de un rectángulo
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - self.rect.width)  # Posición aleatoria
        self.rect.y = random.randint(-100, -40)  # Aparecen fuera de la pantalla
        self.speed = random.randint(2, 6)  # Velocidad aleatoria

    def update(self):
        self.rect.y += self.speed  # El enemigo se mueve hacia abajo
        if self.rect.top > ALTO:
            self.rect.x = random.randint(0, ANCHO - self.rect.width)  # Reaparecer en la parte superior
            self.rect.y = random.randint(-100, -40)


all_sprites = pygame.sprite.Group()
bala_group = pygame.sprite.Group()
enemigos_group = pygame.sprite.Group()

# Crear el avión del jugador
avion = pygame.sprite.Sprite()
avion.image = avion_img
avion.rect = avion.image.get_rect()
avion.rect.center = (ANCHO // 2, ALTO - 50)
all_sprites.add(avion)

game_over = False
font = pygame.font.Font(None, 36)  # Fuente para mostrar texto
game_over_time = 0  # Para llevar el control del tiempo en el que ocurre el Game Over

while not game_over:
    clock.tick(FPS)

    # Comprobar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bala = Bala(avion.rect.centerx, avion.rect.top)
                all_sprites.add(bala)
                bala_group.add(bala)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and avion.rect.left > 0:
        avion.rect.x -= 5
    if keys[pygame.K_RIGHT] and avion.rect.right < ANCHO:
        avion.rect.x += 5
    if keys[pygame.K_UP] and avion.rect.top > 0:
        avion.rect.y -= 5
    if keys[pygame.K_DOWN] and avion.rect.bottom < ALTO:
        avion.rect.y += 5

    # Generar enemigos aleatorios
    if random.random() < 0.01:
        enemigo = Enemigo()
        all_sprites.add(enemigo)
        enemigos_group.add(enemigo)

    all_sprites.update()

    # Detectar colisión entre el avión del jugador y los enemigos
    if pygame.sprite.spritecollide(avion, enemigos_group, False):
        game_over = True  # Establecer que el juego ha terminado
        game_over_time = pygame.time.get_ticks()  # Guardar el tiempo en el que ocurrió el Game Over

    # Detectar colisiones entre balas y enemigos
    for bala in bala_group:
        enemigos_colision = pygame.sprite.spritecollide(bala, enemigos_group, True)
        for enemigo in enemigos_colision:
            bala.kill()  # Eliminar la bala

    # Dibujar todo en la pantalla
    screen.fill(BLANCO)
    all_sprites.draw(screen)

    # Si el juego terminó, mostrar "Game Over" y esperar 3 segundos
    if game_over:
        game_over_text = font.render("GAME OVER", True, NEGRO)
        screen.blit(game_over_text, (ANCHO // 2 - game_over_text.get_width() // 2, ALTO // 2 - game_over_text.get_height() // 2))

        # Esperar 3 segundos antes de cerrar el juego
        if pygame.time.get_ticks() - game_over_time > 6000:  # 3000 ms = 3 segundos
            game_over = True  # Esto hará que el bucle termine

    pygame.display.flip()

pygame.quit()

