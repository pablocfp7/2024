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

# Velocidad del juego
FPS = 60
reloj = pygame.time.Clock()

# Fuente para la puntuación y el mensaje
fuente_puntuacion = pygame.font.SysFont("Arial", 30)
fuente_mensaje = pygame.font.SysFont("Arial", 50)


# Clase para la pelota
class Pelota:
    def __init__(self):
        self.radio = 10
        self.x = ANCHO // 2
        self.y = ALTO // 2
        self.velocidad_x = 7 * random.choice((1, -1))
        self.velocidad_y = 7 * random.choice((1, -1))
        self.aceleracion = 0.1  # Factor de aceleración
        self.vel_max = 15  # Velocidad máxima

    def mover(self):
        self.x += self.velocidad_x
        self.y += self.velocidad_y

        # Colisiones con el borde superior e inferior
        if self.y - self.radio <= 0 or self.y + self.radio >= ALTO:
            self.velocidad_y = -self.velocidad_y
            self.acelerar()

    def colision_pala(self, pala):
        if pala.x <= self.x + self.radio <= pala.x + pala.ancho and pala.y <= self.y <= pala.y + pala.alto:
            self.velocidad_x = -self.velocidad_x
            self.acelerar()

    def reiniciar(self):
        self.x = ANCHO // 2
        self.y = ALTO // 2
        self.velocidad_x = 7 * random.choice((1, -1))
        self.velocidad_y = 7 * random.choice((1, -1))

    def acelerar(self):
        """Acelera la pelota hasta un límite máximo"""
        if abs(self.velocidad_x) < self.vel_max:
            self.velocidad_x += self.aceleracion * (1 if self.velocidad_x > 0 else -1)
        if abs(self.velocidad_y) < self.vel_max:
            self.velocidad_y += self.aceleracion * (1 if self.velocidad_y > 0 else -1)

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, BLANCO, (self.x, self.y), self.radio)


# Clase para las palas
class Pala:
    def __init__(self, x):
        self.ancho = 15
        self.alto = 100
        self.x = x
        self.y = ALTO // 2 - self.alto // 2
        self.velocidad = 10

    def mover(self, direccion):
        if direccion == "arriba" and self.y > 0:
            self.y -= self.velocidad
        elif direccion == "abajo" and self.y < ALTO - self.alto:
            self.y += self.velocidad

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, BLANCO, (self.x, self.y, self.ancho, self.alto))


# Clase para el juego
class PingPong:
    def __init__(self):
        self.puntos_izquierda = 0
        self.puntos_derecha = 0
        self.pala_izquierda = Pala(50)
        self.pala_derecha = Pala(ANCHO - 50 - 15)
        self.pelota = Pelota()

    def dibujar_elementos(self, pantalla):
        pantalla.fill(NEGRO)  # Fondo negro

        # Dibujar las palas
        self.pala_izquierda.dibujar(pantalla)
        self.pala_derecha.dibujar(pantalla)

        # Dibujar la pelota
        self.pelota.dibujar(pantalla)

        # Línea central
        pygame.draw.circle(pantalla, BLANCO, (ANCHO // 2, ALTO // 2), 50, 1)

        # Mostrar la puntuación
        texto_puntos_izquierda = fuente_puntuacion.render(str(self.puntos_izquierda), True, BLANCO)
        pantalla.blit(texto_puntos_izquierda, (ANCHO // 4, 20))
        texto_puntos_derecha = fuente_puntuacion.render(str(self.puntos_derecha), True, BLANCO)
        pantalla.blit(texto_puntos_derecha, (ANCHO * 3 // 4 - texto_puntos_derecha.get_width(), 20))

    def mover_elementos(self):
        self.pelota.mover()

        # Colisiones con las palas
        self.pelota.colision_pala(self.pala_izquierda)
        self.pelota.colision_pala(self.pala_derecha)

        # Verificar si algún jugador ha ganado
        if self.pelota.x - self.pelota.radio <= 0:
            self.puntos_derecha += 1
            self.pelota.reiniciar()

        if self.pelota.x + self.pelota.radio >= ANCHO:
            self.puntos_izquierda += 1
            self.pelota.reiniciar()

    def mover_paletas(self):
        teclas = pygame.key.get_pressed()
        # Movimiento de las palas del jugador humano (usando las teclas de arriba y abajo)
        if teclas[pygame.K_w]:
            self.pala_izquierda.mover("arriba")
        if teclas[pygame.K_s]:
            self.pala_izquierda.mover("abajo")

        # Movimiento de la IA (pala derecha) - la IA sigue la pelota
        if self.pala_derecha.y + self.pala_derecha.alto // 2 < self.pelota.y:
            self.pala_derecha.mover("abajo")
        elif self.pala_derecha.y + self.pala_derecha.alto // 2 > self.pelota.y:
            self.pala_derecha.mover("arriba")

    def mostrar_ganador(self, pantalla, mensaje):
        texto_ganador = fuente_mensaje.render(mensaje, True, BLANCO)
        pantalla.blit(texto_ganador, (ANCHO // 2 - texto_ganador.get_width() // 2, ALTO // 2 - texto_ganador.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(2000)  # Esperar 2 segundos antes de salir


# Función principal del juego
def juego():
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Ping Pong")

    ping_pong = PingPong()
    jugando = True

    while jugando:
        reloj.tick(FPS)

        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

        # Verificar si algún jugador ha ganado
        if ping_pong.puntos_izquierda >= 21:
            ping_pong.mostrar_ganador(pantalla, "¡Jugador Izquierda Gana!")
            break
        elif ping_pong.puntos_derecha >= 21:
            ping_pong.mostrar_ganador(pantalla, "¡Computadora Gana!")
            break

        # Mover las palas (humano y IA)
        ping_pong.mover_paletas()
        ping_pong.mover_elementos()

        # Dibujar los elementos en pantalla
        ping_pong.dibujar_elementos(pantalla)

        # Actualizar la pantalla
        pygame.display.update()

    # Salir del juego
    pygame.quit()

# Ejecutar el juego
juego()
