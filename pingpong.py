import pygame
import random

pygame.init()

ANCHO = 800
ALTO = 600

BLANCO = (255, 255, 255)

FPS = 60
reloj = pygame.time.Clock()

fuente_puntuacion = pygame.font.SysFont("Arial", 60)
fuente_mensaje = pygame.font.SysFont("Arial", 70)

fondo_cancha = pygame.image.load("canchadetenis.jpg")
fondo_cancha = pygame.transform.scale(fondo_cancha, (ANCHO, ALTO))
imagen_raqueta = pygame.image.load("raqueta izquierda.png")
imagen_raqueta = pygame.transform.scale(imagen_raqueta, (30, 120))
pelota_tenis = pygame.image.load("pelotadetenis.png")
pelota_tenis = pygame.transform.scale(pelota_tenis, (20, 20))

class Pelota:
    def __init__(self):
        self.radio = 10
        self.x = ANCHO // 2
        self.y = ALTO // 2
        self.velocidad_x = 7 * random.choice((1, -1))
        self.velocidad_y = 7 * random.choice((1, -1))
        self.aceleracion = 0.1
        self.vel_max = 15

    def mover(self):
        self.x += self.velocidad_x
        self.y += self.velocidad_y

        if self.y - self.radio <= 0 or self.y + self.radio >= ALTO:
            self.velocidad_y = -self.velocidad_y
            self.acelerar()

    def colision_pala(self, pala):
        if pala.x <= self.x + self.radio <= pala.x + pala.ancho and pala.y <= self.y <= pala.y + pala.alto:
            self.velocidad_x = -self.velocidad_x
            pala.golpear()
            self.acelerar()

    def reiniciar(self):
        self.x = ANCHO // 2
        self.y = ALTO // 2
        self.velocidad_x = 6.1 * random.choice((1, -1))
        self.velocidad_y = 6.1 * random.choice((1, -1))

    def acelerar(self):
        if abs(self.velocidad_x) < self.vel_max:
            self.velocidad_x += self.aceleracion * (1 if self.velocidad_x > 0 else -1)
        if abs(self.velocidad_y) < self.vel_max:
            self.velocidad_y += self.aceleracion * (1 if self.velocidad_y > 0 else -1)

    def dibujar(self, pantalla):
        pantalla.blit(pelota_tenis, (self.x - self.radio, self.y - self.radio))

class Pala:
    def __init__(self, x):
        self.ancho = 30
        self.alto = 120
        self.x = x
        self.y = ALTO // 2 - self.alto // 2
        self.velocidad = 10
        self.golpeando = False
        self.angulo = 0

    def mover(self, direccion):
        if direccion == "arriba" and self.y > 0:
            self.y -= self.velocidad
        elif direccion == "abajo" and self.y < ALTO - self.alto:
            self.y += self.velocidad

    def golpear(self):
        self.golpeando = True

    def animar_golpe(self):
        if self.golpeando:
            self.angulo = -30
            self.golpeando = False
        else:
            if self.angulo < 0:
                self.angulo += 5

    def dibujar(self, pantalla):
        self.animar_golpe()
        raqueta_rotada = pygame.transform.rotate(imagen_raqueta, self.angulo)
        pantalla.blit(raqueta_rotada, (self.x, self.y))

class PingPong:
    def __init__(self):
        self.puntos_izquierda = 0
        self.puntos_derecha = 0
        self.pala_izquierda = Pala(50)
        self.pala_derecha = Pala(ANCHO - 80)
        self.pelota = Pelota()

    def dibujar_elementos(self, pantalla):
        pantalla.blit(fondo_cancha, (0, 0))

        self.pala_izquierda.dibujar(pantalla)
        self.pala_derecha.dibujar(pantalla)
        self.pelota.dibujar(pantalla)
        pygame.draw.line(pantalla, BLANCO, (ANCHO // 2, 0), (ANCHO // 2, ALTO), 2)
        texto_puntos_izquierda = fuente_puntuacion.render(str(self.puntos_izquierda), True, BLANCO)
        pantalla.blit(texto_puntos_izquierda, (ANCHO // 4, 20))
        texto_puntos_derecha = fuente_puntuacion.render(str(self.puntos_derecha), True, BLANCO)
        pantalla.blit(texto_puntos_derecha, (ANCHO * 3 // 4 - texto_puntos_derecha.get_width(), 20))

    def mover_elementos(self):
        self.pelota.mover()
        self.pelota.colision_pala(self.pala_izquierda)
        self.pelota.colision_pala(self.pala_derecha)
        if self.pelota.x - self.pelota.radio <= 0:
            self.puntos_derecha += 1
            self.pelota.reiniciar()

        if self.pelota.x + self.pelota.radio >= ANCHO:
            self.puntos_izquierda += 1
            self.pelota.reiniciar()

    def mover_paletas(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w]:
            self.pala_izquierda.mover("arriba")
        if teclas[pygame.K_s]:
            self.pala_izquierda.mover("abajo")
        if self.pala_derecha.y + self.pala_derecha.alto // 2 < self.pelota.y:
            self.pala_derecha.mover("abajo")
        elif self.pala_derecha.y + self.pala_derecha.alto // 2 > self.pelota.y:
            self.pala_derecha.mover("arriba")

    def mostrar_ganador(self, pantalla, mensaje):
        texto_ganador = fuente_mensaje.render(mensaje, True, BLANCO)
        pantalla.blit(texto_ganador,
                      (ANCHO // 2 - texto_ganador.get_width() // 2, ALTO // 2 - texto_ganador.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(2000)

def juego():
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Ping Pong")

    ping_pong = PingPong()
    jugando = True

    while jugando:
        reloj.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False
        if ping_pong.puntos_izquierda >= 21:
            ping_pong.mostrar_ganador(pantalla, "¡Jugador Izquierda Gana!")
            break
        elif ping_pong.puntos_derecha >= 21:
            ping_pong.mostrar_ganador(pantalla, "¡Computadora Gana!")
            break

        ping_pong.mover_paletas()
        ping_pong.mover_elementos()
        ping_pong.dibujar_elementos(pantalla)
        pygame.display.update()

    pygame.quit()

juego()
