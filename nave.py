import pygame
import math

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nave Espacial")

# Colores
BLACK = (0, 0, 0)

# Cargar la imagen de la nave
# Asegúrate de tener una imagen llamada 'nave.png' en la misma carpeta
nave_img = pygame.image.load('nave.png').convert_alpha()
nave_rect = nave_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Variables de control
angle = 0
speed = 5

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # Rotación
    if keys[pygame.K_LEFT]:
        angle += 5
    if keys[pygame.K_RIGHT]:
        angle -= 5
    
    # Movimiento hacia adelante y atrás
    if keys[pygame.K_UP]:
        nave_rect.x += speed * math.cos(math.radians(angle))
        nave_rect.y -= speed * math.sin(math.radians(angle))
    if keys[pygame.K_DOWN]:
        nave_rect.x -= speed * math.cos(math.radians(angle))
        nave_rect.y += speed * math.sin(math.radians(angle))

    # Limpiar la pantalla
    screen.fill(BLACK)

    # Rotar la imagen de la nave
    rotated_nave = pygame.transform.rotate(nave_img, angle)
    rotated_rect = rotated_nave.get_rect(center=nave_rect.center)

    # Dibujar la nave
    screen.blit(rotated_nave, rotated_rect.topleft)

    # Actualizar la pantalla
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Salir de Pygame
pygame.quit()
