import pygame
import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sprites con Colisiones")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
NEW_BACKGROUND_COLOR = (255, 223, 0)  

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
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

        
        self.rect.x = max(0, min(self.rect.x, width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, height - self.rect.height))

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
        
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        
        if self.rect.x <= 0 or self.rect.x >= width - self.rect.width:
            self.speed_x *= -1
        if self.rect.y <= 0 or self.rect.y >= height - self.rect.height:
            self.speed_y *= -1


all_sprites = pygame.sprite.Group()
collectibles = pygame.sprite.Group()


player = Player()
all_sprites.add(player)


for _ in range(10):
    collectible = Collectible()
    all_sprites.add(collectible)
    collectibles.add(collectible)

running = True
score = 0
clock = pygame.time.Clock()


last_add_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    all_sprites.update()

    
    collected = pygame.sprite.spritecollide(player, collectibles, True)
    score += len(collected)

    
    if score >= 10:
        screen.fill(NEW_BACKGROUND_COLOR)
    else:
        screen.fill(WHITE)

    # Añadir un nuevo collectible a mayor velocidad cuando el puntaje aumenta
    current_time = pygame.time.get_ticks()
    if current_time - last_add_time > (1000 - min(score * 10, 900)):  # Reducir el intervalo a medida que el score sube
        collectible = Collectible()
        all_sprites.add(collectible)
        collectibles.add(collectible)
        last_add_time = current_time

    
    all_sprites.draw(screen)

    
    font = pygame.font.Font(None, 36)
    text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(text, (10, 10))

    
    pygame.display.flip()


    clock.tick(60)


pygame.quit()
