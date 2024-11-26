import pygame
import sys

pygame.init()

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)

ANCHO = 800
ALTO = 600

screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Mover Cajas")

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.velocidad = 5

    def update(self, teclas, obstaculos):
        # Verificar límites para el movimiento horizontal (izquierda y derecha)
        if teclas[pygame.K_LEFT] and self.rect.x > 0:  # No se pasa de la izquierda
            self.rect.x -= self.velocidad
            if pygame.sprite.spritecollide(self, obstaculos, False):  # Colisión a la izquierda
                self.rect.x += self.velocidad  # Deshacer movimiento

        if teclas[pygame.K_RIGHT] and self.rect.x < ANCHO - self.rect.width:  # No se pasa de la derecha
            self.rect.x += self.velocidad
            if pygame.sprite.spritecollide(self, obstaculos, False):  # Colisión a la derecha
                self.rect.x -= self.velocidad  # Deshacer movimiento

        # Verificar colisión para movimiento hacia abajo (no pasar por debajo de obstáculos)
        if teclas[pygame.K_DOWN] and self.rect.y < ALTO - self.rect.height:  # No se pasa de abajo
            self.rect.y += self.velocidad
            if pygame.sprite.spritecollide(self, obstaculos, False):  # Colisión abajo
                self.rect.y -= self.velocidad  # Deshacer movimiento

        # Verificar colisión para movimiento hacia arriba (no pasar por encima de obstáculos)
        if teclas[pygame.K_UP] and self.rect.y > 0:  # No se pasa de arriba
            self.rect.y -= self.velocidad
            if pygame.sprite.spritecollide(self, obstaculos, False):  # Colisión arriba
                self.rect.y += self.velocidad  # Deshacer movimiento


class Caja(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Función para mover las cajas y evitar que atraviesen los obstáculos
def mover_caja_alejada(caja, teclas, obstaculos):
    if teclas[pygame.K_LEFT]:
        if pygame.sprite.spritecollide(caja, obstaculos, False):
            caja.rect.x += 5  # Mover hacia la derecha
        else:
            caja.rect.x -= 5
    if teclas[pygame.K_RIGHT]:
        if pygame.sprite.spritecollide(caja, obstaculos, False):
            caja.rect.x -= 5  # Mover hacia la izquierda
        else:
            caja.rect.x += 5
    if teclas[pygame.K_UP]:
        if pygame.sprite.spritecollide(caja, obstaculos, False):
            caja.rect.y += 5  # Mover hacia abajo
        else:
            caja.rect.y -= 5
    if teclas[pygame.K_DOWN]:
        if pygame.sprite.spritecollide(caja, obstaculos, False):
            caja.rect.y -= 5  # Mover hacia arriba
        else:
            caja.rect.y += 5


# Crear el jugador, las cajas y los obstáculos
jugador = Jugador()
cajas = pygame.sprite.Group()

# Colocar algunas cajas en el mapa
caja1 = Caja(200, 200)
caja2 = Caja(300, 300)
cajas.add(caja1, caja2)

# Crear algunos obstáculos en el mapa
obstaculo1 = Obstaculo(400, 200)
obstaculo2 = Obstaculo(500, 300)
obstaculos = pygame.sprite.Group()
obstaculos.add(obstaculo1, obstaculo2)

# Definir la zona segura (un área rectangular)
zona_segura = pygame.Rect(600, 100, 100, 100)

# Variables para mostrar el mensaje
mensaje = ""
fuente = pygame.font.Font(None, 36)

# Temporizador
tiempo_maximo = 30  # en segundos
tiempo_restante = tiempo_maximo  # en segundos
tiempo_inicio = pygame.time.get_ticks()  # tiempo en milisegundos desde que comenzó el juego

todos_los_sprites = pygame.sprite.Group()
todos_los_sprites.add(jugador, *cajas, *obstaculos)

running = True
while running:
    screen.fill(BLANCO)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    teclas = pygame.key.get_pressed()
    jugador.update(teclas, obstaculos)

    # Mover las cajas con el jugador
    for caja in cajas:
        if jugador.rect.colliderect(caja.rect):
            mover_caja_alejada(caja, teclas, obstaculos)

        # Verificar si la caja está dentro de la zona segura
        if zona_segura.colliderect(caja.rect):
            mensaje = "¡Perfecto!"
    
    # Actualizar el temporizador
    tiempo_transcurrido = (pygame.time.get_ticks() - tiempo_inicio) / 1000  # convertir a segundos
    tiempo_restante = max(0, tiempo_maximo - tiempo_transcurrido)

    # Verificar si el tiempo se agotó
    if tiempo_restante == 0:
        mensaje = "¡Se acabó el tiempo!"
    
    # Mostrar el tiempo restante
    tiempo_texto = fuente.render(f"Tiempo: {int(tiempo_restante)}s", True, NEGRO)
    screen.blit(tiempo_texto, (10, 10))  # Mostrar tiempo en la parte superior izquierda

    # Dibujar la zona segura (visualmente)
    pygame.draw.rect(screen, AMARILLO, zona_segura)

    # Dibujar los mensajes en la pantalla
    if mensaje:
        texto = fuente.render(mensaje, True, NEGRO)
        screen.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))

    # Dibujar todos los sprites
    todos_los_sprites.draw(screen)

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
