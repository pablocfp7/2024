import pygame
import sys

# Inicializamos Pygame
pygame.init()

# Parámetros de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulación de Rebote de Pelota")

# Parámetros de la pelota
radio = 20
x, y = ANCHO // 2, ALTO // 2  # Posición inicial
vel_x, vel_y = 5, -5  # Velocidad inicial
coef_rebote = 0.9  # Coeficiente de restitución (rebote)
friccion = 0.99  # Resistencia al aire (decremento de la velocidad)
color_pelota = (255, 0, 0)  # Color rojo

# Reloj para controlar la tasa de fotogramas
reloj = pygame.time.Clock()

# Bucle principal de la simulación
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Actualizamos la posición de la pelota
    x += vel_x
    y += vel_y

    # Rebotamos la pelota contra las paredes
    if x - radio <= 0 or x + radio >= ANCHO:  # Rebote horizontal
        vel_x = -vel_x * coef_rebote
        vel_x *= friccion  # Aplicamos fricción

    if y - radio <= 0 or y + radio >= ALTO:  # Rebote vertical
        vel_y = -vel_y * coef_rebote
        vel_y *= friccion  # Aplicamos fricción

    # Limpiamos la pantalla y dibujamos la pelota
    pantalla.fill((0, 0, 0))  # Fondo negro
    pygame.draw.circle(pantalla, color_pelota, (x, y), radio)

    # Actualizamos la pantalla
    pygame.display.flip()

    # Limitamos la velocidad de la simulación
    reloj.tick(110)
