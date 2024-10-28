import pygame
import random
import pickle


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
        self.suciedad = 0

    def alimentar(self):
        self.hambre = max(self.hambre - 20, 0)

    def jugar(self):
        self.felicidad = min(self.felicidad + 20, 100)
        self.hambre += 10

    def limpiar(self):
        self.suciedad = max(self.suciedad - 20, 0)

    def visitar_veterinario(self):
        self.salud = min(self.salud + 20, 100)

    def pasar_tiempo(self):
        
        if self.hambre < 80:
            self.hambre = min(self.hambre + 1, 100)
        else:
            self.hambre = min(self.hambre + 0.5, 100)  
        
        if self.felicidad > 20:
            self.felicidad = max(self.felicidad - 0.5, 0) 
        else:
            self.felicidad = max(self.felicidad - 1, 0)  
        
        if self.suciedad < 80:
            self.suciedad = min(self.suciedad + 0.5, 100)  
        else:
            self.suciedad = min(self.suciedad + 1, 100)  
        

        if self.hambre >= 100:
            self.salud = max(self.salud - 5, 0)

    def estado(self):
        return f"Felicidad: {self.felicidad}, Hambre: {self.hambre}, Salud: {self.salud}, Suciedad: {self.suciedad}"


def cargar_gato():
    try:
        with open("gato.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return Gato()


def guardar_gato(gato):
    with open("gato.pkl", "wb") as f:
        pickle.dump(gato, f)


gato = cargar_gato()


corriendo = True
reloj = pygame.time.Clock()

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:  # Tecla 'A' para alimentar
                gato.alimentar()
            if evento.key == pygame.K_j:  # Tecla 'J' para jugar
                gato.jugar()
            if evento.key == pygame.K_l:  # Tecla 'L' para limpiar
                gato.limpiar()
            if evento.key == pygame.K_v:  # Tecla 'V' para ir al veterinario
                gato.visitar_veterinario()


    gato.pasar_tiempo()


    pantalla.fill(COLOR_FONDO)
    fuente = pygame.font.SysFont(None, 36)
    texto = fuente.render(gato.estado(), True, COLOR_TEXTO)
    pantalla.blit(texto, (50, 50))


    pygame.display.flip()
    reloj.tick(30)


guardar_gato(gato)
pygame.quit()
