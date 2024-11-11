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


avion_img = pygame.image.load("avion.png")  
avion_rect = avion_img.get_rect()


class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()  


class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - 50)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(2, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > ALTO:
            self.rect.x = random.randint(0, ANCHO - 50)
            self.rect.y = random.randint(-100, -40)


all_sprites = pygame.sprite.Group()
bala_group = pygame.sprite.Group()
enemigos_group = pygame.sprite.Group()


avion = pygame.sprite.Sprite()
avion.image = avion_img
avion.rect = avion.image.get_rect()
avion.rect.center = (ANCHO // 2, ALTO - 50)
all_sprites.add(avion)


game_over = False


while not game_over:
    # Controlar el FPS
    clock.tick(FPS)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                
                bala = Bala(avion.rect.centerx, avion.rect.top)
                all_sprites.add(bala)
                bala_group.add(bala)

    # Mover el avión
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and avion.rect.left > 0:
        avion.rect.x -= 5
    if keys[pygame.K_RIGHT] and avion.rect.right < ANCHO:
        avion.rect.x += 5
    if keys[pygame.K_UP] and avion.rect.top > 0:
        avion.rect.y -= 5
    if keys[pygame.K_DOWN] and avion.rect.bottom < ALTO:
        avion.rect.y += 5

    
    if random.random() < 0.01:  
        enemigo = Enemigo()
        all_sprites.add(enemigo)
        enemigos_group.add(enemigo)

    
    all_sprites.update()

    
    for bala in bala_group:
        enemigos_colision = pygame.sprite.spritecollide(bala, enemigos_group, True)
        for enemigo in enemigos_colision:
            bala.kill()  
            

    
    screen.fill(BLANCO)


    all_sprites.draw(screen)

    
    pygame.display.flip()

pygame.quit()
