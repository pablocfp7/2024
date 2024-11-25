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

    def update(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if teclas[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN]:
            self.rect.y += self.velocidad


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


# Función para mover la caja azul y evitar que atraviese las otras cajas
def mover_caja_alejada(caja, teclas, obstaculos, cajas):
    if teclas[pygame.K_LEFT]:
        # Comprobar si la caja azul colide con una caja roja
        for otra_caja in cajas:
            if caja.rect.colliderect(otra_caja.rect) and caja.rect.left < otra_caja.rect.right:
                caja.rect.x = otra_caja.rect.right  # Detener la caja azul en el borde derecho de la caja roja
                return
        caja.rect.x -= 5

    if teclas[pygame.K_RIGHT]:
        for otra_caja in cajas:
            if caja.rect.colliderect(otra_caja.rect) and caja.rect.right > otra_caja.rect.left:
                caja.rect.x = otra_caja.rect.left - caja.rect.width  # Detener la caja azul en el borde izquierdo de la caja roja
                return
        caja.rect.x += 5

    if teclas[pygame.K_UP]:
        for otra_caja in cajas:
            if caja.rect.colliderect(otra_caja.rect) and caja.rect.top < otra_caja.rect.bottom:
                caja.rect.y = otra_caja.rect.bottom  # Detener la caja azul en el borde inferior de la caja roja
                return
        caja.rect.y -= 5

    if teclas[pygame.K_DOWN]:
        for otra_caja in cajas:
            if caja.rect.colliderect(otra_caja.rect) and caja.rect.bottom > otra_caja.rect.top:
                caja.rect.y = otra_caja.rect.top - caja.rect.height  # Detener la caja azul en el borde superior de la caja roja
                return
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

todos_los_sprites = pygame.sprite.Group()
todos_los_sprites.add(jugador, *cajas, *obstaculos)

running = True
while running:
    screen.fill(BLANCO)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    teclas = pygame.key.get_pressed()
    jugador.update(teclas)

    # Mover las cajas con el jugador
    for caja in cajas:
        if jugador.rect.colliderect(caja.rect):
            mover_caja_alejada(caja, teclas, obstaculos, cajas)

        # Verificar si la caja está dentro de la zona segura
        if zona_segura.colliderect(caja.rect):
            mensaje = "¡Perfecto!"
    
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
