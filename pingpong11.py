import pygame
import random
from time import sleep as sp

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
        # Cargar la imagen de la pelota
        self.imagen = pygame.image.load('pelota.png')  # Asegúrate de que 'pelota.png' esté en el directorio
        self.imagen = pygame.transform.scale(self.imagen, (20, 20))  # Ajusta el tamaño si es necesario
        self.rect = self.imagen.get_rect()
        self.rect.center = (ANCHO // 2, ALTO // 2)  # Centrar la pelota
        self.velocidad_x = 7 * random.choice((1, -1))
        self.velocidad_y = 7 * random.choice((1, -1))
        self.aceleracion = 0.1  # Factor de aceleración
        self.vel_max = 15  # Velocidad máxima

    def mover(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # Colisiones con el borde superior e inferior
        if self.rect.top <= 0 or self.rect.bottom >= ALTO:
            self.velocidad_y = -self.velocidad_y
            self.acelerar()

    def colision_pala(self, pala):
        if pala.rect.colliderect(self.rect):
            self.velocidad_x = -self.velocidad_x
            self.acelerar()

    def reiniciar(self):
        self.rect.center = (ANCHO // 2, ALTO // 2)
        self.velocidad_x = 6.1 * random.choice((1, -1))
        self.velocidad_y = 6.1 * random.choice((1, -1))

    def acelerar(self):
        """Acelera la pelota hasta un límite máximo"""
        if abs(self.velocidad_x) < self.vel_max:
            self.velocidad_x += self.aceleracion * (1 if self.velocidad_x > 0 else -1)
        if abs(self.velocidad_y) < self.vel_max:
            self.velocidad_y += self.aceleracion * (1 if self.velocidad_y > 0 else -1)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)  # Dibujar la imagen de la pelota


# Clase para las palas
class Pala:
    def __init__(self, x):
        self.ancho = 15
        self.alto = 100
        self.x = x
        self.y = ALTO // 2 - self.alto // 2
        self.velocidad = 10
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def mover(self, direccion):
        if direccion == "arriba" and self.rect.top > 0:
            self.rect.y -= self.velocidad
        elif direccion == "abajo" and self.rect.bottom < ALTO:
            self.rect.y += self.velocidad

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, BLANCO, self.rect)


# Clase para el juego
class PingPong:
    def __init__(self):
        self.puntos_izquierda = 0
        self.puntos_derecha = 0
        self.pala_izquierda = Pala(50)
        self.pala_derecha = Pala(ANCHO - 50 - 15)
        self.pelota = Pelota()
        self.factor_lentitud_ia = 0.7  # Coeficiente para hacer que la IA sea más lenta
        self.margen_error_ia = 15  # Margen de error en la posición de la IA

    def dibujar_elementos(self, pantalla):
        pantalla.fill(NEGRO)  # Fondo negro

        # Dibujar las palas
        self.pala_izquierda.dibujar(pantalla)
        self.pala_derecha.dibujar(pantalla)

        # Dibujar la pelota
        self.pelota.dibujar(pantalla)

        # Dibujar la red central (líneas cortas)
        self.dibujar_red(pantalla)

        # Mostrar la puntuación
        texto_puntos_izquierda = fuente_puntuacion.render(str(self.puntos_izquierda), True, BLANCO)
        pantalla.blit(texto_puntos_izquierda, (ANCHO // 4, 20))
        texto_puntos_derecha = fuente_puntuacion.render(str(self.puntos_derecha), True, BLANCO)
        pantalla.blit(texto_puntos_derecha, (ANCHO * 3 // 4 - texto_puntos_derecha.get_width(), 20))

    def dibujar_red(self, pantalla):
        """Dibuja la red en el centro de la pantalla (líneas cortas)"""
        numero_lineas = 15  # Número de líneas que tendrá la red
        ancho_linea = 4
        distancia_lineas = ALTO // numero_lineas

        for i in range(numero_lineas):
            pygame.draw.rect(
                pantalla,
                BLANCO,
                pygame.Rect(ANCHO // 2 - ancho_linea // 2, i * distancia_lineas, ancho_linea, distancia_lineas)
            )

    def mover_elementos(self):
        self.pelota.mover()

        # Colisiones con las palas
        self.pelota.colision_pala(self.pala_izquierda)
        self.pelota.colision_pala(self.pala_derecha)

        # Verificar si algún jugador ha ganado
        if self.pelota.rect.left <= 0:
            self.puntos_derecha += 1
            self.pelota.reiniciar()

        if self.pelota.rect.right >= ANCHO:
            self.puntos_izquierda += 1
            self.pelota.reiniciar()

    def mover_paletas(self):
        teclas = pygame.key.get_pressed()
        # Movimiento de las palas del jugador humano (usando las teclas de arriba y abajo)
        if teclas[pygame.K_w]:
            self.pala_izquierda.mover("arriba")
        if teclas[pygame.K_s]:
            self.pala_izquierda.mover("abajo")

        # Movimiento de la IA (pala derecha) - la IA sigue la pelota con margen de error
        if self.pala_derecha.rect.centery < self.pelota.rect.centery:
            # La IA se mueve hacia abajo pero con lentitud y margen de error
            if self.pala_derecha.rect.centery + self.pala_derecha.alto // 10 < self.pelota.rect.centery:
                # Introducimos un margen de error aleatorio para la posición de la IA
                if random.randint(-self.margen_error_ia, self.margen_error_ia) != 0:
                    self.pala_derecha.mover("abajo")
        elif self.pala_derecha.rect.centery > self.pelota.rect.centery:
            # La IA se mueve hacia arriba pero con lentitud y margen de error
            if self.pala_derecha.rect.centery - self.pala_derecha.alto // 10 > self.pelota.rect.centery:
                # Introducimos un margen de error aleatorio para la posición de la IA
                if random.randint(-self.margen_error_ia, self.margen_error_ia) != 0:
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
        elif ping_pong.puntos_derecha >= 2:
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
