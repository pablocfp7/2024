import pygame
import sys

# Inicializamos Pygame
pygame.init()

# Parámetros de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Tirar la Pelota con la Tecla 'C'")

# Parámetros de la pelota
radio = 20
x, y = ANCHO // 2, ALTO // 2  # Posición inicial
vel_x, vel_y = 0, 0  # Velocidad inicial
coef_rebote = 0.8  # Coeficiente de restitución (rebote)
friccion = 0.99  # Resistencia al aire (decremento de la velocidad)
color_pelota = (255, 0, 0)  # Color rojo
gravedad = 0.5  # Gravedad (afecta la velocidad vertical)

# Estado del juego
pelota_tirada = False  # Si la pelota ha sido tirada
tiempo_espera = 0  # Tiempo de espera antes de permitir caer la pelota
esperando = True  # Estado que indica si la pelota está esperando para caer

# Reloj para controlar la tasa de fotogramas
reloj = pygame.time.Clock()

# Bucle principal de la simulación
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Leer las teclas presionadas
    teclas = pygame.key.get_pressed()

    # Si se presiona la tecla "C" y la pelota aún no ha sido tirada, se tira
    if teclas[pygame.K_c] and not pelota_tirada and esperando:
        pelota_tirada = True
        vel_y = -10  # Velocidad inicial hacia abajo
        esperando = False  # Ya no estamos esperando que se presione la tecla

    # Si la pelota ha sido tirada, actualizamos su movimiento
    if pelota_tirada:
        # Aplicar gravedad (aceleración hacia abajo)
        vel_y += gravedad

        # Actualizar la posición de la pelota
        x += vel_x
        y += vel_y

        # Rebotar contra las paredes (horizontal y vertical)
        if x - radio <= 0 or x + radio >= ANCHO:  # Rebote horizontal
            vel_x = -vel_x * coef_rebote
            vel_x *= friccion  # Aplicamos fricción

        if y - radio <= 0 or y + radio >= ALTO:  # Rebote vertical
            vel_y = -vel_y * coef_rebote
            vel_y *= friccion  # Aplicamos fricción

        # Si la pelota llega al borde inferior y su velocidad es pequeña, la detenemos
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
