import pygame
import random

# Inicializamos Pygame
pygame.init()

# Dimensiones de la pantalla
ANCHO = 800
ALTO = 600

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ping Pong")

# Velocidad del juego
FPS = 60
reloj = pygame.time.Clock()

# Palas
pala_ancho = 15
pala_alto = 100
pala_velocidad = 10

# Pelota
pelota_radio = 10
pelota_velocidad_x = 7 * random.choice((1, -1))
pelota_velocidad_y = 7 * random.choice((1, -1))

# Posiciones iniciales
pala_izquierda_y = ALTO // 2 - pala_alto // 2
pala_derecha_y = ALTO // 2 - pala_alto // 2
pelota_x = ANCHO // 2
pelota_y = ALTO // 2

# Puntuación
puntos_izquierda = 0
puntos_derecha = 0
fuente_puntuacion = pygame.font.SysFont("Arial", 30)
fuente_mensaje = pygame.font.SysFont("Arial", 50)

# Función para dibujar los elementos en la pantalla
def dibujar_elementos():
    pantalla.fill(NEGRO)  # Fondo negro
    pygame.draw.rect(pantalla, BLANCO, (50, pala_izquierda_y, pala_ancho, pala_alto))  # Pala izquierda
    pygame.draw.rect(pantalla, BLANCO, (ANCHO - 50 - pala_ancho, pala_derecha_y, pala_ancho, pala_alto))  # Pala derecha
    pygame.draw.circle(pantalla, BLANCO, (ANCHO // 2, ALTO // 2), 50, 1)  # Línea central

    # Dibujar la pelota como un círculo
    pygame.draw.circle(pantalla, BLANCO, (pelota_x, pelota_y), pelota_radio)  # Pelota

    # Mostrar la puntuación
    texto_puntos_izquierda = fuente_puntuacion.render(str(puntos_izquierda), True, BLANCO)
    pantalla.blit(texto_puntos_izquierda, (ANCHO // 4, 20))
    texto_puntos_derecha = fuente_puntuacion.render(str(puntos_derecha), True, BLANCO)
    pantalla.blit(texto_puntos_derecha, (ANCHO * 3 // 4 - texto_puntos_derecha.get_width(), 20))

# Función para mover la pelota
def mover_pelota():
    global pelota_x, pelota_y, pelota_velocidad_x, pelota_velocidad_y, puntos_izquierda, puntos_derecha

    pelota_x += pelota_velocidad_x
    pelota_y += pelota_velocidad_y

    # Colisiones con el borde superior e inferior
    if pelota_y - pelota_radio <= 0 or pelota_y + pelota_radio >= ALTO:
        pelota_velocidad_y = -pelota_velocidad_y

    # Colisiones con las palas
    if pelota_x - pelota_radio <= 50 + pala_ancho and pala_izquierda_y < pelota_y < pala_izquierda_y + pala_alto:
        pelota_velocidad_x = -pelota_velocidad_x

    if pelota_x + pelota_radio >= ANCHO - 50 - pala_ancho and pala_derecha_y < pelota_y < pala_derecha_y + pala_alto:
        pelota_velocidad_x = -pelota_velocidad_x

    # Si la pelota sale por la izquierda o la derecha, se puntúa
    if pelota_x - pelota_radio <= 0:
        puntos_derecha += 1
        reiniciar_pelota()

    if pelota_x + pelota_radio >= ANCHO:
        puntos_izquierda += 1
        reiniciar_pelota()

# Función para reiniciar la pelota al centro
def reiniciar_pelota():
    global pelota_x, pelota_y, pelota_velocidad_x, pelota_velocidad_y
    pelota_x = ANCHO // 2
    pelota_y = ALTO // 2
    pelota_velocidad_x = 7 * random.choice((1, -1))
    pelota_velocidad_y = 7 * random.choice((1, -1))

# Función para mostrar el mensaje de ganador
def mostrar_ganador(mensaje):
    texto_ganador = fuente_mensaje.render(mensaje, True, BLANCO)
    pantalla.blit(texto_ganador, (ANCHO // 2 - texto_ganador.get_width() // 2, ALTO // 2 - texto_ganador.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(2000)  # Esperar 2 segundos antes de salir

# Función principal del juego
def juego():
    global pala_izquierda_y, pala_derecha_y

    jugando = True
    while jugando:
        reloj.tick(FPS)

        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

        # Verificar si algún jugador ha ganado
        if puntos_izquierda >= 21:
            mostrar_ganador("¡Jugador Izquierda Gana!")
            break
        elif puntos_derecha >= 21:
            mostrar_ganador("¡Jugador Derecha Gana!")
            break

        # Movimiento de las palas (usando las teclas de arriba y abajo)
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w] and pala_izquierda_y > 0:
            pala_izquierda_y -= pala_velocidad
        if teclas[pygame.K_s] and pala_izquierda_y < ALTO - pala_alto:
            pala_izquierda_y += pala_velocidad

        if teclas[pygame.K_UP] and pala_derecha_y > 0:
            pala_derecha_y -= pala_velocidad
        if teclas[pygame.K_DOWN] and pala_derecha_y < ALTO - pala_alto:
            pala_derecha_y += pala_velocidad

        # Mover la pelota
        mover_pelota()

        # Dibujar todos los elementos
        dibujar_elementos()

        # Actualizar la pantalla
        pygame.display.update()

    # Salir del juego
    pygame.quit()

# Ejecutar el juego
juego()
