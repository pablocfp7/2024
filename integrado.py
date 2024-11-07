import pygame
import random


pygame.init()


width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sprites con Animaciones y Colisiones")


WHITE = (255, 255, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.spritesheet = pygame.image.load('kate3.png')  
        self.frame = 0  

        
        self.down_frames = [pygame.Rect(0, 0, 50, 50), pygame.Rect(50, 0, 50, 50), pygame.Rect(100, 0, 50, 50), pygame.Rect(150, 0, 50, 50)]
        self.left_frames = [pygame.Rect(0, 50, 50, 50), pygame.Rect(50, 50, 50, 50), pygame.Rect(100, 50, 50, 50), pygame.Rect(150, 50, 50, 50)]
        self.right_frames = [pygame.Rect(0, 100, 50, 50), pygame.Rect(50, 100, 50, 50), pygame.Rect(100, 100, 50, 50), pygame.Rect(150, 100, 50, 50)]
        self.up_frames = [pygame.Rect(0, 150, 50, 50), pygame.Rect(50, 150, 50, 50), pygame.Rect(100, 150, 50, 50), pygame.Rect(150, 150, 50, 50)]

        self.image = self.spritesheet.subsurface(self.down_frames[self.frame])
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

    def update(self):
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
            self.animate(self.left_frames)
        elif keys[pygame.K_RIGHT]:
            self.rect.x += 5
            self.animate(self.right_frames)
        elif keys[pygame.K_UP]:
            self.rect.y -= 5
            self.animate(self.up_frames)
        elif keys[pygame.K_DOWN]:
            self.rect.y += 5
            self.animate(self.down_frames)
        else:
            
            self.image = self.spritesheet.subsurface(self.down_frames[0])

        
        self.rect.x = max(0, min(self.rect.x, width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, height - self.rect.height))

    def animate(self, direction_frames):
        
        self.frame += 1
        if self.frame >= len(direction_frames):
            self.frame = 0
        self.image = self.spritesheet.subsurface(direction_frames[self.frame])


class Collectible(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = pygame.image.load('collectible.png')  
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


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    all_sprites.update()

    
    collected = pygame.sprite.spritecollide(player, collectibles, True)
    score += len(collected)

    
    screen.fill(WHITE)

    
    all_sprites.draw(screen)

    
    font = pygame.font.Font(None, 36)
    text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(text, (10, 10))

    
    pygame.display.flip()

    
    pygame.time.delay(10)


pygame.quit()
