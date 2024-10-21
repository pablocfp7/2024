import pygame

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mover Nave")

# Colores
BLACK = (0, 0, 0)

# Cargar la imagen de la nave
nave_img = pygame.image.load('nave.png').convert_alpha()
nave_rect = nave_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Velocidad de movimiento
speed = 5

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # Movimiento de la nave
    if keys[pygame.K_LEFT]:
        nave_rect.x -= speed  # Mover a la izquierda
    if keys[pygame.K_RIGHT]:
        nave_rect.x += speed  # Mover a la derecha
    if keys[pygame.K_UP]:
        nave_rect.y -= speed  # Mover hacia arriba
    if keys[pygame.K_DOWN]:
        nave_rect.y += speed  # Mover hacia abajo

    # Limitar el movimiento dentro de la pantalla
    nave_rect.x = max(0, min(nave_rect.x, WIDTH - nave_rect.width))
    nave_rect.y = max(0, min(nave_rect.y, HEIGHT - nave_rect.height))

    # Limpiar la pantalla
    screen.fill(BLACK)

    # Dibujar la nave
    screen.blit(nave_img, nave_rect.topleft)

    # Actualizar la pantalla
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Salir de Pygame
pygame.quit()
