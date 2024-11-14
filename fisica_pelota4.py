import pygame
import sys

# Inicializamos Pygame
pygame.init()

# Parámetros de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Drag and Drop con Rebote")

# Parámetros de la pelota
radio = 20
x, y = ANCHO // 2, ALTO // 2  # Posición inicial
vel_x, vel_y = 0, 0  # Velocidad inicial
coef_rebote = 0.9  # Coeficiente de restitución (rebote)
friccion = 0.99  # Resistencia al aire (decremento de la velocidad)
color_pelota = (255, 0, 0)  # Color rojo
arrastrando = False  # Si estamos arrastrando la pelota
offset_x, offset_y = 0, 0  # Desplazamiento del mouse al hacer click

# Reloj para controlar la tasa de fotogramas
reloj = pygame.time.Clock()

# Bucle principal de la simulación
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Detectar si se hace clic sobre la pelota para empezar a arrastrarla
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = evento.pos
            # Verificar si el mouse está dentro de la pelota
            if (mouse_x - x) ** 2 + (mouse_y - y) ** 2 <= radio ** 2:
                arrastrando = True
                offset_x = x - mouse_x
                offset_y = y - mouse_y

        # Detectar cuando se suelta el clic para dejar de arrastrar
        elif evento.type == pygame.MOUSEBUTTONUP:
            if arrastrando:
                arrastrando = False
                vel_x, vel_y = 0, 0  # Al soltar, la pelota debe empezar a moverse

    # Si estamos arrastrando la pelota, actualizamos su posición
    if arrastrando:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x = mouse_x + offset_x
        y = mouse_y + offset_y
    else:
        # Actualizamos la posición de la pelota si no estamos arrastrando
        x += vel_x
        y += vel_y

        # Rebotamos la pelota contra las paredes
        if x - radio <= 0 or x + radio >= ANCHO:  # Rebote horizontal
            vel_x = -vel_x * coef_rebote
            vel_x *= friccion  # Aplicamos fricción

        if y - radio <= 0 or y + radio >= ALTO:  # Rebote vertical
            vel_y = -vel_y * coef_rebote
            vel_y *= friccion  # Aplicamos fricción

        # Si la pelota está en la parte inferior y su velocidad es muy pequeña, la detenemos
        if y + radio >= ALTO and abs(vel_y) < 0.1 and abs(vel_x) < 0.1:
            vel_x = 0
            vel_y = 0
            y = ALTO - radio  # Aseguramos que se quede en el borde inferior

    # Limpiamos la pantalla y dibujamos la pelota
    pantalla.fill((0, 0, 0))  # Fondo negro
    pygame.draw.circle(pantalla, color_pelota, (x, y), radio)

    # Actualizamos la pantalla
    pygame.display.flip()

    # Limitamos la velocidad de la simulación
    reloj.tick(60)
