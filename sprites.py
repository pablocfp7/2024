import pygame
import sys


pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Animación de Sprites")


WHITE = (255, 255, 255)

sprite_images = [pygame.image.load(f'sprite_frame_{i}.png') for i in range(1, 6)]
current_frame = 0
frame_count = len(sprite_images)


clock = pygame.time.Clock()
frame_rate = 10  


        for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    screen.fill(WHITE)

    
    current_frame = (current_frame + 1) % frame_count

    
    screen.blit(sprite_images[current_frame], (screen_width // 2, screen_height // 2))

    
    pygame.display.flip()

    
    clock.tick(frame_rate)
