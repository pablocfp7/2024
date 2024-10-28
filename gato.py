import pygame
import random


pygame.init()


ANCHO = 800
ALTO = 600
COLOR_FONDO = (255, 255, 255)
COLOR_TEXTO = (0, 0, 0)


pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Cuidado de Gato")


class Gato:
    def __init__(self):
        self.felicidad = 100
        self.hambre = 0
        self.salud = 100

    def alimentar(self):
        self.hambre = max(self.hambre - 20, 0)

    def jugar(self):
        self.felicidad = min(self.felicidad + 20, 100)
        self.hambre += 10

    def pasar_tiempo(self):
        self.hambre = min(self.hambre + 1, 100)
        self.felicidad = max(self.felicidad - 1, 0)

    def estado(self):
        return f"Felicidad: {self.felicidad}, Hambre: {self.hambre}, Salud: {self.salud}"


gato = Gato()


corriendo = True
reloj = pygame.time.Clock()

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:  #  alimentar
                gato.alimentar()
            if evento.key == pygame.K_j:  # jugar
                gato.jugar()


    gato.pasar_tiempo()


    pantalla.fill(COLOR_FONDO)
    fuente = pygame.font.SysFont(None, 36)
    texto = fuente.render(gato.estado(), True, COLOR_TEXTO)
    pantalla.blit(texto, (50, 50))

    pygame.display.flip()
    reloj.tick(30)

pygame.quit()
