import pygame
import random

pygame.init()

ancho_ventana = 800
alto_ventana = 600
ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("Evitando")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)

jugador_ancho = 50
jugador_alto = 50
jugador_x = ancho_ventana // 2 - jugador_ancho // 2
jugador_y = alto_ventana - jugador_alto - 10
velocidad_jugador = 5

vidas = 5
fuera = False

obstaculos = []
reloj = pygame.time.Clock()
contador_obstaculos = 0

while not fuera:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fuera = True

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jugador_x > 0:
        jugador_x -= velocidad_jugador
    if teclas[pygame.K_RIGHT] and jugador_x < ancho_ventana - jugador_ancho:
        jugador_x += velocidad_jugador

    
    contador_obstaculos += 1
    if contador_obstaculos >= 30:  
        obstáculo_x = random.randint(0, ancho_ventana - 50)
        obstaculos.append([obstáculo_x, 0])  
        contador_obstaculos = 0

    
    for obstáculo in obstaculos[:]:  
        obstáculo[1] += 5  
        if (jugador_x < obstáculo[0] + 50 and
            jugador_x + jugador_ancho > obstáculo[0] and
            jugador_y < obstáculo[1] + 50 and
            jugador_y + jugador_alto > obstáculo[1]):
            vidas -= 1
            obstaculos.remove(obstáculo)  

        if obstáculo[1] > alto_ventana:  
            obstaculos.remove(obstáculo)

    ventana.fill(BLANCO)
    pygame.draw.rect(ventana, AZUL, (jugador_x, jugador_y, jugador_ancho, jugador_alto))

    for obstáculo in obstaculos:
        pygame.draw.rect(ventana, NEGRO, (obstáculo[0], obstáculo[1], 50, 50))

    fuente = pygame.font.Font(None, 36)
    texto = fuente.render(f"vidas: {vidas}", True, NEGRO)
    ventana.blit(texto, (10, 10))

    pygame.display.update()
    reloj.tick(60)

    if vidas <= 0:
        fuera = True

pygame.quit()
