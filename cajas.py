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


jugador = Jugador()
cajas = pygame.sprite.Group()

# Colocar algunas cajas en el mapa
caja1 = Caja(200, 200)
caja2 = Caja(300, 300)
cajas.add(caja1, caja2)

todos_los_sprites = pygame.sprite.Group()
todos_los_sprites.add(jugador, *cajas)


running = True
while running:
    screen.fill(BLANCO)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    teclas = pygame.key.get_pressed()
    jugador.update(teclas)


    for caja in cajas:
        if jugador.rect.colliderect(caja.rect):
            # Mover la caja con el jugador
            if teclas[pygame.K_LEFT]:
                caja.rect.x -= jugador.velocidad
            if teclas[pygame.K_RIGHT]:
                caja.rect.x += jugador.velocidad
            if teclas[pygame.K_UP]:
                caja.rect.y -= jugador.velocidad
            if teclas[pygame.K_DOWN]:
                caja.rect.y += jugador.velocidad

    
    todos_los_sprites.draw(screen)

    
    pygame.display.flip()

    
    pygame.time.Clock().tick(60)


pygame.quit()
sys.exit()
