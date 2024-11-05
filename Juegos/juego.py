import pygame
import random

pygame.init()

ancho_ventana = 800
alto_ventana = 600
ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("F1")

BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)

fondo = pygame.image.load("fondo.jpg").convert()
fondo = pygame.transform.scale(fondo, (ancho_ventana, alto_ventana))

fondo_y1 = 0
fondo_y2 = -alto_ventana
velocidad_fondo = 3

jugador_ancho = 50
jugador_alto = 70
jugador_x = 380
jugador_y = 530
velocidad_jugador = 5
jugador_imagen = pygame.image.load("Auto1.png")
jugador_imagen = pygame.transform.scale(jugador_imagen, (40, 70))

vidas = 5
fuera = False

auto_blanco_imagen = pygame.image.load("auto blanco.png")
auto_blanco_imagen = pygame.transform.scale(auto_blanco_imagen, (35, 70))

auto_negro_imagen = pygame.image.load("auto negro.png")
auto_negro_imagen = pygame.transform.scale(auto_negro_imagen, (30, 65))


obstaculos = []
reloj = pygame.time.Clock()
contador_obstaculos = 0

while not fuera:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fuera = True

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jugador_x > 150:
        jugador_x -= velocidad_jugador
    if teclas[pygame.K_RIGHT] and jugador_x < ancho_ventana - 190:
        jugador_x += velocidad_jugador
    if teclas[pygame.K_UP] and jugador_y > 0:
        jugador_y -= velocidad_jugador
    if teclas[pygame.K_DOWN] and jugador_y < alto_ventana - jugador_alto:
        jugador_y += velocidad_jugador


    contador_obstaculos += 1
    if contador_obstaculos >= 30:
        obstáculo_x = random.randint(200, ancho_ventana - 200)
        tipo_obstaculo = random.choice(["Auto_blanco", "Auto_negro"])
        if tipo_obstaculo == "Auto_blanco":
            obstaculos.append([obstáculo_x, 0, auto_blanco_imagen, 100])  # Agregar el auto blanco (imagen y altura)
        else:
            obstaculos.append([obstáculo_x, 0, auto_negro_imagen, 100])  # Agregar el auto negro (imagen y altura)
        contador_obstaculos = 0

    for obstáculo in obstaculos[:]:
        obstáculo[1] += 5
        obstáculo_x, obstáculo_y, obstáculo_imagen, obstáculo_alto = obstáculo

        if (jugador_x < obstáculo_x + 50 and
                jugador_x + jugador_ancho > obstáculo_x and
                jugador_y < obstáculo_y + 50 and
                jugador_y + jugador_alto > obstáculo_y):
            vidas -= 1
            obstaculos.remove(obstáculo)

        if obstáculo_y > alto_ventana:
            obstaculos.remove(obstáculo)

    ventana.blit(fondo, (0, fondo_y1))
    ventana.blit(fondo, (0, fondo_y2))

    fondo_y1 += velocidad_fondo
    fondo_y2 += velocidad_fondo

    if fondo_y1 >= alto_ventana:
        fondo_y1 = fondo_y2 - alto_ventana
    if fondo_y2 >= alto_ventana:
        fondo_y2 = fondo_y1 - alto_ventana

    ventana.blit(jugador_imagen, (jugador_x, jugador_y))

    for obstáculo in obstaculos:
        ventana.blit(obstáculo[2], (obstáculo[0], obstáculo[1]))

    fuente = pygame.font.Font(None, 36)
    texto = fuente.render(f"vidas: {vidas}", True, AZUL)
    ventana.blit(texto, (10, 10))

    pygame.display.update()
    reloj.tick(60)

    if vidas <= 0:
        fuera = True

pygame.quit()