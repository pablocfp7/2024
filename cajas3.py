import pygame
import sys

pygame.init()

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

ANCHO = 800
ALTO = 600

screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Mover Cajas")


class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.velocidad = 5

    def update(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if teclas[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN]:
            self.rect.y += self.velocidad


class Caja(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def mover_caja_alejada(caja, teclas, obstaculos):
    # Detectamos si la caja colide con los obstáculos y en qué dirección.
    if teclas[pygame.K_LEFT]:
        if pygame.sprite.spritecollide(caja, obstaculos, False):
            caja.rect.x += 5  # Mover hacia la derecha
        else:
            caja.rect.x -= 5
    if teclas[pygame.K_RIGHT]:
        if pygame.sprite.spritecollide(caja, obstaculos, False):
            caja.rect.x -= 5  # Mover hacia la izquierda
        else:
            caja.rect.x += 5
    if teclas[pygame.K_UP]:
        if pygame.sprite.spritecollide(caja, obstaculos, False):
            caja.rect.y += 5  # Mover hacia abajo
        else:
            caja.rect.y -= 5
    if teclas[pygame.K_DOWN]:
        if pygame.sprite.spritecollide(caja, obstaculos, False):
            caja.rect.y -= 5  # Mover hacia arriba
        else:
            caja.rect.y += 5


jugador = Jugador()
cajas = pygame.sprite.Group()

# Colocar algunas cajas en el mapa
caja1 = Caja(200, 200)
caja2 = Caja(300, 300)
cajas.add(caja1, caja2)

# Crear algunos obstáculos en el mapa
obstaculo1 = Obstaculo(400, 200)
obstaculo2 = Obstaculo(500, 300)
obstaculos = pygame.sprite.Group()
obstaculos.add(obstaculo1, obstaculo2)

todos_los_sprites = pygame.sprite.Group()
todos_los_sprites.add(jugador, *cajas, *obstaculos)

running = True
while running:
    screen.fill(BLANCO)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    teclas = pygame.key.get_pressed()
    jugador.update(teclas)

    # Mover las cajas con el jugador y evitando la colisión con obstáculos
    for caja in cajas:
        if jugador.rect.colliderect(caja.rect):
            mover_caja_alejada(caja, teclas, obstaculos)

    todos_los_sprites.draw(screen)

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
