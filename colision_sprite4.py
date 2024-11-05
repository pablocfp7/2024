import pygame
import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sprites con Colisiones")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 50  # Tamaño inicial
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(WHITE)  # Color blanco
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

        # Limitar el movimiento del jugador a la pantalla
        self.rect.x = max(0, min(self.rect.x, width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, height - self.rect.height))

    def increase_size(self):
        self.size += 5  # Aumentar tamaño
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(WHITE)  # Mantener el color blanco
        self.rect = self.image.get_rect(center=self.rect.center)  # Mantener el centro

    def split(self):
        # Crear tres nuevos cuadrados más pequeños
        small_size = self.size // 3
        for i in range(3):
            small_square = SmallSquare(self.rect.centerx + (i - 1) * (small_size + 5), self.rect.centery)
            all_sprites.add(small_square)
            small_squares.add(small_square)
        self.kill()  # Eliminar el jugador original

class SmallSquare(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.size = 30  # Tamaño de los cuadrados pequeños
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))

class Collectible(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(0, height - self.rect.height)
        self.speed_x = random.choice([-2, 2])
        self.speed_y = random.choice([-2, 2])

    def update(self):
        # Mover los collectibles
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Rebotar al llegar a los bordes de la pantalla
        if self.rect.x <= 0 or self.rect.x >= width - self.rect.width:
            self.speed_x *= -1
        if self.rect.y <= 0 or self.rect.y >= height - self.rect.height:
            self.speed_y *= -1

def create_collectibles():
    collectibles.empty()  # Vaciar el grupo de collectibles
    for _ in range(10):
        collectible = Collectible()
        all_sprites.add(collectible)
        collectibles.add(collectible)

# Inicialización de grupos y el jugador
all_sprites = pygame.sprite.Group()
collectibles = pygame.sprite.Group()
small_squares = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

create_collectibles()  # Crear los collectibles inicialmente

running = True
score = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                player.split()  # Dividir el cuadrado cuando se presiona 'K'

    all_sprites.update()

    # Colisión entre el jugador y los collectibles
    collected = pygame.sprite.spritecollide(player, collectibles, True)
    score += len(collected)

    # Aumentar el tamaño del jugador por cada collectible
    for _ in collected:
        player.increase_size()

    # Limpiar la pantalla y dibujar el fondo negro
    screen.fill(BLACK)  # Fondo negro
    all_sprites.draw(screen)

    font = pygame.font.Font(None, 36)
    text = font.render(f'Score: {score}', True, (255, 255, 255))  # Texto blanco
    screen.blit(text, (10, 10))

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
